# BizIntel AI

BizIntel AI is a planned web-based business intelligence and decision-assistance platform for small and medium businesses. It will enable businesses to upload datasets and explore data quality, KPIs, analytics, visualizations, forecasting, anomaly detection, AI-generated insights, and natural-language questions.

## Development status

The project is in **Phase 1: foundation**. This phase provides Python packaging, a minimal FastAPI service, automated testing, linting, and repository conventions. Data processing, machine learning, AI, database, frontend, containers, cloud deployment, and CI/CD are intentionally out of scope for this phase.

## Planned architecture

The application will use a layered design:

- A FastAPI backend will expose HTTP APIs.
- Business and analytics logic will live independently of API routes.
- Data-processing and machine-learning components will be added in later phases.
- PostgreSQL will provide persistent storage in a later phase.
- A React or Next.js frontend will consume the backend APIs.

## Planned technology stack

- Backend: Python and FastAPI
- Data science: Pandas, NumPy, and scikit-learn
- Database: PostgreSQL
- Frontend: React or Next.js
- Visualization: Plotly
- Testing: Pytest
- Code quality: Ruff
- Delivery: Docker, GitHub Actions, and cloud hosting
- AI: an LLM API, followed by RAG in a later phase

## Development principles

- Build incrementally and validate each phase.
- Keep business logic separate from API and UI code.
- Use environment-based configuration; never commit credentials.
- Prefer simple, maintainable solutions with automated tests.
- Follow modern Python conventions, including type hints and PEP 8.

## Local development

Requires Python 3.11 or newer.

```bash
python -m pip install -e ".[dev]"
uvicorn bizintel.main:app --reload
```

The health endpoint is available at `GET /health`.

```bash
pytest
ruff check .
```

See [the architecture notes](docs/architecture.md) for the current project boundaries.
