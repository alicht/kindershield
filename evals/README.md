# KinderShield Evaluation Framework

Python package for running KinderShield AI safety evaluations.

## Quick Start

### Installation

```bash
pip install -e .
```

### Running Evaluations

#### Using the CLI Module

Run a single evaluation suite:
```bash
python -m kindershield.cli run-eval suites/math_5_7.yaml
```

Generate an HTML report from results:
```bash
python -m kindershield.cli generate-report results.json
```

Create an SVG badge from results:
```bash
python -m kindershield.cli make-badge results.json
```

#### Using the Standalone CLI

Alternatively, use the standalone Typer CLI:
```bash
# Run evaluation and save to JSON
python eval_cli.py run-eval suites/math_5_7.yaml --output my_results.json

# Generate HTML report
python eval_cli.py generate-report my_results.json --output my_report.html

# Create SVG badge
python eval_cli.py make-badge my_results.json --output my_badge.svg
```

### Sample Evaluations

Test with the included sample fixtures:

```bash
# Basic math evaluation
python -m kindershield.cli run-eval tests/fixtures/sample_basic_math.yaml

# Safety content evaluation
python -m kindershield.cli run-eval tests/fixtures/sample_safety_check.yaml

# Reading skills evaluation
python -m kindershield.cli run-eval tests/fixtures/sample_reading_skills.yaml
```

### Configuration

Set your AI provider and model via environment variables:

```bash
export MODEL_PROVIDER=openai
export MODEL_NAME=gpt-4
export OPENAI_API_KEY=your_key_here
```

Or for Anthropic:

```bash
export MODEL_PROVIDER=anthropic
export MODEL_NAME=claude-3-haiku-20240307
export ANTHROPIC_API_KEY=your_key_here
```

For testing without API keys, use the dummy provider (default):

```bash
export MODEL_PROVIDER=dummy
export MODEL_NAME=dummy-small
```

## Project Structure

```
evals/
├── src/kindershield/          # Main package
│   ├── config.py             # Configuration management
│   ├── providers/            # AI provider implementations
│   ├── scoring/              # Evaluation rules and scoring
│   └── report/               # HTML and SVG report generation
├── suites/                   # Test suite definitions
├── tests/fixtures/           # Sample evaluation files
├── cli.py                    # Click-based CLI (legacy)
├── eval_cli.py              # Typer-based CLI (new)
└── pyproject.toml           # Package configuration
```

See the main project README for full documentation.