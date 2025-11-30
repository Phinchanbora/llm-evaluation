"""
Quick demo of LLM Evaluator - Clean Architecture Edition

Demonstrates the new provider-based architecture with dependency injection
"""

from llm_evaluator import ModelEvaluator  # type: ignore
from llm_evaluator.providers.ollama_provider import OllamaProvider  # type: ignore
from llm_evaluator.providers import GenerationConfig  # type: ignore


def main():
    print("="*60)
    print("LLM EVALUATOR - Clean Architecture Demo")
    print("="*60)
    
    # Configure generation settings
    config = GenerationConfig(
        temperature=0.7,
        max_tokens=500,
        timeout_seconds=30,
        retry_attempts=3
    )
    
    # Initialize provider with dependency injection
    model = "llama3.2:1b"
    provider = OllamaProvider(model=model, config=config)
    
    # Check provider availability
    print(f"\n🔍 Checking {model} availability...")
    if not provider.is_available():
        print(f"❌ {model} not available. Make sure Ollama is running.")
        return
    
    print(f"✅ {model} is ready!")
    
    # Initialize evaluator with provider injection
    evaluator = ModelEvaluator(provider=provider, config=config)
    
    # Run comprehensive evaluation
    results = evaluator.evaluate_all()
    
    # Generate report
    evaluator.generate_report(results, output="evaluation_report.md")
    
    print("\n✅ Demo complete!")
    print(f"📊 Overall Score: {results.overall_score:.2f}/1.00")
    print(f"📄 Report saved to: evaluation_report.md")


if __name__ == "__main__":
    main()
