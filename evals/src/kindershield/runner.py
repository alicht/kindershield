"""Main evaluation runner for KinderShield."""

from typing import List, Dict, Any, Optional
import yaml
import json
import csv
import os
import logging
from datetime import datetime
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
        self._setup_logging()
    
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
        # Get rule from domain or explicit rule field
        rule_name = test_case.get("rule", test_case.get("domain", "safety"))
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
    
    def _setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=getattr(logging, self.config.log_level.upper(), logging.INFO),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def save_results_json(self, results: Dict[str, Any], output_path: str) -> str:
        """Save evaluation results to JSON file."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Add metadata
        results_with_metadata = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "provider": self.config.model_provider,
                "model": self.config.model_name,
                "kindershield_version": "0.1.0"
            },
            **results
        }
        
        with open(output_file, 'w') as f:
            json.dump(results_with_metadata, f, indent=2, default=str)
        
        self.logger.info(f"Results saved to JSON: {output_file}")
        return str(output_file)
    
    def save_results_csv(self, results: Dict[str, Any], output_path: str) -> str:
        """Save evaluation results to CSV file."""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            if not results.get("tests"):
                self.logger.warning("No test results to save to CSV")
                return str(output_file)
            
            # Define CSV headers
            fieldnames = [
                'test_id', 'suite_name', 'age_group', 'domain', 'skill', 
                'prompt', 'response', 'rule', 'expected_type', 'expected_value',
                'evaluation_passed', 'evaluation_score', 'evaluation_reason',
                'timestamp', 'provider', 'model'
            ]
            
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            timestamp = datetime.now().isoformat()
            
            for test in results.get("tests", []):
                # Handle expected values (could be dict or simple value)
                expected = test.get("expected", {})
                if isinstance(expected, dict):
                    expected_type = expected.get("type", "")
                    expected_value = expected.get("value", "")
                else:
                    expected_type = "simple"
                    expected_value = str(expected) if expected is not None else ""
                
                row = {
                    'test_id': test.get("id", ""),
                    'suite_name': results.get("suite_name", ""),
                    'age_group': results.get("age_group", ""),
                    'domain': test.get("domain", ""),
                    'skill': test.get("skill", ""),
                    'prompt': test.get("prompt", ""),
                    'response': test.get("response", ""),
                    'rule': test.get("rule", ""),
                    'expected_type': expected_type,
                    'expected_value': expected_value,
                    'evaluation_passed': test.get("evaluation", {}).get("passed", False),
                    'evaluation_score': test.get("evaluation", {}).get("score", 0.0),
                    'evaluation_reason': test.get("evaluation", {}).get("reason", ""),
                    'timestamp': timestamp,
                    'provider': self.config.model_provider,
                    'model': self.config.model_name
                }
                writer.writerow(row)
        
        self.logger.info(f"Results saved to CSV: {output_file}")
        return str(output_file)
    
    def run_suite_with_export(self, suite_path: str, output_dir: str = "results") -> Dict[str, str]:
        """Run evaluation suite and export results to JSON and CSV."""
        self.logger.info(f"Starting evaluation of suite: {suite_path}")
        
        # Run the evaluation
        results = self.run_evaluation(suite_path)
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Generate base filename from suite name and timestamp
        suite_name = Path(suite_path).stem
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = f"{suite_name}_{timestamp}"
        
        # Export to both formats
        json_file = self.save_results_json(results, output_path / f"{base_filename}.json")
        csv_file = self.save_results_csv(results, output_path / f"{base_filename}.csv")
        
        # Log summary
        summary = results.get("summary", {})
        self.logger.info(
            f"Evaluation complete. Suite: {results.get('suite_name')}, "
            f"Tests: {summary.get('total', 0)}, "
            f"Passed: {summary.get('passed', 0)}, "
            f"Score: {summary.get('average_score', 0.0):.2f}"
        )
        
        return {
            "json_file": json_file,
            "csv_file": csv_file,
            "results": results
        }
    
    def run_multiple_suites_with_export(self, suite_paths: List[str], output_dir: str = "results") -> Dict[str, Any]:
        """Run multiple evaluation suites and export consolidated results."""
        self.logger.info(f"Starting evaluation of {len(suite_paths)} suites")
        
        all_results = []
        individual_exports = []
        
        for suite_path in suite_paths:
            try:
                export_result = self.run_suite_with_export(suite_path, output_dir)
                all_results.append(export_result["results"])
                individual_exports.append({
                    "suite_path": suite_path,
                    "json_file": export_result["json_file"],
                    "csv_file": export_result["csv_file"]
                })
            except Exception as e:
                self.logger.error(f"Failed to process suite {suite_path}: {str(e)}")
                continue
        
        # Create consolidated results
        if all_results:
            consolidated = self._create_consolidated_results(all_results)
            
            # Export consolidated results
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            consolidated_json = self.save_results_json(
                consolidated, 
                Path(output_dir) / f"consolidated_{timestamp}.json"
            )
            consolidated_csv = self.save_results_csv(
                consolidated, 
                Path(output_dir) / f"consolidated_{timestamp}.csv"
            )
            
            return {
                "individual_exports": individual_exports,
                "consolidated_json": consolidated_json,
                "consolidated_csv": consolidated_csv,
                "consolidated_results": consolidated
            }
        else:
            self.logger.error("No suites were successfully processed")
            return {"individual_exports": [], "error": "No suites processed successfully"}
    
    def _create_consolidated_results(self, all_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create consolidated results from multiple suite results."""
        consolidated_tests = []
        total_tests = 0
        total_passed = 0
        total_score = 0.0
        
        suite_summaries = []
        
        for result in all_results:
            # Add all tests to consolidated list
            for test in result.get("tests", []):
                # Add suite info to each test
                test_with_suite = test.copy()
                test_with_suite["suite_name"] = result.get("suite_name", "Unknown")
                test_with_suite["suite_age_group"] = result.get("age_group", "Unknown")
                consolidated_tests.append(test_with_suite)
            
            # Aggregate summary stats
            summary = result.get("summary", {})
            suite_total = summary.get("total", 0)
            suite_passed = summary.get("passed", 0)
            suite_score = summary.get("average_score", 0.0)
            
            total_tests += suite_total
            total_passed += suite_passed
            total_score += suite_score * suite_total  # Weight by number of tests
            
            suite_summaries.append({
                "suite_name": result.get("suite_name", "Unknown"),
                "age_group": result.get("age_group", "Unknown"),
                "total": suite_total,
                "passed": suite_passed,
                "failed": suite_total - suite_passed,
                "average_score": suite_score
            })
        
        return {
            "suite_name": "Consolidated Results",
            "age_group": "Multiple",
            "suite_summaries": suite_summaries,
            "tests": consolidated_tests,
            "summary": {
                "total": total_tests,
                "passed": total_passed,
                "failed": total_tests - total_passed,
                "average_score": total_score / max(total_tests, 1)
            }
        }