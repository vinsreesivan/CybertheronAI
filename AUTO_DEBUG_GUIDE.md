# Auto-Debug Guide - LLM-Powered Code Execution

The Auto-Debug system allows you to execute Python code and automatically fix errors using multiple LLMs working together!

## 🎯 What It Does

1. **Executes your Python code**
2. **Detects errors automatically**
3. **Sends errors to multiple LLMs** (llama3.2:3b, qwen3:4b, gemma3:12b, gpt-oss:20b)
4. **LLMs analyze and propose fixes**
5. **Refined fix is applied and code re-executed**
6. **Loops until code succeeds** or max iterations reached

## 🚀 Three Ways to Use It

### Method 1: Terminal Interactive Mode (Recommended for Quick Testing)

```bash
# Make sure server dependencies are installed
source venv/bin/activate

# Run interactive terminal
python auto_debug.py
```

Then enter your code interactively:
```python
>>> Enter code (END to finish):
print("Hello!")
x = 10 / 0  # This will error
END
```

The system will:
- Execute the code
- Detect the error
- Ask if you want to fix it
- Send to LLMs for analysis
- Show the proposed fix
- Re-execute until it works!

### Method 2: Web UI (Best User Experience)

```bash
# Start the server
python main.py

# Open browser to:
http://localhost:8000/code-editor
```

Features:
- 📝 Syntax-highlighted code editor
- ▶️ One-click execution
- 🔄 Visual iteration history
- 📊 Success/error tracking
- 💾 Example code templates
- ⚙️ Configurable auto-fix behavior

### Method 3: Run Python Files

```bash
# Execute a Python file with auto-debugging
python auto_debug.py script.py

# Auto-fix mode (no confirmation needed)
python auto_debug.py script.py --auto
```

## 📖 Examples

### Example 1: Simple Error Fix

**Input Code:**
```python
print("Calculating...")
x = 10 / 0  # Division by zero
print(f"Result: {x}")
```

**What Happens:**
1. ❌ Code fails with `ZeroDivisionError`
2. 🤖 LLMs receive the error
3. 🔧 LLMs propose: Change `0` to a valid number or add error handling
4. ✅ Fixed code executes successfully

### Example 2: Syntax Error

**Input Code:**
```python
print("Hello"
# Missing closing parenthesis
```

**What Happens:**
1. ❌ `SyntaxError: unexpected EOF`
2. 🤖 LLMs analyze
3. 🔧 LLMs fix: Add missing `)`
4. ✅ Success!

### Example 3: Logic Error

**Input Code:**
```python
def calculate_average(numbers):
    return sum(numbers) / len(numbers)

nums = []
result = calculate_average(nums)
print(f"Average: {result}")
```

**What Happens:**
1. ❌ `ZeroDivisionError` (empty list)
2. 🤖 LLMs analyze
3. 🔧 LLMs add check for empty list
4. ✅ Fixed code handles edge case

## ⚙️ Configuration

### Max Iterations

Set how many times the system will try to fix the code:

**Web UI:** Adjust the "Max iterations" input (1-10)

**Terminal:** Edit `auto_debug.py`:
```python
self.max_iterations = 5  # Change this number
```

### Auto-Fix Mode

**Web UI:** Check/uncheck "Auto-fix errors" checkbox

**Terminal:**
- Interactive mode: You'll be asked for each fix
- File mode with `--auto`: Fixes automatically

### Which LLMs Are Used

The system uses all enabled models in `config.yaml`:

```yaml
models:
  - name: "llama3.2:3b"
    enabled: true
  - name: "qwen3:4b"
    enabled: true
  - name: "gemma3:12b"
    enabled: true
  - name: "gpt-oss:20b"
    enabled: true  # Added!
```

The **refiner model** synthesizes the final fix from all responses.

## 🎨 Terminal Interface

The terminal interface provides:

