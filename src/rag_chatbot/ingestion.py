"""Document validation, loading, chunking, and corpus identity."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from .config import Settings
from .domain import DocumentChunk, FileIngestionResult, SourceDocument

SUPPORTED_SUFFIXES = {".md", ".markdown", ".pdf"}


class DocumentValidationError(ValueError):
    """Raised when a document cannot be safely processed."""


class UploadedFileLike(Protocol):
    name: str
    size: int

    def getvalue(self) -> bytes: ...


@dataclass(frozen=True, slots=True)
class LoadedDocument:
    source: SourceDocument
    text: str
    page: int | None = None


def validate_path(path: Path, root: Path, settings: Settings) -> None:
    """Validate a source path before reading it."""
    try:
        resolved_path = path.resolve()
        resolved_root = root.resolve()
        resolved_path.relative_to(resolved_root)
    except ValueError as error:
        raise DocumentValidationError(
            "Document path is outside the configured source directory"
        ) from error
    if path.suffix.lower() not in SUPPORTED_SUFFIXES:
        raise DocumentValidationError("Unsupported document type")
    if not path.is_file():
        raise DocumentValidationError("Document does not exist or is not a regular file")
    if path.stat().st_size > settings.max_file_size_bytes:
        raise DocumentValidationError("Document exceeds the configured size limit")


def load_document(path: Path, root: Path, settings: Settings) -> list[LoadedDocument]:
    validate_path(path, root, settings)
    relative_path = path.resolve().relative_to(root.resolve()).as_posix()
    content_hash = _file_hash(path)
    source_id = hashlib.sha256(relative_path.encode("utf-8")).hexdigest()[:24]
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        documents = _load_pdf(path, source_id, relative_path, content_hash)
    else:
        documents = _load_markdown(path, source_id, relative_path, content_hash)
    if not documents or not any(document.text.strip() for document in documents):
        raise DocumentValidationError("Document contains no readable text")
    return documents


def chunk_documents(documents: list[LoadedDocument], settings: Settings) -> list[DocumentChunk]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=1_200, chunk_overlap=160)
    chunks: list[DocumentChunk] = []
    for document in documents:
        pieces = splitter.split_text(document.text)
        for index, text in enumerate(pieces):
            section = _section_for_text(document.text, text, document.source.title)
            chunk_seed = f"{document.source.source_id}:{document.source.content_hash}:{index}"
            chunk_id = hashlib.sha256(chunk_seed.encode("utf-8")).hexdigest()
            chunks.append(
                DocumentChunk(
                    chunk_id=chunk_id,
                    source_id=document.source.source_id,
                    text=text,
                    chunk_index=index,
                    section=section,
                    page=document.page,
                    metadata={
                        "source_id": document.source.source_id,
                        "relative_path": document.source.relative_path,
                        "filename": document.source.filename,
                        "file_type": document.source.file_type,
                        "title": document.source.title,
                        "section": section,
                        "page": document.page,
                        "ingestion_version": settings.ingestion_version,
                    },
                )
            )
    return chunks


def corpus_hash(root: Path, settings: Settings) -> str:
    entries: list[str] = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES:
            validate_path(path, root, settings)
            relative_path = path.resolve().relative_to(root.resolve()).as_posix()
            entries.append(f"{relative_path}:{_file_hash(path)}")
    return hashlib.sha256("\n".join(entries).encode("utf-8")).hexdigest()


def ingest_directory(
    root: Path, settings: Settings
) -> tuple[list[DocumentChunk], list[FileIngestionResult]]:
    paths = sorted(path for path in root.rglob("*") if path.is_file())
    if len(paths) > settings.max_file_count:
        raise DocumentValidationError("Document count exceeds the configured limit")
    chunks: list[DocumentChunk] = []
    results: list[FileIngestionResult] = []
    for path in paths:
        if path.suffix.lower() not in SUPPORTED_SUFFIXES:
            results.append(
                FileIngestionResult(
                    path=str(path), status="skipped", message="Unsupported document type"
                )
            )
            continue
        try:
            loaded = load_document(path, root, settings)
            file_chunks = chunk_documents(loaded, settings)
            chunks.extend(file_chunks)
            results.append(
                FileIngestionResult(
                    path=str(path),
                    status="indexed",
                    message="Indexed",
                    chunk_count=len(file_chunks),
                )
            )
        except (DocumentValidationError, OSError, ValueError) as error:
            results.append(FileIngestionResult(path=str(path), status="failed", message=str(error)))
    return chunks, results


def save_uploaded_files(
    uploaded_files: list[UploadedFileLike], settings: Settings
) -> list[FileIngestionResult]:
    """Persist Streamlit uploads using safe names and configured limits."""
    if len(uploaded_files) > settings.max_file_count:
        raise DocumentValidationError("Uploaded file count exceeds the configured limit")
    settings.documents_path.mkdir(parents=True, exist_ok=True)
    results: list[FileIngestionResult] = []
    for uploaded_file in uploaded_files:
        filename = Path(uploaded_file.name).name
        destination = settings.documents_path / filename
        try:
            if not filename or filename in {".", ".."}:
                raise DocumentValidationError("Invalid uploaded filename")
            if destination.suffix.lower() not in SUPPORTED_SUFFIXES:
                raise DocumentValidationError("Unsupported document type")
            content = uploaded_file.getvalue()
            if len(content) > settings.max_file_size_bytes:
                raise DocumentValidationError("Document exceeds the configured size limit")
            if not content:
                raise DocumentValidationError("Document is empty")
            destination.write_bytes(content)
            results.append(FileIngestionResult(filename, "saved", "File added"))
        except (DocumentValidationError, OSError) as error:
            results.append(FileIngestionResult(filename, "failed", str(error)))
    return results


def _load_markdown(
    path: Path, source_id: str, relative_path: str, content_hash: str
) -> list[LoadedDocument]:
    text = path.read_text(encoding="utf-8")
    title = _first_heading(text) or path.stem
    source = SourceDocument(source_id, relative_path, path.name, "markdown", content_hash, title)
    return [LoadedDocument(source, _normalize(text))]


def _load_pdf(
    path: Path, source_id: str, relative_path: str, content_hash: str
) -> list[LoadedDocument]:
    reader = PdfReader(str(path))
    documents: list[LoadedDocument] = []
    source = SourceDocument(source_id, relative_path, path.name, "pdf", content_hash, path.stem)
    for page_number, page in enumerate(reader.pages, start=1):
        text = _normalize(page.extract_text() or "")
        if text:
            documents.append(LoadedDocument(source, text, page_number))
    return documents


def _first_heading(text: str) -> str | None:
    match = re.search(r"^#{1,6}\s+(.+?)\s*$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def _section_for_text(full_text: str, text: str, default: str | None) -> str | None:
    position = full_text.find(text[:80])
    headings = list(re.finditer(r"^#{1,6}\s+(.+?)\s*$", full_text, re.MULTILINE))
    section = default
    for heading in headings:
        if heading.start() <= position:
            section = heading.group(1).strip()
        else:
            break
    return section


def _normalize(text: str) -> str:
    return re.sub(r"[ \t]+\n", "\n", re.sub(r"\n{3,}", "\n\n", text)).strip()


def _file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()
