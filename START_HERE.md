# 🚀 CybertheronAI - Quick Start

**Multi-LLM Fusion with Auto-Debug Code Execution**

## ⚡ One Command Start

```bash
./start.sh
```

Then open: **http://localhost:9876**

---

## 📍 Access Points

| Feature | URL |
|---------|-----|
| **Multi-LLM Fusion** | http://localhost:9876 |
| **Auto-Debug Editor** | http://localhost:9876/code-editor |
| **API Documentation** | http://localhost:9876/docs |

## 🤖 Active Models

This system uses **4 powerful models** running in parallel:

1. **llama3.2:3b** - Fast general model
2. **qwen3:4b** - Quick reasoning
3. **gemma3:12b** - Balanced quality (refiner)
4. **gpt-oss:20b** - Large capability model

## 🎯 What Can You Do?

### 1. Multi-LLM Fusion (Main UI)
Query multiple LLMs at once and get a refined, synthesized answer.

**Example:**
```
Q: "Explain quantum computing in simple terms"
→ 4 models respond independently
→ Refiner synthesizes best answer
```

### 2. Auto-Debug Code Execution
Write Python code with errors and let the LLMs fix them automatically!

**Example:**
```python
x = 10 / 0  # Error!
```
→ LLMs detect error
→ Propose fix
→ Auto re-run until success ✅

---

## 📖 Setup (First Time Only)

```bash
# 1. Clone repository
git clone https://github.com/vinsreesivan/CybertheronAI.git
cd CybertheronAI

# 2. Pull latest changes
git pull

# 3. Setup (installs dependencies)
./setup_simple.sh

# 4. Start
./start.sh
```

---

## 🛠️ Requirements

- **Python 3.9+** (tested with 3.13)
- **Ollama** running on port 11502
- **Models installed**: llama3.2:3b, qwen3:4b, gemma3:12b, gpt-oss:20b

### Check Ollama

```bash
curl http://localhost:11502/api/tags
```

If Ollama is not running:
```bash
OLLAMA_HOST=0.0.0.0:11502 ollama serve
```

---

## 💻 Terminal Auto-Debug Mode

For command-line code debugging:

```bash
# Interactive mode
python auto_debug.py

# Run a file with auto-fix
python auto_debug.py script.py --auto
```

---

## ⚙️ Configuration

Edit `config.yaml` to:
- Enable/disable models
- Change refiner model
- Adjust temperature and max tokens
- Switch fusion strategy

### Quick Preset Switching

```bash
# For coding tasks
./switch_preset.sh coding

# For security analysis
./switch_preset.sh security

# Maximum quality (slower)
./switch_preset.sh quality
```

---

## 🔧 Troubleshooting

### Server won't start
```bash
# Check Python environment
source venv/bin/activate
python --version
```

### Ollama connection error
```bash
# Verify Ollama is running
curl http://localhost:11502/api/tags

# Start Ollama if needed
OLLAMA_HOST=0.0.0.0:11502 ollama serve
```

### Port 9876 already in use
```bash
# Find what's using the port
lsof -i :9876

# Or change port in config.yaml
```

### Models are slow
```bash
# Use speed preset (only 2 models)
./switch_preset.sh speed
```

---

## 📚 Documentation

- **START_HERE.md** - This file (quick start)
- **README.md** - Full project overview
- **QUICKSTART.md** - Detailed setup guide
- **AUTO_DEBUG_GUIDE.md** - Auto-debug documentation
- **CONFIG_PRESETS.md** - Model configuration presets
- **TESTING_GUIDE.md** - Testing procedures

---

## 🎓 Examples

### Example 1: Get diverse perspectives
**Web UI** → http://localhost:9876
```
Query: "What are the pros and cons of microservices architecture?"
```

### Example 2: Auto-fix buggy code
**Code Editor** → http://localhost:9876/code-editor
```python
def average(numbers):
    return sum(numbers) / len(numbers)

print(average([]))  # Error! LLMs will fix this
```

### Example 3: API Usage
```bash
curl -X POST http://localhost:9876/query \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain recursion"}'
```

---

## 🎯 Key Features

✅ **Parallel LLM Querying** - All models run simultaneously
✅ **Intelligent Fusion** - Best insights from all models
✅ **Auto Code Debugging** - Automatic error detection & fixing
✅ **Interactive Terminal** - Color-coded CLI interface
✅ **Modern Web UI** - Beautiful, responsive interface
✅ **REST API** - Full programmatic access
✅ **Configurable Presets** - Easy model switching

---

## 🚦 Status Check

After starting the server, verify everything is working:

```bash
# Health check
curl http://localhost:9876/health

# List active models
curl http://localhost:9876/models
```

---

## ⚡ Quick Commands

| Command | Purpose |
|---------|---------|
| `./start.sh` | Start the server |
| `./setup_simple.sh` | Install dependencies |
| `./test_system.sh` | Run system tests |
| `python auto_debug.py` | Terminal auto-debug |
| `./switch_preset.sh [name]` | Change model preset |

---

## 🌐 Network Access

The server runs on `0.0.0.0:9876`, meaning:
- **Local access**: http://localhost:9876
- **Network access**: http://YOUR_IP:9876

To restrict to localhost only, edit `config.yaml`:
```yaml
server:
  host: "127.0.0.1"  # localhost only
```

---

## 📊 Performance

**Typical Response Times:**
- Single LLM query: 5-15 seconds
- Multi-LLM fusion: 10-30 seconds
- Auto-debug iteration: 15-35 seconds

**With 4 models active:**
- Parallel queries ≈ time of slowest model
- Total RAM usage: ~25-30 GB

---

## 💡 Tips

1. **Start Simple**: Try the web UI first
2. **Patience**: LLM fusion takes 10-30 seconds
3. **Experiments**: Use auto-debug for rapid prototyping
4. **Presets**: Switch models based on task type
5. **Iterations**: Complex bugs may need 2-3 fix attempts

---

## 📞 Support

For detailed guides, see:
- `README.md` - Full documentation
- `AUTO_DEBUG_GUIDE.md` - Auto-debug features
- `SETUP_GUIDE.md` - Installation help

---

**Made with ❤️ for AI experimentation and rapid development**

**Port: 9876** | **Ollama: 11502** | **Models: 4**
