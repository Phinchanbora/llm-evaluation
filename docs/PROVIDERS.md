# 🔌 Providers Guide

> Complete guide to all supported LLM providers.

**Navigation:** [← README](../README.md) | [Quick Start](QUICKSTART.md) | [API Reference](API.md) | [Academic Usage](ACADEMIC_USAGE.md)

---

## Overview

LLM Benchmark Toolkit supports **5 providers** out of the box:

| Provider | Type | Models | Cost |
|----------|------|--------|------|
| **Ollama** | Local | Llama, Mistral, Phi, etc. | Free |
| **OpenAI** | API | GPT-4o, GPT-4, GPT-3.5 | $$ |
| **Anthropic** | API | Claude 3.5, Claude 3 | $$ |
| **DeepSeek** | API | DeepSeek-V3, Coder | $ |
| **HuggingFace** | API | Various | Varies |

---

## Ollama (Local)

Run models locally on your machine.

### Setup

```bash
# Install Ollama
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai

# Start server
ollama serve

# Download models
ollama pull llama3.2:1b
ollama pull mistral:7b
ollama pull phi3:3.8b
```

### Usage

```python
from llm_evaluator.providers import OllamaProvider

provider = OllamaProvider(
    model="llama3.2:1b",
    base_url="http://localhost:11434"  # Default
)

result = provider.generate("What is 2+2?")
print(result.text)
```

### Available Models

```bash
ollama list
```

Popular models:

- `llama3.2:1b`, `llama3.2:3b` - Meta's latest
- `mistral:7b` - Mistral AI
- `phi3:3.8b` - Microsoft
- `qwen2.5:0.5b`, `qwen2.5:7b` - Alibaba
- `gemma2:2b`, `gemma2:9b` - Google

### Pros & Cons

✅ **Pros:**

- Free to use
- No API keys needed
- Full privacy (runs locally)
- Fast for small models

❌ **Cons:**

- Requires local GPU/CPU resources
- Limited to models you can run
- Setup required

---

## OpenAI

Access GPT models via API.

### Setup

```bash
export OPENAI_API_KEY="sk-..."
```

Or set in Python:

```python
provider = OpenAIProvider(
    model="gpt-4o-mini",
    api_key="sk-..."
)
```

### Usage

```python
from llm_evaluator.providers import OpenAIProvider

provider = OpenAIProvider(model="gpt-4o-mini")

result = provider.generate("What is 2+2?")
print(result.text)
print(f"Cost: ${result.cost_usd:.4f}")
```

### Available Models

| Model | Context | Price (Input/Output) |
|-------|---------|---------------------|
| `gpt-4o` | 128K | $2.50 / $10.00 per 1M |
| `gpt-4o-mini` | 128K | $0.15 / $0.60 per 1M |
| `gpt-4-turbo` | 128K | $10.00 / $30.00 per 1M |
| `gpt-3.5-turbo` | 16K | $0.50 / $1.50 per 1M |

### Pros & Cons

✅ **Pros:**

- State-of-the-art performance
- No hardware requirements
- Easy to use

❌ **Cons:**

- Costs money
- Rate limits
- Data sent to OpenAI

---

## Anthropic

Access Claude models via API.

### Setup

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Usage

```python
from llm_evaluator.providers import AnthropicProvider

provider = AnthropicProvider(model="claude-3-5-sonnet-20241022")

result = provider.generate("What is 2+2?")
print(result.text)
```

### Available Models

| Model | Context | Price (Input/Output) |
|-------|---------|---------------------|
| `claude-3-5-sonnet-20241022` | 200K | $3.00 / $15.00 per 1M |
| `claude-3-opus-20240229` | 200K | $15.00 / $75.00 per 1M |
| `claude-3-haiku-20240307` | 200K | $0.25 / $1.25 per 1M |

### Pros & Cons

✅ **Pros:**

- Excellent reasoning
- Long context window
- Good at following instructions

❌ **Cons:**

- Costs money
- Requires `anthropic` package

---

## DeepSeek

Affordable API with strong performance.

### Setup

