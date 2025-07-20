from mcp.server.fastmcp import FastMCP
from datetime import datetime


# Init MCP Server for project creation guidance
mcp = FastMCP(name="ProjectBuilderServer", instructions="Server to provide ML service creation guidelines and checklists")


@mcp.tool()
def service_creation_prompt():
    """
    Returns a standardized prompt for creating ML services with comprehensive guidelines and must-have checklist.
    
    Returns:
        str: A comprehensive guide for ML service creation with all must-have components.
    """
    today_date = datetime.now().strftime("%B %d, %Y")
    
    return f"""
# ML Service Must-Have Checklist - {today_date}

You are creating a new ML service project. Follow this comprehensive checklist to ensure all critical components are included:

## General Requirements
- [ ] FastAPI application using `async def`
- [ ] Minimum 4 workers (Gunicorn + Uvicorn worker)
- [ ] Docker + docker-compose setup
- [ ] Docker runs only on `127.0.0.1` (not `0.0.0.0`) for local safety
- [ ] ENV configuration via `.env` + Pydantic `BaseSettings`
- [ ] `.sh` script for quick local run (e.g., `run_local.sh`) of a simple example
- [ ] Minimal `README.md` with run instructions, curl example, input/output
- [ ] `.gitignore` includes `logs/`, `models/`, `.env`, `__pycache__/`, etc.
- [ ] Support for structured logging (JSON)
- [ ] Clear separation of development vs. production dependencies (requirements.txt / requirements-dev.txt or pyproject.toml)
- [ ] Version endpoint (/version) for easy identification of running model/service

## Model Management
- [ ] Heavy files (model, index, etc.) loaded once on startup
- [ ] Model readiness check endpoint (`/ready`)
- [ ] Service health check endpoint (`/health`)
- [ ] Asynchronous model initialization supported
- [ ] Graceful shutdown of resources/models (GPU-bound resources)
- [ ] Endpoint for retrieving model metadata (e.g., model version, date trained, hyperparameters)

## Recommended Project Structure
```plaintext
project/
├── src/
│   ├── api/              # FastAPI routes
│   ├── config/           # ENV and settings
│   ├── data/             # Input/output processing
│   │   ├── models/       # Model files (gitignored)
│   │   ├── datasets/     # Dataset files (gitignored)
│   ├── inference/        # Model and prediction logic
│   ├── utils/            # Utility and helper functions
│   ├── scripts/          # Utility scripts (e.g., model download, maintenance)
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

## Classical ML Model Training
- [ ] Train multiple candidate models (e.g., XGBoost, RandomForest, LightGBM) and select the best-performing model based on validation metrics
- [ ] Always perform probability calibration

## Dataset Handling
- [ ] Visualize dataset distributions to identify potential severe class imbalance
- [ ] Apply stratified splits (train/test/validation) to maintain class distributions, especially for imbalanced datasets

## Quality Metrics
- [ ] Essential Metrics for classification: Accuracy, Precision, Recall, F1-score, ROC-AUC
- [ ] Imbalanced Classification: PR-AUC as the primary metric
- [ ] LLM Cost Efficiency: Include cost calculation metrics when using external APIs: Input token num and costs, output token num and cost
- [ ] LLM Proprietary: Overall cost efficiency (metric_per_dollar)—evaluate performance per dollar spent
- [ ] Local Models: Calculate and document both accuracy and inference speed (ms/request, tokens/sec)

## Performance Metrics
- [ ] RPS (Requests Per Second)
- [ ] Latency
- [ ] Measure and separately report detailed timing within the prediction pipeline (i.e. preprocessing, embedding, model, post-processing, total time)
- [ ] Return detailed timing breakdown in the output JSON for each request

## Testing
- [ ] Unit test for at least one successful inference
- [ ] Input validation tests (e.g., empty, corrupted input)
- [ ] Load testing with Locust or K6
- [ ] Performance benchmarking guidelines or reports included

## Security & Stability
- [ ] Proper CORS policy
- [ ] Rate limiting (e.g., slowapi) — optional
- [ ] HTTPS-ready config for production use
- [ ] Ability to disable graphical/statistical tools via ENV
- [ ] Logging only enabled in debug/dev mode

## DevOps & Automation
- [ ] pre-commit hooks (black, isort, flake8)
- [ ] CI/CD pipeline with linting, tests, Docker build (GitHub Actions or GitLab CI)
- [ ] Optional: Prometheus, OpenTelemetry, or FastAPI Instrumentator

---

## Implementation Guidelines:

1. **Start with the project structure** - Create all necessary directories first
2. **Set up FastAPI with async endpoints** - Use proper async/await patterns
3. **Implement health and readiness checks early** - Essential for monitoring
4. **Add proper logging from the beginning** - Structured JSON logging is preferred
5. **Use Pydantic for all data validation** - Input/output schemas and configuration
6. **Containerize early** - Docker setup should be one of the first steps
7. **Add tests as you develop** - Don't leave testing until the end
8. **Document as you go** - README with examples and API documentation

**Remember**: This checklist ensures production-ready, maintainable, and scalable ML services. Each item addresses common pitfalls and best practices learned from production deployments.

---

## Agent Development Recommendations:

### For AI Agents Using This Checklist:

**Phase-Based Development Approach:**

1. **Foundation Phase** (Essential First Steps):
   - Create project directory structure first
   - Set up basic FastAPI app with health endpoints (`/health`, `/ready`, `/version`)
   - Initialize Docker configuration (Dockerfile + docker-compose.yml)
   - Create basic `.env` configuration with Pydantic BaseSettings
   - Set up `.gitignore` with all necessary exclusions
   - **Checkpoint**: Verify the service starts and responds to health checks

2. **Core Implementation Phase**:
   - Implement main API endpoints with Pydantic validation
   - Add model loading and inference logic
   - Implement proper error handling and JSON responses
   - Add structured logging (JSON format)
   - **Checkpoint**: Basic functionality works end-to-end

3. **Production Readiness Phase**:
   - Add comprehensive testing (unit tests, input validation tests)
   - Implement proper async patterns throughout
   - Add performance monitoring and timing breakdowns
   - Configure proper worker setup (Gunicorn + Uvicorn)
   - **Checkpoint**: Service passes all tests and handles load

4. **Quality & Security Phase**:
   - Implement security measures (CORS, rate limiting)
   - Add model metadata endpoints
   - Set up CI/CD pipeline with linting and tests
   - Add load testing configuration
   - **Checkpoint**: Production-ready deployment

### Implementation Strategy for Agents:

**Required Actions:**
- Follow the phases sequentially - do not skip foundation steps
- Test each checkpoint before moving to the next phase
- Create working examples and curl commands in README
- Use async/await patterns consistently from the start
- Implement proper graceful shutdown for resources
- Add timing breakdowns to all responses for performance monitoring
- Use Pydantic for ALL data validation (input, output, config)
- Create a simple `run_local.sh` script for easy testing
- Keep documentation minimal and focused on essentials only

**Actions to Avoid:**
- Do not skip the project structure setup - it is foundational
- Do not ignore health/ready endpoints - they are critical for deployment
- Do not use blocking I/O operations in async endpoints
- Do not expose Docker on 0.0.0.0 for local development
- Do not skip input validation - always use Pydantic models
- Do not omit proper error handling with JSON responses
- Do not defer testing - implement as you build, not at the end
- Do not create excessive documentation - keep it concise and practical

### Agent Execution Protocol:

**For each item in the checklist:**
1. **Read the requirement carefully** - understand what needs to be implemented
2. **Check dependencies** - ensure prerequisite items are completed
3. **Implement with examples** - always include working examples
4. **Test immediately** - verify functionality before moving on
5. **Document the implementation** - update README with usage examples

### Development Order Priority:

**Critical Path (Must implement first):**
1. Project structure → FastAPI app → Health endpoints → Docker setup
2. Basic model loading → Simple inference endpoint → Pydantic validation
3. Error handling → Logging → Testing setup

**Parallel Development (Can implement simultaneously):**
- Minimal documentation and working examples
- Additional endpoints and features
- Performance optimizations
- Security enhancements

### Initial Setup Commands for Agents:

```bash
# Agent should execute these commands to initialize the project:
mkdir -p project_name/{src/{api,config,data/{models,datasets},inference,utils,scripts},tests,logs,notebooks}
cd project_name
touch src/main.py src/api/__init__.py src/config/__init__.py
touch Dockerfile docker-compose.yml requirements.txt .env .gitignore README.md
touch run_local.sh && chmod +x run_local.sh
```

**Success Criteria**: After following this checklist, the agent should produce a service that:
- Starts successfully with `./run_local.sh`
- Responds to health checks within 100ms
- Has working inference endpoint with example curl command
- Passes all implemented tests
- Is ready for containerized deployment

### Documentation Guidelines for Agents:

**Minimal Documentation Requirements** - Only create the following documentation:

1. **README.md** should contain ONLY:
   - Brief description (2-3 sentences maximum)
   - Project structure overview
   - Input/output examples with curl commands
   - How to run instructions (`./run_local.sh`)
   - No extensive explanations or theory

2. **API Documentation**:
   - Use FastAPI's automatic documentation (Swagger UI)
   - Add concise docstrings to endpoints (1-2 lines maximum)
   - Include example request/response in Pydantic models

3. **Code Comments**:
   - Only comment complex business logic
   - Avoid obvious comments
   - Focus on "why" not "what"

**Do NOT create**:
- Extensive markdown files
- Architecture diagrams
- Detailed API documentation beyond FastAPI's auto-generated docs
- Deployment guides beyond basic run instructions
- Theory or background explanations

**Important Note**: The objective is not merely to complete checklist items, but to create a robust, maintainable service that follows production best practices. Each item in this checklist addresses real-world deployment challenges and operational requirements. Keep documentation minimal and action-oriented.
"""


if __name__ == "__main__":
    # Example usage
    print(service_creation_prompt()) 