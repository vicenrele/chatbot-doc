# Spec Delta

## Purpose

This capability provides a local technical-documentation assistant that answers questions from a controlled corpus and makes the supporting documentation visible to users.

## ADDED Requirements

### Requirement: The system SHALL ingest supported technical documents

The system SHALL accept Markdown and PDF files, validate their type, size, readability, and extracted content, and report per-file success or failure without exposing internal errors or secrets.

#### Scenario: Valid Markdown and PDF files are ingested
- **WHEN** an authorized ingestion operation receives readable Markdown and PDF files within configured limits
- **THEN** the system indexes their normalized content and preserves source filename, relative path, title or section, and page metadata when available

#### Scenario: An unsupported or invalid file is received
- **WHEN** an ingestion operation receives an unsupported, oversized, unreadable, or empty file
- **THEN** the system skips that file, reports an actionable validation result, and does not add partial or unsafe content to the corpus

### Requirement: The system SHALL maintain a reproducible local document index

The system SHALL create a persistent local index for the configured corpus and SHALL associate it with the exact embedding configuration, corpus identity, and ingestion version used to build it.

#### Scenario: The corpus has not changed
- **WHEN** the application starts and the persisted index manifest matches the current corpus and embedding configuration
- **THEN** the system reuses the index without creating duplicate document chunks

#### Scenario: The corpus or embedding configuration has changed
- **WHEN** an authorized rebuild is requested or the persisted manifest is incompatible with the current configuration
- **THEN** the system rebuilds the index explicitly and reports the resulting indexed, skipped, and failed files

### Requirement: The system SHALL answer questions using retrieved documentation evidence

The system SHALL retrieve relevant document chunks, preserve their source metadata, and generate answers grounded only in the retrieved evidence.

#### Scenario: Relevant evidence is available
- **WHEN** a user submits a question with matching documentation in the current index
- **THEN** the system returns an answer with citations that map to real indexed chunks and include useful filename, section, or page information

#### Scenario: The index is empty or evidence is insufficient
- **WHEN** a user submits a question and no relevant indexed evidence meets the configured retrieval criteria
- **THEN** the system states that the documentation is insufficient and does not present an unsupported answer as authoritative

#### Scenario: Source content contains instructions unrelated to retrieval
- **WHEN** retrieved documentation includes text that attempts to override the assistant's behavior
- **THEN** the system treats that text as evidence only and continues to follow the application's grounding and safety rules

### Requirement: The system SHALL provide a safe Streamlit documentation chat

The system SHALL show index availability, ingestion or rebuild status, conversation messages, loading and error states, and source citations while keeping business logic independently testable outside Streamlit.

#### Scenario: A user submits a question with a usable index
- **WHEN** the user submits a non-empty question while the index is available
- **THEN** the interface displays the grounded answer and expandable or otherwise readable source details

#### Scenario: A user submits a question without a usable index
- **WHEN** the user submits a question before a compatible index is available
- **THEN** the interface explains that documents must be indexed before questions can be answered and does not call the generation model

#### Scenario: The model or provider fails
- **WHEN** retrieval or generation encounters a timeout, configuration error, or provider failure
- **THEN** the interface displays a safe actionable message and does not expose credentials, prompts, stack traces, or internal filesystem paths