```bash
export DEEPSEEK_API_KEY="sk-..."
```

### Usage

```python
from llm_evaluator.providers import DeepSeekProvider

provider = DeepSeekProvider(model="deepseek-chat")

result = provider.generate("What is 2+2?")
print(result.text)
```

### Available Models

| Model | Description | Price |
|-------|-------------|-------|
| `deepseek-chat` | General chat | $0.14 / $0.28 per 1M |
| `deepseek-coder` | Code generation | $0.14 / $0.28 per 1M |
| `deepseek-reasoner` | Advanced reasoning | $0.55 / $2.19 per 1M |

### Pros & Cons

✅ **Pros:**

- Very affordable
- Good performance
- OpenAI-compatible API

❌ **Cons:**

- Newer provider
- Smaller ecosystem

---

## Google Gemini

Access Google's Gemini models via API.

### Setup

```bash
# Windows
set GEMINI_API_KEY=AIza...

# Linux/Mac
export GEMINI_API_KEY="AIza..."
```

Or set in Python:

```python
provider = GeminiProvider(
    model="gemini-2.0-flash",
    api_key="AIza..."
)
```

### Usage

```python
from llm_evaluator.providers import GeminiProvider

provider = GeminiProvider(model="gemini-2.0-flash")

result = provider.generate("What is 2+2?")
print(result.text)
print(f"Tokens: {result.total_tokens}")
```

### Available Models

| Model | Context | Price (Input/Output) | Free Tier Limit |
|-------|---------|---------------------|-----------------|
| `gemini-2.5-flash` | 1M | $0.075 / $0.30 per 1M | 10 req/min |
| `gemini-2.5-pro` | 2M | $3.50 / $10.50 per 1M | 10 req/min |
| `gemini-2.0-flash` | 1M | $0.10 / $0.40 per 1M | 10 req/min |

### ⚠️ Free Tier Limitations

The Gemini free tier has **very strict rate limits**:

- **10 requests per minute** maximum
- Additional daily/hourly quotas may apply
- Rate limit errors automatically retry with exponential backoff

**Recommended usage for free tier:**

```bash
# Use small sample sizes (5-10 questions max)
llm-eval quick --model gemini-2.0-flash --provider gemini -s 5

# Run ONE benchmark at a time with pauses
llm-eval benchmark --model gemini-2.0-flash --provider gemini -b mmlu -s 5

# Wait 60+ seconds between runs to avoid hitting limits
```

**For serious evaluation work:**
- Upgrade to a paid plan for higher rate limits
- Use Ollama (local, unlimited) or Groq (generous free tier) for testing

### Pros & Cons

✅ **Pros:**

- Latest Google AI models
- Very long context windows (1-2M tokens)
- Competitive pricing on paid tier
- Auto-retry on rate limits

❌ **Cons:**

- Free tier extremely limited (10 req/min)
- May hit daily quotas quickly
- Not suitable for large benchmarks on free tier
- Requires API key setup

### Testing Status

⚠️ **Partially Tested**: Gemini provider has been tested with `gemini-2.0-flash` on small sample sizes. Works correctly but free tier limitations make extensive testing impractical. Unit tests verify the implementation, but real-world usage on free tier is limited.

---

## HuggingFace

Access models via HuggingFace Inference API.

### Setup

```bash
export HF_TOKEN="hf_..."
```

### Usage

```python
from llm_evaluator.providers import HuggingFaceProvider

provider = HuggingFaceProvider(
    model="meta-llama/Llama-2-7b-chat-hf"
)

result = provider.generate("What is 2+2?")
print(result.text)
```

### Pros & Cons

✅ **Pros:**

- Access to many models
- Some free tier

❌ **Cons:**

- Variable availability
- Rate limits on free tier

---

## CachedProvider

Wrapper that adds caching to any provider.

### Usage

