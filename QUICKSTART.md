# Quick Start Guide - Your Custom Setup

This guide is tailored for your specific Ollama setup (port 11502).

## Prerequisites Check

Your Ollama is already running with these models:
- ✅ llama3.2:3b
- ✅ qwen3:4b
- ✅ gemma3:12b (and others)

## Step-by-Step Instructions

### 1. Install Python Dependencies

```bash
# Navigate to project directory
cd /home/user/CybertheronAI

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Expected output:
```
Successfully installed fastapi-0.104.1 uvicorn-0.24.0 ollama-0.1.6 ...
```

### 2. Test Ollama Connection

```bash
# Check Ollama is accessible
curl http://localhost:11502/api/tags
```

You should see JSON output with your models.

### 3. Start the Server

**Option A: Simple start**
```bash
python main.py
```

**Option B: Using the run script**
```bash
./run.sh
```

Expected output:
```
INFO:     Started server process
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✅ **Server is now running!**

### 4. Quick Test

Open a **new terminal** and run:

```bash
./test_system.sh
```

This will:
- ✅ Check Ollama connection
- ✅ Verify models are available
- ✅ Test the server health
- ✅ Send a test query

### 5. Open Web Interface

Open your browser to:
```
http://localhost:8000
```

You should see the **Multi-LLM Fusion Interface**.

### 6. Try Your First Query

In the web interface:

1. **Enter a question**, for example:
   ```
   Explain what Python decorators are in simple terms
   ```

2. **Select strategy**: Keep "Refiner (AI-synthesized)"

3. **Click** "Query All Models"

4. **Wait** 10-20 seconds (3 models running in parallel)

5. **View results**:
   - Refined fusion result (synthesized answer)
   - Individual model responses (click "Show responses")
   - Performance metrics

## Testing Different Scenarios

### Test 1: General Question
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is machine learning?"}'
```

### Test 2: Coding Question (Switch to Coding Preset)
```bash
# Switch preset
./switch_preset.sh coding

# Restart server
# Ctrl+C to stop current server, then:
python main.py

# In another terminal, test:
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Write a Python function to reverse a linked list"}'
```

### Test 3: Security Question (Switch to Security Preset)
```bash
# Switch preset
./switch_preset.sh security

# Restart server
python main.py

# Test with security question:
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Explain common web application vulnerabilities"}'
```

### Test 4: Python API Usage
```bash
# Make sure server is running, then:
python example_usage.py
```

This will run multiple test queries and show results.

## Verification Checklist

Run through this checklist:

- [ ] Python virtual environment created and activated
- [ ] Dependencies installed successfully
- [ ] Ollama accessible on port 11502
- [ ] Server starts without errors
- [ ] Health check returns "healthy" status
- [ ] Test query completes successfully
- [ ] Web UI loads at http://localhost:8000
- [ ] Can submit query via web UI
- [ ] See fused response and individual responses
- [ ] Performance metrics display correctly

## Common Issues & Solutions

### Issue: "Connection refused" to Ollama
**Solution**:
```bash
# Check Ollama is running on correct port
OLLAMA_HOST=0.0.0.0:11502 ollama serve
```

### Issue: "Module not found"
**Solution**:
```bash
# Make sure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: "Port 8000 already in use"
**Solution**:
```bash
# Find what's using port 8000
lsof -i :8000

# Kill it or change port in config.yaml
# Then restart server
```

### Issue: Models are slow
**Solution**:
```bash
# Switch to speed preset (only 2 small models)
./switch_preset.sh speed
python main.py
```

### Issue: Out of memory
**Solution**:
Edit `config.yaml` and disable one model:
```yaml
- name: "gemma3:12b"
  enabled: false  # Disable this one
```

## Performance Expectations

With your current setup (llama3.2:3b, qwen3:4b, gemma3:12b):

- **Query Time**: 10-25 seconds
- **RAM Usage**: ~13 GB
- **Quality**: Very good (balanced)

## Next Steps

After testing:

1. **Try different presets**:
   - `./switch_preset.sh coding` - For programming questions
   - `./switch_preset.sh security` - For security analysis
   - `./switch_preset.sh quality` - For best results (slower)

2. **Customize config.yaml**:
   - Enable/disable models
   - Adjust temperature
   - Change refiner model

3. **Integrate into your workflow**:
   - Use the API programmatically
   - Create custom presets
   - Add your own models

## Monitoring

To monitor the server:

```bash
# In server terminal, you'll see logs like:
INFO:     Initialized LLM Fusion Engine with 3 models
INFO:     Querying llama3.2:3b...
INFO:     llama3.2:3b responded in 8.34s
INFO:     Running refiner model: gemma3:12b
```

## Stopping the Server

```bash
# Press Ctrl+C in the server terminal
^C
INFO:     Shutting down
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `source venv/bin/activate` | Activate Python environment |
| `python main.py` | Start server |
| `./test_system.sh` | Run quick tests |
| `./switch_preset.sh [name]` | Change model preset |
| `python example_usage.py` | Test Python API |
| `curl http://localhost:8000/health` | Check server health |
| `curl http://localhost:8000/docs` | View API documentation |

---

**You're all set! Start with `python main.py` and open http://localhost:8000** 🚀
