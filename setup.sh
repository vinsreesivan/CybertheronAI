#!/bin/bash

echo "==================================="
echo "Multi-LLM Fusion Setup"
echo "==================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed!"
    echo ""
    echo "Please install Ollama first:"
    echo "  - Linux/Mac: curl -fsSL https://ollama.com/install.sh | sh"
    echo "  - Or visit: https://ollama.com/download"
    exit 1
fi

echo "✅ Ollama found: $(ollama --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing Python dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "🤖 Pulling required Ollama models..."
echo "This may take a while depending on your internet connection..."
echo ""

# Pull models
models=("llama3.2" "gemma2" "qwen2.5")
for model in "${models[@]}"; do
    echo "Pulling $model..."
    ollama pull "$model"
done

echo ""
echo "==================================="
echo "✅ Setup Complete!"
echo "==================================="
echo ""
echo "To start the server:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run: python main.py"
echo "  3. Open your browser to: http://localhost:8000"
echo ""
echo "To customize models, edit config.yaml"
echo ""
