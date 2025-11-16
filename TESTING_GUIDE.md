# Testing Guide

This guide helps you test the Multi-LLM Fusion system to ensure everything works correctly.

## Prerequisites

Before testing, ensure:

1. ✅ Ollama is installed and running
2. ✅ Required models are pulled
3. ✅ Python dependencies are installed
4. ✅ Server is running on port 8000

## Quick Test

```bash
# 1. Start Ollama (if not already running)
ollama serve

# 2. In another terminal, start the server
source venv/bin/activate
python main.py

# 3. In another terminal, run the example script
source venv/bin/activate
python example_usage.py
```

## Manual Testing Steps

### Step 1: Verify Ollama Setup

```bash
# Check Ollama is running
ollama list

# You should see your models:
# NAME            SIZE     MODIFIED
# llama3.2:latest 2.0 GB   X days ago
# gemma2:latest   1.6 GB   X days ago
# qwen2.5:latest  1.9 GB   X days ago
```

If models are missing:

```bash
ollama pull llama3.2
ollama pull gemma2
ollama pull qwen2.5
```

### Step 2: Test Server Startup

```bash
# Activate virtual environment
source venv/bin/activate

# Start server
python main.py
```

Expected output:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Test Health Endpoint

In a new terminal:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "models": ["llama3.2", "gemma2", "qwen2.5"],
  "fusion_strategy": "refiner"
}
```

### Step 4: Test Configuration Endpoint

```bash
curl http://localhost:8000/config
```

Should return your configuration from `config.yaml`.

### Step 5: Test Simple Query

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is 2+2?"}'
```

This should return a JSON response with:
- `fused_response`: The synthesized answer
- `individual_responses`: Responses from each model
- `total_time`: Time taken
- `successful_responses`: Number of successful queries

### Step 6: Test Web UI

1. Open browser to `http://localhost:8000`
2. You should see the Multi-LLM Fusion Interface
3. Enter a test question: "Explain what Python is in one sentence"
4. Click "Query All Models"
5. Wait for responses
6. Verify you see:
   - Refined fusion result
   - Individual model responses (when expanded)
   - Performance metrics

### Step 7: Test Both Fusion Strategies

**Test Refiner Strategy:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Compare Python and JavaScript", "strategy": "refiner"}'
```

**Test Consensus Strategy:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Compare Python and JavaScript", "strategy": "consensus"}'
```

Compare the results - refiner should be more synthesized.

## Automated Testing

Run the example script:

```bash
python example_usage.py
```

This script tests:
- ✅ Health check
- ✅ Model listing
- ✅ Refiner strategy query
- ✅ Consensus strategy query
- ✅ Response parsing

## Performance Testing

### Test 1: Response Time

```bash
time curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is machine learning?"}'
```

Expected: 5-30 seconds depending on your hardware and models.

### Test 2: Parallel Execution

The individual responses should show similar timestamps, proving parallel execution.

Check the `time_taken` field in individual responses - they should be similar, not sequential.

### Test 3: Load Test (Optional)

```bash
# Install Apache Bench
sudo apt-get install apache2-utils  # Ubuntu/Debian

# Run 10 requests
ab -n 10 -c 1 -p query.json -T application/json http://localhost:8000/query

# query.json contains:
# {"prompt": "Test question"}
```

## Error Testing

### Test 1: Invalid Model

Edit `config.yaml`, add a non-existent model:

```yaml
models:
  - name: "nonexistent-model"
    enabled: true
```

Restart server and query. You should see errors for that model but success for others.

### Test 2: Empty Prompt

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"prompt": ""}'
```

Expected: HTTP 400 error with message "Prompt cannot be empty"

### Test 3: Ollama Not Running

1. Stop Ollama: `pkill ollama`
2. Try a query
3. Expected: All models should fail with connection errors

Restart Ollama: `ollama serve`

## Configuration Testing

### Test Different Models

1. Edit `config.yaml`
2. Disable one model:
   ```yaml
   - name: "gemma2"
     enabled: false
   ```
3. Restart server
4. Query - should only use 2 models

### Test Different Parameters

Edit `config.yaml`:

```yaml
generation:
  temperature: 0.3  # Lower = more focused
  max_tokens: 500   # Shorter responses
```

Restart and test - responses should be shorter and more focused.

## Common Issues

### Issue: "Connection refused"
**Solution**: Start the server with `python main.py`

### Issue: "All models failed"
**Solution**: Check Ollama is running with `pgrep ollama`

### Issue: Slow responses
**Solution**:
- Use smaller models (e.g., `llama3.2:1b`)
- Reduce `max_tokens` in config
- Disable some models

### Issue: Out of memory
**Solution**:
- Reduce number of enabled models
- Use quantized models
- Increase system RAM/swap

## API Documentation

Full interactive API docs available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Validation Checklist

Before deploying or sharing, verify:

- [ ] Health endpoint returns "healthy"
- [ ] All configured models respond
- [ ] Refiner strategy works
- [ ] Consensus strategy works
- [ ] Web UI loads and functions
- [ ] Individual responses display
- [ ] Performance metrics show
- [ ] Error handling works
- [ ] Configuration changes apply
- [ ] Example script runs successfully

## Next Steps

After successful testing:

1. **Customize**: Adjust models and settings for your use case
2. **Optimize**: Tune parameters for best performance
3. **Deploy**: Consider production deployment options
4. **Integrate**: Use the API in your applications

## Getting Help

If tests fail:

1. Check server logs for errors
2. Verify Ollama models: `ollama list`
3. Check Python version: `python3 --version`
4. Ensure port 8000 is free: `lsof -i :8000`
5. Review SETUP_GUIDE.md for troubleshooting

---

**Happy Testing! 🧪**
