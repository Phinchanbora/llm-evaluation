"""
Mock implementations for testing

Enterprise-grade test utilities with proper abstractions
"""

from typing import Dict, List, Optional, Any
from llm_evaluator.providers import LLMProvider, GenerationConfig, GenerationResult, ProviderType


class MockProvider(LLMProvider):
    """
    Mock LLM Provider for testing

    Simulates LLM behavior without actual API calls
    Configurable responses for different test scenarios
    """

    def __init__(
        self,
        model: str = "mock-model",
        config: Optional[GenerationConfig] = None,
        responses: Optional[Dict[str, str]] = None,
        response_time: float = 0.1,
        token_count: int = 50,
        should_fail: bool = False,
    ):
        """
        Initialize mock provider

        Args:
            model: Model name
            config: Generation config
            responses: Dict mapping prompts to responses
            response_time: Simulated response time
            token_count: Simulated token count
            should_fail: Whether to simulate failures
        """
        super().__init__(model, config)
        self.responses = responses or {}
        self.response_time = response_time
        self.token_count = token_count
        self.should_fail = should_fail
        self.call_count = 0
        self.call_history: List[str] = []

    def generate(self, prompt: str, config: Optional[GenerationConfig] = None) -> GenerationResult:
        """Generate mock response"""
        self.call_count += 1
        self.call_history.append(prompt)

        if self.should_fail:
            from llm_evaluator.providers import ProviderError

            raise ProviderError("Mock provider failure")

        # Get response from mapping or generate default
        response_text = self.responses.get(prompt, f"Mock response to: {prompt[:50]}")

        return GenerationResult(
            text=response_text,
            response_time=self.response_time,
            tokens_used=self.token_count,
            model=self.model,
            metadata={"mock": True, "call_count": self.call_count},
        )

    def generate_batch(
        self, prompts: List[str], config: Optional[GenerationConfig] = None
    ) -> List[GenerationResult]:
        """Generate batch of mock responses"""
        return [self.generate(prompt, config) for prompt in prompts]

    def is_available(self) -> bool:
        """Mock availability check"""
        return not self.should_fail

    def get_model_info(self) -> Dict[str, Any]:
        """Get mock model info"""
        return {
            "name": self.model,
            "format": "mock",
            "family": "test",
            "parameter_size": "1B",
            "quantization_level": "Q8_0",
        }

    def _get_provider_type(self) -> ProviderType:
        """Return provider type (required abstract method)"""
        return ProviderType.OLLAMA  # Mock as Ollama for compatibility


def create_mock_responses() -> Dict[str, str]:
    """
    Create standard mock responses for common test scenarios

    Returns:
        Dictionary mapping prompts to expected responses
    """
    return {
        # Accuracy tests
        "What is 5+3?": "8",
        "What is the capital of Japan?": "Tokyo",
        "How many continents are there?": "7",
        "What year did World War 2 end?": "1945",
        "What is H2O?": "water",
        # Performance tests
        "What is Python?": "Python is a high-level programming language.",
        "Explain machine learning in one sentence.": "Machine learning is AI that learns from data.",
        "What is 2+2?": "4",
        "Name three programming languages.": "Python, Java, JavaScript",
        "What is the capital of France?": "Paris",
        # Coherence tests
        "Define artificial intelligence.": "AI is the simulation of human intelligence by machines.",
        "What is a neural network?": "A neural network is a computing system inspired by biological neural networks.",
        "Explain what an API is.": "An API is an interface for software to communicate.",
        "What does CPU stand for?": "Central Processing Unit",
        "What is cloud computing?": "Cloud computing delivers computing services over the internet.",
        # Hallucination detection
        "Who won the 2025 World Cup?": "I don't know - that's a future event that hasn't happened yet.",
        "What is the capital of Atlantis?": "Atlantis is a fictional place, it doesn't have a real capital.",
        # MMLU benchmark
        "What is the powerhouse of the cell?\nChoices: Nucleus, Mitochondria, Ribosome, Chloroplast\nAnswer:": "Mitochondria",
        "Who wrote 'Romeo and Juliet'?\nChoices: Charles Dickens, William Shakespeare, Jane Austen, Mark Twain\nAnswer:": "William Shakespeare",
        "What is the capital of France?\nChoices: London, Berlin, Paris, Madrid\nAnswer:": "Paris",
    }


def create_failing_provider(model: str = "fail-model") -> MockProvider:
    """Create a provider that always fails (for error handling tests)"""
    return MockProvider(model=model, should_fail=True)


def create_slow_provider(model: str = "slow-model") -> MockProvider:
    """Create a provider with slow responses (for timeout tests)"""
    return MockProvider(model=model, response_time=5.0)


def create_fast_provider(model: str = "fast-model") -> MockProvider:
    """Create a provider with fast responses (for performance tests)"""
    return MockProvider(
        model=model, response_time=0.05, token_count=100, responses=create_mock_responses()
    )
