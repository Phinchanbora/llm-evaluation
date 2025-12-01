#!/usr/bin/env python3
"""
Academic Evaluation Example

This example demonstrates how to run publication-quality evaluations
with statistical rigor, baseline comparisons, and proper export formats.

Usage:
    python academic_evaluation.py

Output:
    - academic_results.json: Full results with confidence intervals
    - results_table.tex: LaTeX table for papers
    - citations.bib: BibTeX citations for benchmarks
    - reproducibility_manifest.json: Full reproducibility info
"""

import json
from pathlib import Path

# Import evaluation components
from llm_evaluator import ModelEvaluator
from llm_evaluator.providers.ollama_provider import OllamaProvider

# Import academic features
from llm_evaluator.statistical_metrics import (
    calculate_wilson_ci,
    mcnemar_test,
    cohens_h,
)
from llm_evaluator.academic_baselines import (
    ACADEMIC_BASELINES,
    compare_to_baseline,
)
from llm_evaluator.error_analysis import (
    ErrorAnalyzer,
    expected_calibration_error,
)
from llm_evaluator.export import (
    export_to_latex,
    generate_bibtex,
    generate_reproducibility_manifest,
    generate_methods_section,
)


def main():
    print("=" * 60)
    print("🎓 Academic Evaluation Example")
    print("=" * 60)
    
    # =========================================================
    # 1. Setup
    # =========================================================
    print("\n📦 Setting up evaluation...")
    
    model_name = "llama3.2:1b"  # Change to your model
    sample_size = 100  # Use 500+ for papers
    
    # Create provider (use OpenAIProvider for GPT models, etc.)
    provider = OllamaProvider(model=model_name)
    
    # Check availability
    if not provider.is_available():
        print(f"❌ Model {model_name} not available. Is Ollama running?")
        print("   Try: ollama pull llama3.2:1b")
        return
    
    evaluator = ModelEvaluator(provider=provider)
    
    # =========================================================
    # 2. Run Academic Evaluation
    # =========================================================
    print(f"\n📊 Running academic evaluation (n={sample_size})...")
    print("   This may take several minutes...")
    
    results = evaluator.evaluate_all_academic(
        sample_size=sample_size,
        compare_baselines=True
    )
    
    # =========================================================
    # 3. Display Results with Confidence Intervals
    # =========================================================
    print("\n" + "=" * 60)
    print("📊 RESULTS WITH CONFIDENCE INTERVALS")
    print("=" * 60)
    
    print(f"\n📈 MMLU Accuracy: {results.mmlu_accuracy:.1%}")
    if results.mmlu_ci:
        ci_width = results.mmlu_ci[1] - results.mmlu_ci[0]
        print(f"   95% CI: [{results.mmlu_ci[0]:.1%}, {results.mmlu_ci[1]:.1%}]")
        print(f"   CI Width: {ci_width:.1%}")
    
    print(f"\n📈 TruthfulQA Score: {results.truthfulqa_score:.1%}")
    if results.truthfulqa_ci:
        print(f"   95% CI: [{results.truthfulqa_ci[0]:.1%}, {results.truthfulqa_ci[1]:.1%}]")
    
    print(f"\n📈 HellaSwag Accuracy: {results.hellaswag_accuracy:.1%}")
    if results.hellaswag_ci:
        print(f"   95% CI: [{results.hellaswag_ci[0]:.1%}, {results.hellaswag_ci[1]:.1%}]")
    
    # =========================================================
    # 4. Baseline Comparison
    # =========================================================
    print("\n" + "=" * 60)
    print("📊 COMPARISON TO PUBLISHED BASELINES")
    print("=" * 60)
    
    if results.baseline_comparison:
        for baseline_name, comparison in results.baseline_comparison.items():
            diff = comparison.get("difference", 0)
            sign = "+" if diff > 0 else ""
            print(f"\n   vs {baseline_name}:")
            print(f"      MMLU difference: {sign}{diff:.1%}")
            
            # Calculate effect size
            if "baseline_mmlu" in comparison:
                h = cohens_h(results.mmlu_accuracy, comparison["baseline_mmlu"])
                effect = "small" if abs(h) < 0.2 else ("medium" if abs(h) < 0.5 else "large")
                print(f"      Effect size (Cohen's h): {h:.3f} ({effect})")
    
    # =========================================================
    # 5. Error Analysis
    # =========================================================
    print("\n" + "=" * 60)
    print("🔍 ERROR ANALYSIS")
    print("=" * 60)
    
    if results.error_analysis:
        print("\n   Error Categories:")
        if "categories" in results.error_analysis:
            for category, count in results.error_analysis["categories"].items():
                print(f"      {category}: {count}")
        
        if "ece" in results.error_analysis:
            ece = results.error_analysis["ece"]
            calibration = "well-calibrated" if ece < 0.1 else "poorly calibrated"
            print(f"\n   Expected Calibration Error: {ece:.3f} ({calibration})")
    
    # =========================================================
    # 6. Statistical Significance Example
    # =========================================================
    print("\n" + "=" * 60)
    print("📐 STATISTICAL METHODS DEMO")
    print("=" * 60)
    
    # Wilson CI calculation
    print("\n   Wilson CI for 85% accuracy with n=100:")
    lower, upper = calculate_wilson_ci(0.85, 100, confidence=0.95)
    print(f"      95% CI: [{lower:.1%}, {upper:.1%}]")
    
    # Effect size
    print("\n   Effect size between 85% and 80%:")
    h = cohens_h(0.85, 0.80)
    print(f"      Cohen's h = {h:.3f}")
    
    # =========================================================
    # 7. Export Results
    # =========================================================
    print("\n" + "=" * 60)
    print("📄 EXPORTING RESULTS")
    print("=" * 60)
    
    # Prepare results dict for export
    results_dict = {
        "model": model_name,
        "sample_size": sample_size,
        "mmlu_accuracy": results.mmlu_accuracy,
        "mmlu_ci": results.mmlu_ci,
        "truthfulqa_score": results.truthfulqa_score,
        "truthfulqa_ci": results.truthfulqa_ci,
        "hellaswag_accuracy": results.hellaswag_accuracy,
        "hellaswag_ci": results.hellaswag_ci,
        "baseline_comparison": results.baseline_comparison,
        "error_analysis": results.error_analysis,
    }
    
    # Save JSON
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    
    json_path = output_dir / "academic_results.json"
    json_path.write_text(json.dumps(results_dict, indent=2, default=str))
    print(f"\n   ✅ JSON results: {json_path}")
    
    # Generate LaTeX table
    latex_content = export_to_latex(results_dict, model_name)
    latex_path = output_dir / "results_table.tex"
    latex_path.write_text(latex_content)
    print(f"   ✅ LaTeX table: {latex_path}")
    
    # Generate BibTeX
    bibtex_content = generate_bibtex()
    bibtex_path = output_dir / "citations.bib"
    bibtex_path.write_text(bibtex_content)
    print(f"   ✅ BibTeX citations: {bibtex_path}")
    
    # Generate reproducibility manifest
    manifest = generate_reproducibility_manifest(
        model=model_name,
        provider="ollama",
        sample_size=sample_size,
        random_seed=42,
        results=results_dict
    )
    manifest_path = output_dir / "reproducibility_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, default=str))
    print(f"   ✅ Reproducibility manifest: {manifest_path}")
    
    # =========================================================
    # 8. Methods Section
    # =========================================================
    print("\n" + "=" * 60)
    print("📝 METHODS SECTION FOR PAPER")
    print("=" * 60)
    
    methods = generate_methods_section(
        model=model_name,
        sample_size=sample_size,
        benchmarks=["mmlu", "truthfulqa", "hellaswag"]
    )
    print(f"\n{methods}")
    
    # =========================================================
    # 9. Summary
    # =========================================================
    print("\n" + "=" * 60)
    print("✅ EVALUATION COMPLETE")
    print("=" * 60)
    print(f"""
Files generated in {output_dir}/:
  - academic_results.json: Full results with CIs
  - results_table.tex: Ready-to-use LaTeX table
  - citations.bib: BibTeX for MMLU, TruthfulQA, HellaSwag
  - reproducibility_manifest.json: Full reproducibility info

For your paper, report results as:
  MMLU: {results.mmlu_accuracy:.1%} (95% CI: [{results.mmlu_ci[0]:.1%}, {results.mmlu_ci[1]:.1%}], n={sample_size})
""")


if __name__ == "__main__":
    main()
