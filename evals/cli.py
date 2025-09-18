#!/usr/bin/env python3
"""Command-line interface for KinderShield evaluations."""

import click
import sys
from pathlib import Path

# Add src to path so we can import kindershield
sys.path.insert(0, str(Path(__file__).parent / "src"))

from kindershield import Config, Runner
from kindershield.report import HTMLReportGenerator, SVGBadgeGenerator


@click.group()
@click.option('--config', '-c', help='Configuration file path')
@click.pass_context
def main(ctx, config):
    """KinderShield: AI safety evaluation framework for child-appropriate content."""
    ctx.ensure_object(dict)
    ctx.obj['config'] = Config.from_env()


@main.command()
@click.argument('suite_path', type=click.Path(exists=True))
@click.option('--output', '-o', default='reports', help='Output directory for reports')
@click.option('--html/--no-html', default=True, help='Generate HTML report')
@click.option('--badge/--no-badge', default=True, help='Generate SVG badge')
@click.pass_context
def run(ctx, suite_path, output, html, badge):
    """Run evaluation for a specific test suite."""
    config = ctx.obj['config']
    runner = Runner(config)
    
    click.echo(f"Running evaluation for: {suite_path}")
    
    # Run the evaluation
    results = runner.run_evaluation(suite_path)
    
    # Display summary
    summary = results['summary']
    click.echo(f"\nResults for {results['suite_name']} ({results['age_group']}):")
    click.echo(f"  Total tests: {summary['total']}")
    click.echo(f"  Passed: {summary['passed']}")
    click.echo(f"  Failed: {summary['failed']}")
    click.echo(f"  Average score: {summary['average_score']:.2f}")
    
    # Generate reports
    if html or badge:
        Path(output).mkdir(exist_ok=True)
        
        if html:
            html_gen = HTMLReportGenerator(output)
            html_path = html_gen.generate_report([results])
            click.echo(f"HTML report generated: {html_path}")
        
        if badge:
            badge_gen = SVGBadgeGenerator(output)
            badge_path = badge_gen.generate_badge([results])
            click.echo(f"SVG badge generated: {badge_path}")


@main.command()
@click.option('--suites-dir', '-s', default='suites', help='Directory containing test suites')
@click.option('--output', '-o', default='reports', help='Output directory for reports')
@click.option('--html/--no-html', default=True, help='Generate HTML report')
@click.option('--badge/--no-badge', default=True, help='Generate SVG badge')
@click.pass_context
def run_all(ctx, suites_dir, output, html, badge):
    """Run all test suites in the suites directory."""
    config = ctx.obj['config']
    runner = Runner(config)
    
    click.echo(f"Running all test suites in: {suites_dir}")
    
    # Run all evaluations
    results = runner.run_all_suites(suites_dir)
    
    if not results:
        click.echo("No test suites found!")
        return
    
    # Display summary for each suite
    total_tests = 0
    total_passed = 0
    
    for result in results:
        summary = result['summary']
        click.echo(f"\n{result['suite_name']} ({result['age_group']}):")
        click.echo(f"  Tests: {summary['passed']}/{summary['total']} passed")
        click.echo(f"  Score: {summary['average_score']:.2f}")
        
        total_tests += summary['total']
        total_passed += summary['passed']
    
    # Overall summary
    overall_pass_rate = total_passed / max(total_tests, 1) * 100
    click.echo(f"\nOverall Results:")
    click.echo(f"  Total tests: {total_tests}")
    click.echo(f"  Passed: {total_passed}")
    click.echo(f"  Pass rate: {overall_pass_rate:.1f}%")
    
    # Generate reports
    if html or badge:
        Path(output).mkdir(exist_ok=True)
        
        if html:
            html_gen = HTMLReportGenerator(output)
            html_path = html_gen.generate_report(results)
            click.echo(f"HTML report generated: {html_path}")
        
        if badge:
            badge_gen = SVGBadgeGenerator(output)
            badge_path = badge_gen.generate_badge(results)
            click.echo(f"SVG badge generated: {badge_path}")