- **Color-coded output**
  - 🟢 Green = Success
  - 🔴 Red = Error
  - 🟡 Yellow = Warning
  - 🔵 Blue = Info

- **Clear sections**
  - Current code display
  - Execution status
  - Error analysis
  - Proposed fixes
  - Iteration summary

- **Progress tracking**
  - Iteration count
  - Time per iteration
  - Success/failure status

## 🌐 Web API

You can also use the API directly:

```bash
curl -X POST http://localhost:8000/execute \
  -H "Content-Type: application/json" \
  -d '{
    "code": "print(\"Hello\")\nx = 10 / 0",
    "auto_fix": true,
    "max_iterations": 5
  }'
```

Response:
```json
{
  "success": true,
  "iterations": [
    {
      "iteration": 1,
      "success": false,
      "error": "ZeroDivisionError...",
      "proposed_fix": "..."
    },
    {
      "iteration": 2,
      "success": true,
      "output": "Hello\n"
    }
  ],
  "final_code": "...",
  "output": "Hello\n"
}
```

## 🔒 Safety Features

1. **Subprocess Execution**: Code runs in isolated subprocess
2. **Timeout Protection**: 30-second timeout per execution
3. **Iteration Limit**: Maximum 5 attempts by default
4. **Error Containment**: Errors don't crash the main process

## 💡 Tips for Best Results

1. **Start Simple**: Test with simple errors first
2. **Clear Errors**: The clearer the error, the better the fix
3. **Patience**: LLMs need time to analyze (10-30 seconds)
4. **Iterations**: Complex errors may need 2-3 iterations
5. **Model Selection**: More models = better synthesis but slower

## 🐛 Troubleshooting

### "LLMs could not generate a fix"

**Cause**: LLMs' responses didn't contain valid code

**Solution**:
- Try running again (different LLM responses)
- Simplify the code
- Add comments explaining what you want

### "Maximum iterations reached"

**Cause**: Code couldn't be fixed in N attempts

**Solution**:
- Increase max_iterations
- Check if the error is too complex
- Try a different approach to the code

### "Timeout error"

**Cause**: Code took > 30 seconds

**Solution**:
- Remove infinite loops
- Optimize slow operations
- Increase timeout in `code_executor.py`

### Server not responding

**Solution**:
```bash
# Check Ollama is running
curl http://localhost:11502/api/tags

# Restart the server
python main.py
```

## 📊 Performance

**Typical Times:**
- Single execution: 2-5 seconds
- LLM analysis: 10-30 seconds
- Total (with 1 fix): 15-35 seconds
- Total (with 3 fixes): 45-90 seconds

**With 4 models active**: Expect ~20-30 seconds per iteration

## 🎓 Advanced Usage

### Custom Error Prompts

Edit `code_executor.py` to customize how errors are presented to LLMs:

```python
def get_error_prompt(self) -> str:
    return f"""Your custom prompt here...
    Code: {self.code}
    Error: {self.error}
    """
```

### Integration with CI/CD

```bash
# Test scripts automatically
python auto_debug.py test_suite.py --auto
```

### Batch Processing

```python
import asyncio
from auto_debug import AutoDebugger

async def process_files(files):
    debugger = AutoDebugger()
    for file in files:
        with open(file) as f:
            code = f.read()
        await debugger.run_code_with_auto_fix(code, auto_mode=True)
```

## 📚 Related Features

- **Multi-LLM Fusion**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Code Editor UI**: http://localhost:8000/code-editor

## 🆘 Quick Reference

| Task | Command |
|------|---------|
| Interactive terminal | `python auto_debug.py` |
| Run file | `python auto_debug.py script.py` |
| Auto-fix mode | `python auto_debug.py script.py --auto` |
| Web UI | `http://localhost:8000/code-editor` |
| Stop execution | `Ctrl+C` |
| Exit interactive | Type `exit` |
| Help | Type `help` in interactive mode |

---

**Enjoy automatic code debugging with the power of multiple LLMs!** 🚀
