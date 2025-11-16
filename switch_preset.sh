#!/bin/bash

# Quick preset switcher for Multi-LLM Fusion

PRESET=$1

if [ -z "$PRESET" ]; then
    echo "Usage: ./switch_preset.sh [general|coding|security|quality|speed]"
    echo ""
    echo "Available presets:"
    echo "  general  - General purpose (llama3.2:3b, qwen3:4b, gemma3:12b)"
    echo "  coding   - Coding & development (qwen3-coder, qwen3:4b, gemma3:12b)"
    echo "  security - Cybersecurity (Foundation-Sec, BaronLLM, gemma3:12b)"
    echo "  quality  - Maximum quality (llama4:16x17b, gpt-oss:20b, gemma3:12b)"
    echo "  speed    - Speed optimized (llama3.2:3b, qwen3:4b)"
    echo ""
    exit 1
fi

# Backup current config
cp config.yaml config.yaml.backup

case $PRESET in
    general)
        cat > config.yaml << 'EOF'
# Multi-LLM Fusion Configuration - General Purpose Preset

models:
  - name: "llama3.2:3b"
    weight: 1.0
    enabled: true
  - name: "qwen3:4b"
    weight: 1.0
    enabled: true
  - name: "gemma3:12b"
    weight: 1.0
    enabled: true

refiner_model: "gemma3:12b"
fusion_strategy: "refiner"

server:
  host: "0.0.0.0"
  port: 8000
  ollama_base_url: "http://localhost:11502"

generation:
  temperature: 0.7
  max_tokens: 2000
  timeout: 60
EOF
        echo "✅ Switched to GENERAL purpose preset"
        echo "   Models: llama3.2:3b, qwen3:4b, gemma3:12b"
        ;;

    coding)
        cat > config.yaml << 'EOF'
# Multi-LLM Fusion Configuration - Coding Preset

models:
  - name: "qwen3-coder:latest"
    weight: 1.0
    enabled: true
  - name: "qwen3:4b"
    weight: 1.0
    enabled: true
  - name: "gemma3:12b"
    weight: 1.0
    enabled: true

refiner_model: "qwen3-coder:latest"
fusion_strategy: "refiner"

server:
  host: "0.0.0.0"
  port: 8000
  ollama_base_url: "http://localhost:11502"

generation:
  temperature: 0.7
  max_tokens: 2000
  timeout: 90
EOF
        echo "✅ Switched to CODING preset"
        echo "   Models: qwen3-coder, qwen3:4b, gemma3:12b"
        echo "   Refiner: qwen3-coder (coding specialist)"
        ;;

    security)
        cat > config.yaml << 'EOF'
# Multi-LLM Fusion Configuration - Security Preset

models:
  - name: "hf.co/fdtn-ai/Foundation-Sec-8B-Instruct-Q8_0-GGUF:Q8_0"
    weight: 1.0
    enabled: true
  - name: "hf.co/AlicanKiraz0/Cybersecurity-BaronLLM_Offensive_Security_LLM_Q6_K_GGUF:latest"
    weight: 1.0
    enabled: true
  - name: "gemma3:12b"
    weight: 1.0
    enabled: true

refiner_model: "hf.co/fdtn-ai/Foundation-Sec-8B-Instruct-Q8_0-GGUF:Q8_0"
fusion_strategy: "refiner"

server:
  host: "0.0.0.0"
  port: 8000
  ollama_base_url: "http://localhost:11502"

generation:
  temperature: 0.7
  max_tokens: 2000
  timeout: 90
EOF
        echo "✅ Switched to SECURITY preset"
        echo "   Models: Foundation-Sec, BaronLLM, gemma3:12b"
        echo "   Refiner: Foundation-Sec (security specialist)"
        ;;

    quality)
        cat > config.yaml << 'EOF'
# Multi-LLM Fusion Configuration - Maximum Quality Preset

models:
  - name: "llama4:16x17b"
    weight: 1.0
    enabled: true
  - name: "gpt-oss:20b"
    weight: 1.0
    enabled: true
  - name: "gemma3:12b"
    weight: 1.0
    enabled: true

refiner_model: "llama4:16x17b"
fusion_strategy: "refiner"

server:
  host: "0.0.0.0"
  port: 8000
  ollama_base_url: "http://localhost:11502"

generation:
  temperature: 0.7
  max_tokens: 3000
  timeout: 120
EOF
        echo "✅ Switched to QUALITY preset (slow but best results)"
        echo "   Models: llama4:16x17b, gpt-oss:20b, gemma3:12b"
        echo "   Refiner: llama4:16x17b (most capable)"
        echo "   ⚠️  Warning: Requires ~80GB+ RAM"
        ;;

    speed)
        cat > config.yaml << 'EOF'
# Multi-LLM Fusion Configuration - Speed Optimized Preset

models:
  - name: "llama3.2:3b"
    weight: 1.0
    enabled: true
  - name: "qwen3:4b"
    weight: 1.0
    enabled: true

refiner_model: "qwen3:4b"
fusion_strategy: "refiner"

server:
  host: "0.0.0.0"
  port: 8000
  ollama_base_url: "http://localhost:11502"

generation:
  temperature: 0.7
  max_tokens: 1500
  timeout: 45
EOF
        echo "✅ Switched to SPEED preset (fast responses)"
        echo "   Models: llama3.2:3b, qwen3:4b"
        echo "   Refiner: qwen3:4b"
        ;;

    *)
        echo "❌ Unknown preset: $PRESET"
        echo "Available: general, coding, security, quality, speed"
        mv config.yaml.backup config.yaml
        exit 1
        ;;
esac

echo ""
echo "Previous config backed up to: config.yaml.backup"
echo "Restart the server to apply changes: ./run.sh"