@main.command()
@click.option('--suite', '-s', required=True, type=click.Path(exists=True), help='Path to test suite YAML file')
@click.option('--out', '-o', default='results', help='Output directory for results')
@click.option('--format', '-f', type=click.Choice(['json', 'csv', 'both']), default='both', help='Output format')
@click.pass_context
def eval(ctx, suite, out, format):
    """Run evaluation for a specific test suite and export results."""
    config = ctx.obj['config']
    runner = Runner(config)
    
    click.echo(f"🚀 Running evaluation for suite: {suite}")
    click.echo(f"📁 Output directory: {out}")
    
    try:
        # Run evaluation with export
        export_result = runner.run_suite_with_export(suite, out)
        
        # Display results summary
        results = export_result["results"]
        summary = results['summary']
        
        click.echo(f"\n📊 Results for {results['suite_name']} ({results['age_group']}):")
        click.echo(f"  ✅ Total tests: {summary['total']}")
        click.echo(f"  ✅ Passed: {summary['passed']}")
        click.echo(f"  ❌ Failed: {summary['failed']}")
        click.echo(f"  📈 Average score: {summary['average_score']:.2f}")
        
        # Show export files
        click.echo(f"\n📄 Exported files:")
        if format in ['json', 'both']:
            click.echo(f"  📋 JSON: {export_result['json_file']}")
        if format in ['csv', 'both']:
            click.echo(f"  📊 CSV: {export_result['csv_file']}")
            
    except Exception as e:
        click.echo(f"❌ Error running evaluation: {str(e)}", err=True)
        raise click.Abort()


@main.command()
@click.option('--suites-dir', '-s', default='suites', help='Directory containing test suites')
@click.option('--out', '-o', default='results', help='Output directory for results')
@click.option('--format', '-f', type=click.Choice(['json', 'csv', 'both']), default='both', help='Output format')
@click.pass_context
def eval_all(ctx, suites_dir, out, format):
    """Run all test suites and export consolidated results."""
    config = ctx.obj['config']
    runner = Runner(config)
    
    click.echo(f"🚀 Running all test suites in: {suites_dir}")
    click.echo(f"📁 Output directory: {out}")
    
    # Find all YAML files in the suites directory
    suites_path = Path(suites_dir)
    suite_files = list(suites_path.glob("*.yaml"))
    
    if not suite_files:
        click.echo(f"❌ No YAML test suites found in {suites_dir}")
        raise click.Abort()
    
    click.echo(f"📝 Found {len(suite_files)} test suites")
    
    try:
        # Run multiple suites with export
        export_result = runner.run_multiple_suites_with_export(
            [str(f) for f in suite_files], 
            out
        )
        
        if "error" in export_result:
            click.echo(f"❌ {export_result['error']}", err=True)
            raise click.Abort()
        
        # Display consolidated results
        consolidated = export_result["consolidated_results"]
        summary = consolidated['summary']
        
        click.echo(f"\n📊 Consolidated Results:")
        click.echo(f"  ✅ Total tests: {summary['total']}")
        click.echo(f"  ✅ Passed: {summary['passed']}")
        click.echo(f"  ❌ Failed: {summary['failed']}")
        click.echo(f"  📈 Average score: {summary['average_score']:.2f}")
        
        # Show individual suite summaries
        click.echo(f"\n📋 Individual Suite Results:")
        for suite_summary in consolidated.get('suite_summaries', []):
            name = suite_summary['suite_name']
            passed = suite_summary['passed']
            total = suite_summary['total']
            score = suite_summary['average_score']
            click.echo(f"  • {name}: {passed}/{total} passed (score: {score:.2f})")
        
        # Show export files
        click.echo(f"\n📄 Exported files:")
        if format in ['json', 'both']:
            click.echo(f"  📋 Consolidated JSON: {export_result['consolidated_json']}")
        if format in ['csv', 'both']:
            click.echo(f"  📊 Consolidated CSV: {export_result['consolidated_csv']}")
        
        # Show individual exports
        click.echo(f"\n📁 Individual suite exports:")
        for export in export_result['individual_exports']:
            suite_name = Path(export['suite_path']).stem
            click.echo(f"  • {suite_name}:")
            if format in ['json', 'both']:
                click.echo(f"    📋 JSON: {export['json_file']}")
            if format in ['csv', 'both']:
                click.echo(f"    📊 CSV: {export['csv_file']}")
                
    except Exception as e:
        click.echo(f"❌ Error running evaluations: {str(e)}", err=True)
        raise click.Abort()


@main.command()
@click.option('--provider', '-p', default=None, help='Provider to test (openai, anthropic, dummy)')
@click.pass_context
def test_provider(ctx, provider):
    """Test connection to AI provider."""
    config = ctx.obj['config']
    
    if provider:
        config.model_provider = provider
    
    runner = Runner(config)
    
    click.echo(f"🧪 Testing {config.model_provider} provider ({config.model_name})...")
    
    try:
        response = runner.provider.generate("Hello, this is a test!")
        click.echo(f"✅ Provider working! Response: {response}")
    except Exception as e:
        click.echo(f"❌ Provider error: {e}")


if __name__ == '__main__':
    main()