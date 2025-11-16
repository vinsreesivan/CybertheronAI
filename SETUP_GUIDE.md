# Multi-LLM Fusion - Setup Guide

A unified interface to query multiple LLMs via Ollama and get an intelligently fused response.

## Features

- **Multi-Model Querying**: Query multiple LLMs (Llama, Gemma, Qwen, etc.) simultaneously
- **Parallel Processing**: All models queried in parallel for fast results
- **Intelligent Fusion**: Two fusion strategies:
  - **Refiner**: Uses an AI model to synthesize the best answer from all responses
  - **Consensus**: Simple voting/selection mechanism
- **Beautiful UI**: Modern, responsive web interface
- **Configurable**: Easy YAML configuration for models and settings
- **Real-time Feedback**: See individual model responses and fusion result

## Architecture

```
┌─────────────┐
│   Web UI    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  FastAPI    │
│   Backend   │
└──────┬──────┘
       │
       ▼
┌─────────────┐      ┌──────────┐
│ LLM Fusion  │─────▶│  Ollama  │
│   Engine    │      └──────────┘
└─────────────┘            │
                           ▼
                    ┌─────────────┐
                    │   Models:   │
                    │  - Llama    │
                    │  - Gemma    │
                    │  - Qwen     │
                    │  - etc.     │
                    └─────────────┘
```

## Prerequisites

1. **Python 3.8+**
2. **Ollama** - Install from https://ollama.com/download

## Quick Start

### Option 1: Automated Setup (Recommended)

```bash
# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

### Option 2: Manual Setup

#### Step 1: Install Ollama

```bash
# Linux/Mac
curl -fsSL https://ollama.com/install.sh | sh

# Or download from https://ollama.com/download
```

#### Step 2: Pull Models

```bash
# Pull the default models (this may take a while)
ollama pull llama3.2
ollama pull gemma2
ollama pull qwen2.5

# Optional: Pull additional models
ollama pull mistral
ollama pull codellama
```

#### Step 3: Install Python Dependencies

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

#### Step 4: Start the Server

```bash
python main.py
```

The server will start on `http://localhost:8000`

## Usage

1. Open your browser to `http://localhost:8000`
2. Enter your question or prompt
3. Select a fusion strategy:
   - **Refiner**: AI synthesizes the best answer (recommended)
   - **Consensus**: Returns the most detailed response
4. Click "Query All Models"
5. View individual responses and the refined fusion result

## Configuration

Edit `config.yaml` to customize:

```yaml
# Add/remove models
models:
  - name: "llama3.2"
    weight: 1.0
    enabled: true
  - name: "gemma2"
    weight: 1.0
    enabled: true
  - name: "mistral"      # Add new model
    weight: 1.0
    enabled: true

# Choose refiner model (your best model)
refiner_model: "llama3.2"

# Fusion strategy: "refiner" or "consensus"
fusion_strategy: "refiner"

# Generation parameters
generation:
  temperature: 0.7      # Creativity (0.0 - 1.0)
  max_tokens: 2000      # Max response length
  timeout: 60           # Timeout in seconds
```

## How Fusion Works

### Refiner Strategy (Default)

1. **Query Phase**: All enabled models are queried in parallel
2. **Collection Phase**: Individual responses are collected
3. **Refinement Phase**: The refiner model analyzes all responses and synthesizes a final answer by:
   - Identifying the most accurate information from each response
   - Combining best insights
   - Removing contradictions and redundancies
   - Producing a comprehensive, refined answer

### Consensus Strategy

1. **Query Phase**: All enabled models are queried in parallel
2. **Selection Phase**: The most detailed response is selected (based on length)
3. Returns that response as the final answer

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

### Main Endpoints

- `GET /` - Web UI
- `POST /query` - Query LLMs and get fused response
- `GET /health` - Health check
- `GET /config` - Get current configuration
- `GET /models` - List available models

### Example API Call

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain quantum computing in simple terms"}'
```

## Troubleshooting

### "Cannot connect to backend"

- Make sure the Python server is running: `python main.py`
- Check that port 8000 is not in use

### "All models failed to respond"

- Ensure Ollama is running: `ollama serve`
- Check that models are installed: `ollama list`
- Verify model names in `config.yaml` match installed models

### Models are slow

- Reduce `max_tokens` in `config.yaml`
- Use smaller/faster models
- Ensure your system has enough RAM/VRAM

### Out of memory

- Disable some models in `config.yaml` (set `enabled: false`)
- Use smaller models (e.g., `llama3.2:1b` instead of `llama3.2:70b`)
- Close other applications

## Adding New Models

1. Pull the model with Ollama:
   ```bash
   ollama pull <model-name>
   ```

2. Add to `config.yaml`:
   ```yaml
   models:
     - name: "<model-name>"
       weight: 1.0
       enabled: true
   ```

3. Restart the server

## Performance Tips

- **Parallel Processing**: All models query in parallel, so total time ≈ slowest model
- **Model Selection**: Use 2-4 diverse models for best fusion results
- **Refiner Model**: Choose your most capable model as the refiner
- **Temperature**: Lower (0.3-0.5) for factual questions, higher (0.7-0.9) for creative tasks

## Use Cases

- **Research**: Get diverse perspectives on complex topics
- **Coding**: Compare solutions from multiple models
- **Creative Writing**: Synthesize ideas from different models
- **Fact-Checking**: Cross-reference answers across models
- **Learning**: See how different models approach problems

## Project Structure

```
CybertheronAI/
├── main.py              # FastAPI server
├── llm_fusion.py        # Fusion engine logic
├── config.yaml          # Configuration
├── requirements.txt     # Python dependencies
├── setup.sh            # Setup script
├── ui/
│   └── index.html      # Web interface
└── docs/               # Documentation
```

## Advanced Usage

### Custom Fusion Strategy

You can implement your own fusion logic by modifying `llm_fusion.py`:

```python
async def custom_fusion(self, model_responses: List[ModelResponse]) -> str:
    # Your custom logic here
    pass
```

### API Integration

Use the API programmatically:

```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    json={
        "prompt": "Your question here",
        "strategy": "refiner"
    }
)

result = response.json()
print(result['fused_response'])
```

## Contributing

Feel free to:
- Add new fusion strategies
- Improve the UI
- Add model-specific optimizations
- Create plugins

## License

MIT License - Feel free to use and modify!

## Support

For issues or questions:
1. Check Ollama is running: `ollama serve`
2. Check models are installed: `ollama list`
3. Review server logs for errors
4. Ensure all dependencies are installed

---

**Enjoy your Multi-LLM Fusion Interface! 🚀**