```python
from llm_evaluator.providers import CachedProvider, OllamaProvider

base = OllamaProvider(model="llama3.2:1b")
provider = CachedProvider(base, cache_dir="~/.cache/llm-eval")

# First call: hits the model
result1 = provider.generate("What is 2+2?")
print(f"Cached: {result1.cached}")  # False

# Second call: from cache
result2 = provider.generate("What is 2+2?")
print(f"Cached: {result2.cached}")  # True

# Check stats
stats = provider.get_cache_stats()
print(f"Hit rate: {stats['hit_rate_percent']:.1f}%")
```

### Cache Location

Default: `~/.cache/llm-eval/`

Each model gets its own cache directory.

---

## Provider Auto-Detection

The CLI auto-detects providers from environment variables:

```bash
# Set one of these
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export DEEPSEEK_API_KEY="sk-..."
export HF_TOKEN="hf_..."

# Or have Ollama running locally

# Then run
llm-eval quick
```

Detection order:

1. OpenAI (if `OPENAI_API_KEY` set)
2. Anthropic (if `ANTHROPIC_API_KEY` set)
3. DeepSeek (if `DEEPSEEK_API_KEY` set)
4. Ollama (if server running on localhost:11434)
5. HuggingFace (if `HF_TOKEN` set)

---

## Custom Provider

Implement your own provider:

```python
from llm_evaluator.providers import LLMProvider, GenerationResult, ProviderType

class MyProvider(LLMProvider):
    def __init__(self, model: str):
        self._model = model
    
    @property
    def model_name(self) -> str:
        return self._model
    
    @property
    def provider_type(self) -> ProviderType:
        return ProviderType.OPENAI  # Or create custom
    
    def generate(self, prompt: str) -> GenerationResult:
        # Your implementation
        response = call_my_api(prompt)
        return GenerationResult(
            text=response.text,
            response_time=response.latency,
            tokens_used=response.tokens
        )
```

---

## Comparison Table

| Feature | Ollama | OpenAI | Anthropic | Gemini | DeepSeek | Groq | Together | Fireworks | HuggingFace |
|---------|--------|--------|-----------|--------|----------|------|----------|-----------|-------------|
| Local | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Free | ✅ | ❌ | ❌ | Limited* | ❌ | ✅ | ❌ | ❌ | Partial |
| API Key | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Speed | Varies | Fast | Fast | Fast | Fast | Very Fast | Fast | Fast | Varies |
| Best Models | Llama, Mistral | GPT-4o | Claude 3.5 | Gemini 2.5 | DeepSeek-V3 | Llama 3.1 | Various | Various | Varies |
| **Tested** | ✅ Full | ⚠️ Units | ⚠️ Units | ⚠️ Partial | ⚠️ Units | ⚠️ Units | ⚠️ Units | ⚠️ Units | ⚠️ Units |

\* Gemini free tier: 10 requests/minute only

---

## Provider Testing Status

### ✅ Fully Tested
- **Ollama**: Extensively tested with Llama 3.2, Mistral, Phi3, and other models. All features verified with real-world usage.

### ⚠️ Partially Tested
- **Gemini**: Tested with `gemini-2.0-flash` on small sample sizes. Works correctly but free tier limitations (10 req/min) prevent extensive testing. Auto-retry logic verified. Unit tests pass.

### ⚠️ Unit Tests Only
The following providers have **unit tests** and follow the same patterns as tested providers, but have **NOT been verified with real API keys** to avoid subscription costs:

- **OpenAI** - Should work with valid API key (standard OpenAI SDK)
- **Anthropic** - Should work with valid API key (standard Anthropic SDK)
- **DeepSeek** - Should work with valid API key (OpenAI-compatible)
- **Groq** - Should work with valid API key (OpenAI-compatible)
- **Together** - Should work with valid API key (OpenAI-compatible)
- **Fireworks** - Should work with valid API key (OpenAI-compatible)
- **HuggingFace** - Should work with valid token (HF Inference API)

**If you test any of these providers and find issues, please [open an issue](https://github.com/NahuelGiudizi/llm-evaluation/issues)!**

---

**Navigation:** [← README](../README.md) | [Quick Start](QUICKSTART.md) | [API Reference](API.md) | [Academic Usage](ACADEMIC_USAGE.md)
