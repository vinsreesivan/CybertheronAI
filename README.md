# 🤖 Multi-LLM Fusion Interface

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Required-orange.svg)](https://ollama.com/)

**Query multiple LLMs simultaneously and get an intelligently refined, fused response.**

## ✨ What is This?

This project provides a unified interface to interact with multiple Large Language Models (LLMs) through Ollama. Instead of querying models one by one, you can:

1. **Query multiple models in parallel** (Llama, Gemma, Qwen, Mistral, etc.)
2. **Compare their responses** side-by-side
3. **Get a refined, synthesized answer** that combines the best insights from all models

Perfect for research, coding, creative writing, or any task where diverse AI perspectives add value!

## 🎯 Key Features

- ⚡ **Parallel Processing** - Query all models simultaneously
- 🧠 **Intelligent Fusion** - AI-powered synthesis of responses
- 🎨 **Beautiful UI** - Modern, responsive web interface
- ⚙️ **Highly Configurable** - Easy YAML configuration
- 🔌 **REST API** - Full API for programmatic access
- 📊 **Response Analytics** - Compare individual model outputs

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com/download)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/vinsreesivan/CybertheronAI.git
cd CybertheronAI

# 2. Run automated setup
chmod +x setup.sh
./setup.sh

# 3. Start the server
./run.sh
```

That's it! Open `http://localhost:8000` in your browser.

## 📖 Usage

### Web Interface

1. Navigate to `http://localhost:8000`
2. Enter your question
3. Select fusion strategy (Refiner or Consensus)
4. Click "Query All Models"
5. View individual responses and refined result

### API Usage

```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    json={"prompt": "Explain quantum computing"}
)

result = response.json()
print(result['fused_response'])
```

### Command Line

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Your question here"}'
```

## 🔧 Configuration

Edit `config.yaml` to customize models and settings:

```yaml
models:
  - name: "llama3.2"
    weight: 1.0
    enabled: true
  - name: "gemma2"
    weight: 1.0
    enabled: true

refiner_model: "llama3.2"
fusion_strategy: "refiner"  # or "consensus"
```

## 📚 How It Works

### Refiner Strategy (Recommended)

```
User Question → [Llama3.2, Gemma2, Qwen2.5] → Individual Responses
                                              ↓
                                      Refiner Model analyzes
                                              ↓
                                    Synthesized Best Answer
```

The refiner model:
- Analyzes all responses
- Identifies most accurate information
- Combines best insights
- Removes contradictions
- Produces comprehensive answer

### Consensus Strategy

Selects the most detailed response based on content length.

## 📁 Project Structure

```
CybertheronAI/
├── main.py              # FastAPI server
├── llm_fusion.py        # Fusion engine
├── config.yaml          # Configuration
├── requirements.txt     # Dependencies
├── setup.sh            # Setup script
├── run.sh              # Run script
├── ui/
│   └── index.html      # Web interface
├── SETUP_GUIDE.md      # Detailed guide
└── docs/               # Additional docs
```

## 🎨 Screenshots

**Main Interface:**
- Clean, modern UI with gradient design
- Real-time model status
- Collapsible individual responses
- Performance metrics

## 💡 Use Cases

- **Research**: Get diverse perspectives on complex topics
- **Coding**: Compare coding solutions from multiple models
- **Writing**: Synthesize creative ideas
- **Fact-Checking**: Cross-reference answers
- **Learning**: See different problem-solving approaches

## 🛠️ Advanced Features

### Adding New Models

```bash
# Pull model
ollama pull mistral

# Add to config.yaml
models:
  - name: "mistral"
    enabled: true
```

### API Endpoints

- `GET /` - Web UI
- `POST /query` - Query and fuse
- `GET /health` - Health check
- `GET /config` - Current config
- `GET /models` - List models
- `GET /docs` - API documentation

## 🐛 Troubleshooting

**Server won't start:**
- Check Python version: `python3 --version`
- Ensure virtual environment is activated
- Check port 8000 is free

**Models not responding:**
- Verify Ollama is running: `ollama serve`
- List installed models: `ollama list`
- Check model names match config

**Out of memory:**
- Reduce enabled models
- Use smaller model variants
- Lower `max_tokens` in config

See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed troubleshooting.

## 📊 Performance

- **Parallel Queries**: Total time ≈ slowest model
- **Recommended**: 2-4 diverse models for optimal fusion
- **Best Models**: Use your most capable model as refiner

## 🤝 Contributing

Contributions welcome! Ideas:
- New fusion strategies
- UI improvements
- Model-specific optimizations
- Additional features

## 📄 License

MIT License - See LICENSE file

## 🙏 Acknowledgments

- [Ollama](https://ollama.com/) - Local LLM runtime
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- All the amazing open-source LLM projects

## 📞 Support

For detailed setup and usage instructions, see [SETUP_GUIDE.md](SETUP_GUIDE.md)

---

**Made with ❤️ for the AI community**