#!/bin/bash

# Quick run script for Multi-LLM Fusion

echo "🚀 Starting Multi-LLM Fusion Server..."
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "⚠️  Ollama is not running. Starting Ollama..."
    ollama serve &
    sleep 3
fi

# Start the server
echo "✅ Starting FastAPI server..."
echo ""
python main.py
