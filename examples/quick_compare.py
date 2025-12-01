"""
Quick comparison between 2 models

Usage: python examples/quick_compare.py

Requirements:
- Ollama running with models downloaded
- Run: ollama pull llama3.2:1b mistral:7b
"""

import json
from pathlib import Path

from llm_evaluator import ModelEvaluator
from llm_evaluator.providers.ollama_provider import OllamaProvider
from llm_evaluator.visualizations import EvaluationVisualizer


def compare_models(models: list[str], output_dir: str = "comparison_output"):
    """Compare multiple models and generate dashboard"""
    
    print("🔄 Comparing models (evaluating each with quick test)...\n")
    
    results = {}
    
    for model in models:
        print(f"📊 Evaluating {model}...")
        
        try:
            provider = OllamaProvider(model=model)
            
            if not provider.is_available():
                print(f"  ⚠️ {model} not available, skipping")
                continue
            
            evaluator = ModelEvaluator(provider=provider)
            eval_results = evaluator.evaluate_all()
            
            results[model] = {
                "overall_score": eval_results.overall_score,
                "accuracy": eval_results.accuracy,
                "avg_response_time": eval_results.avg_response_time,
                "coherence_score": eval_results.coherence_score,
            }
            
            print(f"  ✅ Score: {eval_results.overall_score:.1%}")
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            continue
    
    if not results:
        print("\n❌ No models could be evaluated!")
        return
    
    # Save results
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    results_file = output_path / "comparison_results.json"
    results_file.write_text(json.dumps(results, indent=2))
    
    # Print comparison table
    print("\n" + "=" * 60)
    print("📊 Comparison Results")
    print("=" * 60)
    print(f"{'Model':<25} {'Score':<10} {'Accuracy':<10} {'Speed (s)':<10}")
    print("-" * 60)
    
    for model, data in sorted(results.items(), key=lambda x: x[1]["overall_score"], reverse=True):
        print(
            f"{model:<25} "
            f"{data['overall_score']:<10.1%} "
            f"{data['accuracy']:<10.1%} "
            f"{data['avg_response_time']:<10.2f}"
        )
    
    print("=" * 60)
    
    # Try to generate dashboard
    try:
        visualizer = EvaluationVisualizer()
        dashboard_path = output_path / "dashboard.html"
        # Note: This requires evaluation results objects, not dicts
        # For now, just save the JSON
        print(f"\n✅ Results saved to: {results_file}")
        print(f"📊 To generate dashboard, use: llm-eval visualize {results_file}")
    except Exception as e:
        print(f"\n⚠️ Could not generate dashboard: {e}")
        print(f"✅ Results saved to: {results_file}")


if __name__ == "__main__":
    # Default models to compare
    models = ["llama3.2:1b", "phi3:mini"]
    
    print("=" * 60)
    print("🚀 LLM Quick Comparison")
    print("=" * 60)
    print(f"Models: {', '.join(models)}")
    print()
    
    compare_models(models)
