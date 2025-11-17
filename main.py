"""
Multi-LLM Fusion API Server
FastAPI backend for the LLM Fusion UI
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import yaml
import logging
from pathlib import Path
import asyncio
import re
from llm_fusion import LLMFusionEngine
from code_executor import CodeExecutor, CodeExecutionResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
config_path = Path("config.yaml")
if not config_path.exists():
    raise FileNotFoundError("config.yaml not found!")

with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Initialize FastAPI
app = FastAPI(
    title="Multi-LLM Fusion API",
    description="Query multiple LLMs and get a refined, fused response",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize fusion engine and code executor
fusion_engine = LLMFusionEngine(config)
code_executor = CodeExecutor(timeout=30)


# Request/Response models
class QueryRequest(BaseModel):
    prompt: str
    strategy: str = None  # Optional override of default strategy


class CodeExecutionRequest(BaseModel):
    code: str
    auto_fix: bool = False  # If True, automatically fix errors without asking
    max_iterations: int = 5  # Maximum number of fix attempts


class HealthResponse(BaseModel):
    status: str
    models: list
    fusion_strategy: str


@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main UI"""
    ui_path = Path("ui/index.html")
    if ui_path.exists():
        return FileResponse(ui_path)
    return """
    <html>
        <body>
            <h1>Multi-LLM Fusion API</h1>
            <p>API is running. Visit /docs for API documentation.</p>
            <p>UI not found at ui/index.html</p>
        </body>
    </html>
    """


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models": [m['name'] for m in config['models'] if m.get('enabled', True)],
        "fusion_strategy": config.get('fusion_strategy', 'refiner')
    }


@app.get("/config")
async def get_config():
    """Get current configuration"""
    return {
        "models": config['models'],
        "refiner_model": config.get('refiner_model'),
        "fusion_strategy": config.get('fusion_strategy'),
        "generation": config.get('generation', {})
    }


@app.post("/query")
async def query_llms(request: QueryRequest):
    """
    Main endpoint: Query multiple LLMs and return fused response
    """
    if not request.prompt or len(request.prompt.strip()) == 0:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    try:
        # Override strategy if provided
        if request.strategy:
            original_strategy = fusion_engine.fusion_strategy
            fusion_engine.fusion_strategy = request.strategy

        result = await fusion_engine.fuse_responses(request.prompt)

        # Restore original strategy
        if request.strategy:
            fusion_engine.fusion_strategy = original_strategy

        return result

    except Exception as e:
        logger.error(f"Query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


@app.get("/models")
async def list_models():
    """List all available models"""
    try:
        # Get list of available models from Ollama
        models_info = []
        for model in config['models']:
            models_info.append({
                "name": model['name'],
                "enabled": model.get('enabled', True),
                "weight": model.get('weight', 1.0)
            })
        return {"models": models_info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list models: {str(e)}")


def extract_code_from_response(response: str) -> str:
    """Extract Python code from LLM response"""
    # Try to find code blocks
    code_block_pattern = r'```python\s*(.*?)\s*```'
    matches = re.findall(code_block_pattern, response, re.DOTALL)

    if matches:
        return matches[0].strip()

    # Try generic code blocks
    code_block_pattern = r'```\s*(.*?)\s*```'
    matches = re.findall(code_block_pattern, response, re.DOTALL)

    if matches:
        return matches[0].strip()

    # If no code blocks, return the whole response stripped
    return response.strip()


@app.post("/execute")
async def execute_code(request: CodeExecutionRequest):
    """
    Execute Python code with automatic error fixing via LLM fusion

    This endpoint:
    1. Executes the provided code
    2. If there's an error, uses LLM fusion to fix it
    3. Optionally loops until code succeeds or max iterations reached
    """
    if not request.code or len(request.code.strip()) == 0:
        raise HTTPException(status_code=400, detail="Code cannot be empty")

    try:
        iterations = []
        current_code = request.code
        iteration = 0

        while iteration < request.max_iterations:
            iteration += 1

            # Execute code
            result = code_executor.execute(current_code, use_subprocess=True)

            iteration_data = {
                "iteration": iteration,
                "code": current_code,
                "success": result.success,
                "output": result.output,
                "error": result.error,
                "error_type": result.error_type
            }

            iterations.append(iteration_data)

            if result.success:
                # Code succeeded!
                return {
                    "success": True,
                    "iterations": iterations,
                    "final_code": current_code,
                    "output": result.output
                }

            # Code failed - try to fix with LLM
            if iteration >= request.max_iterations:
                # Max iterations reached
                return {
                    "success": False,
                    "iterations": iterations,
                    "final_code": current_code,
                    "error": "Maximum iterations reached without success"
                }

            # Get LLM to fix the code
            prompt = result.get_error_prompt()
            fusion_result = await fusion_engine.fuse_responses(prompt)

            fixed_code = extract_code_from_response(fusion_result['fused_response'])

            if not fixed_code:
                # LLM couldn't generate a fix
                return {
                    "success": False,
                    "iterations": iterations,
                    "final_code": current_code,
                    "error": "LLMs could not generate a fix"
                }

            # Store the proposed fix
            iteration_data["proposed_fix"] = fixed_code
            iteration_data["llm_analysis"] = fusion_result['fused_response']

            # Use fixed code for next iteration
            current_code = fixed_code

        # Should not reach here, but just in case
        return {
            "success": False,
            "iterations": iterations,
            "final_code": current_code,
            "error": "Maximum iterations reached"
        }

    except Exception as e:
        logger.error(f"Code execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")


@app.get("/code-editor", response_class=HTMLResponse)
async def code_editor():
    """Serve the code editor UI"""
    editor_path = Path("ui/code_editor.html")
    if editor_path.exists():
        return FileResponse(editor_path)
    raise HTTPException(status_code=404, detail="Code editor not found")


if __name__ == "__main__":
    import uvicorn

    server_config = config.get('server', {})
    host = server_config.get('host', '0.0.0.0')
    port = server_config.get('port', 8000)

    logger.info(f"Starting Multi-LLM Fusion Server on {host}:{port}")
    logger.info(f"Enabled models: {[m['name'] for m in config['models'] if m.get('enabled', True)]}")

    uvicorn.run(app, host=host, port=port)
