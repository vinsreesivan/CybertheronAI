#!/bin/bash

echo "=========================================="
echo "Multi-LLM Fusion - Quick Test Script"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Check Ollama
echo "Test 1: Checking Ollama connection..."
if curl -s http://localhost:11502/api/tags > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Ollama is running on port 11502${NC}"
else
    echo -e "${RED}❌ Ollama is not accessible on port 11502${NC}"
    echo "   Start it with: OLLAMA_HOST=0.0.0.0:11502 ollama serve"
    exit 1
fi
echo ""

# Test 2: Check if models exist
echo "Test 2: Checking if configured models are available..."
MODELS=("llama3.2:3b" "qwen3:4b" "gemma3:12b")
for model in "${MODELS[@]}"; do
    if curl -s http://localhost:11502/api/tags | grep -q "$model"; then
        echo -e "${GREEN}✅ $model found${NC}"
    else
        echo -e "${YELLOW}⚠️  $model not found (may need to pull it)${NC}"
    fi
done
echo ""

# Test 3: Check if server is running
echo "Test 3: Checking if FastAPI server is running..."
if curl -s http://localhost:9876/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Server is running on port 9876${NC}"

    # Get health info
    echo ""
    echo "Server Health Info:"
    curl -s http://localhost:9876/health | python3 -m json.tool
    echo ""
else
    echo -e "${YELLOW}⚠️  Server is not running${NC}"
    echo "   Start it with: python main.py"
    echo ""
    exit 0
fi

# Test 4: Simple query test
echo "Test 4: Testing simple query..."
echo "Sending test query: 'What is 2+2?'"
echo ""

RESPONSE=$(curl -s -X POST http://localhost:9876/query \
    -H "Content-Type: application/json" \
    -d '{"prompt": "What is 2+2? Answer in one sentence."}')

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Query successful!${NC}"
    echo ""
    echo "Fused Response:"
    echo "----------------------------------------"
    echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['fused_response'][:300] + ('...' if len(data['fused_response']) > 300 else ''))"
    echo "----------------------------------------"
    echo ""
    echo "Stats:"
    echo "$RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f\"  Time: {data['total_time']}s\"); print(f\"  Models: {data['successful_responses']}/{data['models_queried']} succeeded\")"
    echo ""
else
    echo -e "${RED}❌ Query failed${NC}"
fi

echo ""
echo "=========================================="
echo "Testing Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Open browser to: http://localhost:9876"
echo "  2. Try the web interface"
echo "  3. Run example script: python example_usage.py"
echo "  4. Switch presets: ./switch_preset.sh coding"
echo ""
