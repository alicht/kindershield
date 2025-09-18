#!/usr/bin/env python3
"""Simple CLI wrapper for KinderShield evaluations using Typer."""

import typer
import json
import sys
from pathlib import Path
from typing import Optional

# Add src to path so we can import kindershield
sys.path.insert(0, str(Path(__file__).parent / "src"))

from kindershield import Config, Runner
from kindershield.report import HTMLReportGenerator, SVGBadgeGenerator

app = typer.Typer(
    name="eval-cli",
    help="KinderShield evaluation CLI - Simple commands for running evals, generating reports, and creating badges"
)


@app.command("run-eval")
def run_eval(
    suite_yaml: str = typer.Argument(..., help="Path to the test suite YAML file"),
    output: Optional[str] = typer.Option("results.json", "--output", "-o", help="Output JSON file path"),
):
    """Run evaluation for a specific test suite and save results to JSON."""
    typer.echo(f"🚀 Running evaluation for suite: {suite_yaml}")
    
    try:
        # Initialize runner
        config = Config.from_env()
        runner = Runner(config)
        
        # Run evaluation
        results = runner.run_evaluation(suite_yaml)
        
        # Save results to JSON
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Display summary
        summary = results['summary']
        typer.echo(f"✅ Evaluation complete!")
        typer.echo(f"   Suite: {results['suite_name']} ({results['age_group']})")
        typer.echo(f"   Tests: {summary['passed']}/{summary['total']} passed")
        typer.echo(f"   Score: {summary['average_score']:.2f}")
        typer.echo(f"   Results saved to: {output_path}")
        
    except Exception as e:
        typer.echo(f"❌ Error running evaluation: {str(e)}", err=True)
        raise typer.Exit(1)


@app.command("generate-report")
def generate_report(
    results_json: str = typer.Argument(..., help="Path to the results JSON file"),
    output: Optional[str] = typer.Option("report.html", "--output", "-o", help="Output HTML file path"),
    output_dir: Optional[str] = typer.Option("reports", "--dir", "-d", help="Output directory for report"),
):
    """Generate HTML report from evaluation results JSON."""
    typer.echo(f"📊 Generating HTML report from: {results_json}")
    
    try:
        # Load results
        with open(results_json, 'r') as f:
            results_data = json.load(f)
        
        # Handle both single result and list of results
        if isinstance(results_data, dict):
            # Single result - wrap in list
            results = [results_data]
        elif isinstance(results_data, list):
            # Already a list
            results = results_data
        else:
            raise ValueError("Results JSON must contain a dict or list of evaluation results")
        
        # Generate HTML report
        html_gen = HTMLReportGenerator(output_dir)
        html_path = html_gen.generate_report(results, output)
        
        typer.echo(f"✅ HTML report generated: {html_path}")
        
    except Exception as e:
        typer.echo(f"❌ Error generating report: {str(e)}", err=True)
        raise typer.Exit(1)


@app.command("make-badge")
def make_badge(
    results_json: str = typer.Argument(..., help="Path to the results JSON file"),
    output: Optional[str] = typer.Option("badge.svg", "--output", "-o", help="Output SVG file path"),
    output_dir: Optional[str] = typer.Option("reports", "--dir", "-d", help="Output directory for badge"),
):
    """Generate SVG badge from evaluation results JSON."""
    typer.echo(f"🏷️  Generating SVG badge from: {results_json}")
    
    try:
        # Load results
        with open(results_json, 'r') as f:
            results_data = json.load(f)
        
        # Handle both single result and list of results
        if isinstance(results_data, dict):
            # Single result - wrap in list
            results = [results_data]
        elif isinstance(results_data, list):
            # Already a list
            results = results_data
        else:
            raise ValueError("Results JSON must contain a dict or list of evaluation results")
        
        # Generate SVG badge
        badge_gen = SVGBadgeGenerator(output_dir)
        badge_path = badge_gen.generate_badge(results, output)
        
        # Calculate and display pass rate
        total_tests = sum(r["summary"]["total"] for r in results)
        total_passed = sum(r["summary"]["passed"] for r in results)
        pass_rate = (total_passed / max(total_tests, 1)) * 100
        
        typer.echo(f"✅ SVG badge generated: {badge_path}")
        typer.echo(f"   Pass rate: {pass_rate:.1f}% ({total_passed}/{total_tests})")
        
    except Exception as e:
        typer.echo(f"❌ Error generating badge: {str(e)}", err=True)
        raise typer.Exit(1)


@app.command("info")
def info():
    """Show information about KinderShield configuration."""
    try:
        config = Config.from_env()
        typer.echo("🛡️  KinderShield Configuration:")
        typer.echo(f"   Provider: {config.model_provider}")
        typer.echo(f"   Model: {config.model_name}")
        typer.echo(f"   Log Level: {config.log_level}")
        
    except Exception as e:
        typer.echo(f"❌ Error loading configuration: {str(e)}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()