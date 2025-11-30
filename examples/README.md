# Examples Directory

This directory contains example scripts demonstrating how to use the LLM Evaluation framework.

## Quick Start Examples

### 1. `demo.py` - Quick Test (30 seconds)
Basic demo with 8 hardcoded questions. Perfect for testing your setup.

```bash
python examples/demo.py
```

**Output:** Basic scores (MMLU, TruthfulQA, HellaSwag) with demo data.

---

### 2. `demo_visualizations.py` - See the Charts (1 minute)
Generates all visualization types with simulated data. No model evaluation.

```bash
python examples/demo_visualizations.py
```

**Output:** 7 interactive charts in `outputs/visualizations/`
- Open `evaluation_dashboard.html` in your browser

---

### 3. `compare_models.py` - Compare 2+ Models (Interactive)
Interactive script to compare multiple models side-by-side.

```bash
python examples/compare_models.py
```

**Prompts:**
1. Enter model names (e.g., `llama3.2:1b,mistral:7b`)
2. Choose mode (Demo/Sample/Full)

**Output:** Comparison dashboard in `outputs/comparisons/`

---

### 4. `run_sample_comparison.py` - Fast Comparison (45 minutes)
**Recommended for quick, statistically valid comparisons.**

Compares `qwen2.5:0.5b` vs `phi3.5:3.8b` with 500 questions per benchmark.

```bash
python examples/run_sample_comparison.py
```

**Output:**
- Statistical confidence: ±4.4% at 95% confidence
- Comparison dashboard with all charts
- ~45 minutes total for both models

---

### 5. `run_full_comparison.py` - Complete Benchmark (5 hours)
Full scientific comparison with all 24,901 questions.

```bash
python examples/run_full_comparison.py
```

**Output:**
- Research-grade data for papers
- Full MMLU (14,042), TruthfulQA (817), HellaSwag (10,042)
- ~2-3 hours per model

---

## Other Examples

### `demo_full_benchmarks.py`
Demonstrates different benchmark modes (demo vs full vs sampling).

### `demo_vs_real.py`
Side-by-side comparison of demo data vs real benchmark results.

---

## Typical Workflow

1. **Test your setup:** `python examples/demo.py`
2. **See visualizations:** `python examples/demo_visualizations.py`
3. **Quick comparison:** `python examples/run_sample_comparison.py`
4. **Full benchmark:** `python examples/run_full_comparison.py` (overnight)

---

## Customization

### Compare Your Own Models

Edit `run_sample_comparison.py`:

```python
models = ["your-model-1", "your-model-2"]
sample_size = 500  # Adjust sample size
```

### Change Output Directory

```python
output_dir = Path("custom/output/path")
```

---

## Benchmark Modes

| Mode | Questions | Time | Use Case |
|------|-----------|------|----------|
| **Demo** | 8 | 30s | Quick testing |
| **Sample (100)** | 300 | 5 min | Fast iteration |
| **Sample (500)** | 1,500 | 45 min | Valid comparison |
| **Sample (1000)** | 3,000 | 1.5 hrs | High confidence |
| **Full** | 24,901 | 5 hrs | Scientific paper |

---

## Output Files

All examples generate output in `outputs/`:

```
outputs/
├── visualizations/          # From demo_visualizations.py
│   ├── evaluation_dashboard.html  ← Open this!
│   ├── benchmark_comparison.png
│   └── ...
│
└── comparisons/            # From compare_models.py
    ├── comparison_dashboard.html  ← Open this!
    ├── benchmark_comparison.png
    └── ...
```

---

## Requirements

All examples require:
- Ollama running locally (`ollama serve`)
- Models pulled (`ollama pull llama3.2:1b`)
- Python 3.11+
- Dependencies installed (`pip install -e .`)

---

## Troubleshooting

**"Connection refused"**
```bash
ollama serve
```

**"Model not found"**
```bash
ollama pull <model-name>
```

**Slow execution**
- Check GPU usage: `nvidia-smi`
- Reduce sample_size in scripts
- Use demo mode for testing

---

## Next Steps

- Read [TUTORIAL.md](../TUTORIAL.md) for detailed guide
- Check [docs/QUICKSTART.md](../docs/QUICKSTART.md) for setup
- See [README.md](../README.md) for full documentation
