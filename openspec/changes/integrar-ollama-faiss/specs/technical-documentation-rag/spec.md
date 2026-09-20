# Spec Delta

## MODIFIED Requirements

### Requirement: The system SHALL maintain a reproducible local document index

The system SHALL create a persistent local index for the configured corpus and SHALL associate it with the exact embedding provider, embedding model, embedding dimensions, distance strategy, corpus identity, and ingestion version used to build it.

#### Scenario: The corpus has not changed
- **WHEN** the application starts and the persisted index manifest matches the current corpus and embedding configuration
- **THEN** the system reuses the index without creating duplicate document chunks or contacting a paid provider when a local provider is configured

#### Scenario: The embedding configuration has changed
- **WHEN** the application starts or an index operation detects that the persisted embedding provider, model, dimensions, or distance strategy differs from the current configuration
- **THEN** the system removes the incompatible FAISS snapshot and rebuilds it from the current corpus and embedding configuration before serving retrieval requests

#### Scenario: The corpus or embedding configuration has changed
- **WHEN** an authorized rebuild is requested or the persisted manifest is incompatible with the current corpus or ingestion version
- **THEN** the system rebuilds the index explicitly and reports the resulting indexed, skipped, and failed files

#### Scenario: The index rebuild fails
- **WHEN** automatic or explicit rebuilding cannot create a valid complete snapshot
- **THEN** the system reports an actionable safe error and does not serve retrieval results from the incompatible or partial snapshot

## ADDED Requirements

### Requirement: The system SHALL support configurable local chat and embedding providers

The system SHALL allow the chat model and embedding model to be configured independently, including a local Ollama chat provider and a local embedding provider that operate without an OpenAI API key. Provider failures and missing local runtime prerequisites SHALL be reported without exposing credentials, prompts, or stack traces.

#### Scenario: Local providers are configured
- **WHEN** the configured chat provider is Ollama and the configured embedding provider is local
- **THEN** the system constructs both clients from the configured model identities and does not require `OPENAI_API_KEY`

#### Scenario: An explicitly configured OpenAI provider is used
- **WHEN** both providers are configured for OpenAI and a valid OpenAI credential is available
- **THEN** the system continues to construct and use the OpenAI clients with the existing grounded-answer behavior

#### Scenario: A local provider is unavailable
- **WHEN** Ollama is not running, a local model is unavailable, or a local embedding dependency cannot be loaded
- **THEN** the system displays an actionable configuration or provider error and does not expose internal exception details
