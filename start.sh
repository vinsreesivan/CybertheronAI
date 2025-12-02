#!/bin/bash

echo "=========================================="
echo "🚀 CybertheronAI Multi-LLM Fusion Launcher"
echo "=========================================="
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run setup_simple.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if Ollama is accessible
echo "🔍 Checking Ollama connection..."
if curl -s http://localhost:11502/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running on port 11502"
else
    echo "⚠️  Warning: Ollama not accessible on port 11502"
    echo "   Make sure Ollama is running: OLLAMA_HOST=0.0.0.0:11502 ollama serve"
    echo ""
fi

# Start the server
echo ""
echo "✅ Starting Multi-LLM Fusion Server..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📱 Access the application at:"
echo "   • Main Fusion UI:    http://localhost:9876"
echo "   • Auto-Debug Editor: http://localhost:9876/code-editor"
echo "   • API Docs:          http://localhost:9876/docs"
echo ""
echo "🤖 Active Models: llama3.2:3b, qwen3:4b, gemma3:12b, gpt-oss:20b"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python main.py
