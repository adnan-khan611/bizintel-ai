# Architecture notes

## Phase 1 scope

The service currently contains only a FastAPI application and its health endpoint. The `src/bizintel` package is the application boundary, while `tests` holds automated checks.

## Deferred components

The following are deliberately deferred to later phases: data ingestion, analytics, machine learning, LLM integration, database persistence, user interface, authentication, containerization, CI/CD, and cloud deployment.

When these components are introduced, domain and analytics logic should remain independent of HTTP route handlers.
