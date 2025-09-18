"""Main evaluation runner for KinderShield."""

from typing import List, Dict, Any, Optional
import yaml
import os
from pathlib import Path

from .config import Config
from .providers import DummyProvider, OpenAIProvider, AnthropicProvider
from .scoring.rules import SafetyRule, MathRule, ReadingRule, EvaluationResult


class Runner:
    """Main evaluation runner that orchestrates tests and scoring."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the runner with configuration."""
        self.config = config or Config.from_env()
        self.provider = self._get_provider()
        self.rules = {
            "safety": SafetyRule(),
            "math": MathRule(),
            "reading": ReadingRule()
        }
    
    def _get_provider(self):
        """Get the appropriate AI provider based on configuration."""
        provider_name = self.config.model_provider.lower()
        model_name = self.config.model_name
        api_key = self.config.get_api_key_for_provider(provider_name)
        
        if provider_name == "openai":
            return OpenAIProvider(model_name=model_name, api_key=api_key)
        elif provider_name == "anthropic":
            return AnthropicProvider(model_name=model_name, api_key=api_key)
        else:
            return DummyProvider(model_name=model_name, api_key=api_key)
    
    def load_test_suite(self, suite_path: str) -> Dict[str, Any]:
        """Load a test suite from YAML file."""
        with open(suite_path, 'r') as f:
            return yaml.safe_load(f)
    
    def run_evaluation(self, suite_path: str) -> Dict[str, Any]:
        """Run evaluation for a test suite."""
        suite = self.load_test_suite(suite_path)
        results = {
            "suite_name": suite.get("name", "Unknown"),
            "age_group": suite.get("age_group", "Unknown"),
            "tests": [],
            "summary": {
                "total": 0,
                "passed": 0,
                "failed": 0,
                "average_score": 0.0
            }
        }
        
        total_score = 0.0
        
        for test_case in suite.get("tests", []):
            test_result = self._run_single_test(test_case)
            results["tests"].append(test_result)
            
            if test_result["evaluation"]["passed"]:
                results["summary"]["passed"] += 1
            else:
                results["summary"]["failed"] += 1
            
            total_score += test_result["evaluation"]["score"]
        
        results["summary"]["total"] = len(results["tests"])
        if results["summary"]["total"] > 0:
            results["summary"]["average_score"] = total_score / results["summary"]["total"]
        
        return results
    
    def _run_single_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single test case."""
        prompt = test_case["prompt"]
        rule_name = test_case.get("rule", "safety")
        expected = test_case.get("expected")
        
        # Generate response from AI provider
        try:
            response = self.provider.generate(prompt)
        except Exception as e:
            response = f"Error generating response: {str(e)}"
        
        # Evaluate response
        rule = self.rules.get(rule_name, self.rules["safety"])
        evaluation = rule.evaluate(response, expected)
        
        return {
            "id": test_case.get("id", "unknown"),
            "prompt": prompt,
            "response": response,
            "rule": rule_name,
            "expected": expected,
            "evaluation": evaluation.model_dump()
        }
    
    def run_all_suites(self, suites_dir: str = "suites") -> List[Dict[str, Any]]:
        """Run all test suites in the specified directory."""
        results = []
        suites_path = Path(suites_dir)
        
        for suite_file in suites_path.glob("*.yaml"):
            suite_results = self.run_evaluation(str(suite_file))
            results.append(suite_results)
        
        return results