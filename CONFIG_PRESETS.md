# Configuration Presets for Different Use Cases

You have several specialized models. Here are recommended configurations for different scenarios:

## Preset 1: General Purpose (Default)
**Best for**: General questions, research, explanations

```yaml
models:
  - name: "llama3.2:3b"
    enabled: true
  - name: "qwen3:4b"
    enabled: true
  - name: "gemma3:12b"
    enabled: true

refiner_model: "gemma3:12b"
```

**Why**: Fast, diverse models with good general knowledge.

---

## Preset 2: Coding & Development
**Best for**: Programming questions, code review, debugging

```yaml
models:
  - name: "qwen3-coder:latest"     # Specialized for coding
    enabled: true
  - name: "qwen3:4b"               # General knowledge
    enabled: true
  - name: "gemma3:12b"             # Good reasoning
    enabled: true

refiner_model: "qwen3-coder:latest"  # Use coding expert as refiner
```

**Why**: Combines coding specialist with general models for comprehensive answers.

---

## Preset 3: Cybersecurity & Offensive Security
**Best for**: Security analysis, penetration testing, vulnerability research

```yaml
models:
  - name: "hf.co/fdtn-ai/Foundation-Sec-8B-Instruct-Q8_0-GGUF:Q8_0"
    enabled: true
  - name: "hf.co/AlicanKiraz0/Cybersecurity-BaronLLM_Offensive_Security_LLM_Q6_K_GGUF:latest"
    enabled: true
  - name: "gemma3:12b"             # General reasoning
    enabled: true

refiner_model: "hf.co/fdtn-ai/Foundation-Sec-8B-Instruct-Q8_0-GGUF:Q8_0"
```

**Why**: Two security-focused models + general model for balanced perspective.

---

## Preset 4: Maximum Quality (Slow)
**Best for**: Complex analysis, research, when quality > speed

```yaml
models:
  - name: "llama4:16x17b"          # Massive MoE model
    enabled: true
  - name: "gpt-oss:20b"
    enabled: true
  - name: "gemma3:12b"
    enabled: true

refiner_model: "llama4:16x17b"     # Use most capable model
```

**Why**: Uses your largest, most capable models. Slower but highest quality.

---

## Preset 5: Speed Optimized
**Best for**: Quick answers, rapid prototyping, testing

```yaml
models:
  - name: "llama3.2:3b"
    enabled: true
  - name: "qwen3:4b"
    enabled: true

refiner_model: "qwen3:4b"
```

**Why**: Only small, fast models. Great for quick iterations.

---

## Preset 6: Multi-Domain Expert
**Best for**: Complex questions requiring multiple perspectives

```yaml
models:
  - name: "qwen3-coder:latest"     # Coding
    enabled: true
  - name: "hf.co/fdtn-ai/Foundation-Sec-8B-Instruct-Q8_0-GGUF:Q8_0"  # Security
    enabled: true
  - name: "gemma3:12b"             # General
    enabled: true
  - name: "gpt-oss:20b"            # Reasoning
    enabled: true

refiner_model: "gpt-oss:20b"
```

**Why**: Combines specialists from different domains.

---

## How to Switch Presets

### Method 1: Edit config.yaml directly
Just copy the desired preset into your `config.yaml` file.

### Method 2: Create multiple config files
```bash
# Save different presets
cp config.yaml config-general.yaml
cp config.yaml config-coding.yaml
cp config.yaml config-security.yaml

# Run with specific config (modify main.py to accept --config flag)
python main.py --config config-coding.yaml
```

### Method 3: Quick toggle via comments
Keep all models in config.yaml and toggle `enabled: true/false`:

```yaml
models:
  # General models
  - name: "llama3.2:3b"
    enabled: true      # ← Change to false to disable

  # Coding models
  - name: "qwen3-coder:latest"
    enabled: false     # ← Change to true to enable
```

---

## Performance Comparison

| Preset | Models | Avg Time | Quality | RAM Usage |
|--------|--------|----------|---------|-----------|
| Speed Optimized | 2 | ~5-10s | Good | ~5 GB |
| General Purpose | 3 | ~10-20s | Very Good | ~13 GB |
| Coding | 3 | ~15-30s | Excellent (code) | ~25 GB |
| Security | 3 | ~15-25s | Excellent (sec) | ~18 GB |
| Multi-Domain | 4 | ~20-40s | Excellent | ~35 GB |
| Maximum Quality | 3 | ~40-90s | Outstanding | ~80+ GB |

*Times are approximate and depend on hardware and prompt complexity*

---

## Recommendations

1. **Start with General Purpose** (default config) to test the system
2. **For coding work**: Switch to Coding preset
3. **For security analysis**: Switch to Cybersecurity preset
4. **For best results**: Use Maximum Quality (if you have 128GB+ RAM)
5. **For quick testing**: Use Speed Optimized

## Pro Tips

- **Mixing specialists**: Combine domain-specific models for cross-domain questions
- **Refiner selection**: Use the most capable model as refiner for best synthesis
- **RAM constraints**: Disable larger models or use smaller variants
- **Speed vs Quality**: Fewer models = faster, more models = better fusion

---

**Your Current Config**: General Purpose (llama3.2:3b, qwen3:4b, gemma3:12b)
**Recommended for you**: Try the Coding or Security presets given your specialized models!
