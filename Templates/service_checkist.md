# ML Service Must-Have Checklist

## General
- [ ] FastAPI application using `async def`
- [ ] Minimum 4 workers (Gunicorn + Uvicorn worker)
- [ ] Docker + docker-compose setup
- [ ] Docker runs only on `127.0.0.1` (not `0.0.0.0`) for local safety
- [ ] ENV configuration via `.env` + Pydantic `BaseSettings`
- [ ] `.sh` script for quick local run (e.g., `run_local.sh`) of a simple example
- [ ] Minimal `README.md` with run instructions, curl example, input/output
- [ ] `.gitignore` includes `logs/`, `models/`, `.env`, `__pycache__/`, etc.
- [ ]  Support for structured logging (JSON))
- [ ]  Clear separation of development vs. production dependencies (requirements.txt / requirements-dev.txt or pyproject.toml)
- [ ]  Version endpoint (/version) for easy identification of running model/service

---

## Model Management
- [ ] Heavy files (model, index, etc.) loaded once on startup
- [ ] Model readiness check endpoint (`/ready`)
- [ ] Service health check endpoint (`/health`)
- [ ] Asynchronous model initialization supported
- [ ] Graceful shutdown of resources/models (GPU-bound resources)
- [ ] Endpoint for retrieving model metadata (e.g., model version, date trained, hyperparameters)

---

## Project Structure
```plaintext
project/
├── src/
│   ├── api/              # FastAPI routes
│   ├── config/           # ENV and settings
│   ├── data/             # Input/output processing
|   |   ├── models/        # Model files (gitignored)
|   |   ├── datasets/        # Dataset files (gitignored)
│   ├── inference/        # Model and prediction logic
│   ├── utils/            # Utility and helper functions
|   ├── scripts/          # Utility scripts (e.g., model download, maintenance)
│   └── main.py           # FastAPI entrypoint
├── logs/                 # Logs and saved outputs (gitignored)
├── tests/                # Unit and integration tests
├── notebooks/            # Jupyter notebooks (optional)
├── run_local.sh          # Quick launch script
├── Dockerfile
├── docker-compose.yml
├── requirements.txt      # Dependencies
├── requirements-dev.txt  # Development-only dependencies
├── .env
├── .dockerignore
└── README.md

```

## Data Handling
- [ ] Input validation via Pydantic  
- [ ] Error handling with readable JSON responses  
- [ ] Logging of input/output can be disabled via ENV flag  
- [ ] Output must be JSON-serializable  
- [ ] Multipart/form support for images/files
- [ ] Clearly defined response schemas (Pydantic response models)
- [ ] Optional input size limitations or validations (e.g., file-size limit, dimensions)

---

## Classical ML Model Training
- [ ] Train multiple candidate models (e.g., XGBoost, RandomForest, LightGBM) and select the best-performing model based on validation metrics.
- [ ] Always perform probability calibration

---

## Dataset Handling
- [ ] Visualize dataset distributions to identify potential severe class imbalance.
- [ ] Apply stratified splits (train/test/validation) to maintain class distributions, especially for imbalanced datasets.

---

## Dataset Handling
- [ ] Visualize dataset distributions to identify potential severe class imbalance.
- [ ] Apply stratified splits (train/test/validation) to maintain class distributions, especially for imbalanced datasets.

---

## Quality Metrics
- [ ] Essential Metrics for classification: Accuracy, Precision, Recall, F1-score, ROC-AUC.
- [ ] Imbalanced Classification: PR-AUC as the primary metric.
- [ ] LLM Cost Efficiency: Include cost calculation metrics when using external APIs: Input token num and costs, output token num and cost
- [ ] LLM Proprietary: Overall cost efficiency (metric_per_dollar)—evaluate performance per dollar spent.
- [ ]  Local Models: Calculate and document both accuracy and inference speed (ms/request, tokens/sec).

---

## Performance Metrics
- [ ] RPS
- [ ] Latency
- [ ] Measure and separately report detailed timing within the prediction pipeline (i.e. preprocessing, emb, model, post-processing, total time)
- [ ]  Return detailed timing breakdown in the output JSON for each request.

---

## Testing
- [ ] Unit test for at least one successful inference  
- [ ] Input validation tests (e.g., empty, corrupted input)  
- [ ] Load testing with Locust or K6
- [ ]  Performance benchmarking guidelines or reports included

---

##  Security & Stability
- [ ] Proper CORS policy  
- [ ] Rate limiting (e.g., slowapi) — optional  
- [ ] HTTPS-ready config for production use  
- [ ] Ability to disable graphical/statistical tools via ENV  
- [ ] Logging only enabled in debug/dev mode  

---

## DevOps & Automation
- [ ] pre-commit hooks (black, isort, flake8)  
- [ ] CI/CD pipeline with linting, tests, Docker build (GitHub Actions or GitLab CI)  
- [ ] Optional: Prometheus, OpenTelemetry, or FastAPI Instrumentator  
