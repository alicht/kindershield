"""HTML report generation for KinderShield evaluations."""

from typing import List, Dict, Any
from pathlib import Path
from jinja2 import Template


class HTMLReportGenerator:
    """Generator for HTML evaluation reports."""
    
    def __init__(self, output_dir: str = "reports"):
        """Initialize the HTML report generator."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_report(self, results: List[Dict[str, Any]], output_filename: str = "report.html") -> str:
        """Generate an HTML report from evaluation results."""
        template = Template(self._get_template())
        
        # Calculate overall statistics
        total_tests = sum(r["summary"]["total"] for r in results)
        total_passed = sum(r["summary"]["passed"] for r in results)
        total_failed = sum(r["summary"]["failed"] for r in results)
        overall_score = sum(r["summary"]["average_score"] * r["summary"]["total"] for r in results) / max(total_tests, 1)
        
        html_content = template.render(
            results=results,
            total_tests=total_tests,
            total_passed=total_passed,
            total_failed=total_failed,
            overall_score=overall_score,
            pass_rate=total_passed / max(total_tests, 1) * 100
        )
        
        output_path = self.output_dir / output_filename
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        return str(output_path)
    
    def _get_template(self) -> str:
        """Get the HTML template for reports."""
        return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KinderShield Evaluation Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 20px;
        }
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .metric {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 6px;
            text-align: center;
        }
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            color: #2c3e50;
        }
        .metric-label {
            color: #7f8c8d;
            margin-top: 5px;
        }
        .suite {
            margin-bottom: 30px;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            overflow: hidden;
        }
        .suite-header {
            background: #34495e;
            color: white;
            padding: 15px 20px;
            font-weight: bold;
        }
        .test {
            padding: 15px 20px;
            border-bottom: 1px solid #f0f0f0;
        }
        .test:last-child {
            border-bottom: none;
        }
        .test-passed {
            background-color: #d4edda;
            border-left: 4px solid #28a745;
        }
        .test-failed {
            background-color: #f8d7da;
            border-left: 4px solid #dc3545;
        }
        .test-id {
            font-weight: bold;
            margin-bottom: 5px;
        }
        .test-details {
            font-size: 0.9em;
            color: #666;
        }
        .score {
            float: right;
            font-weight: bold;
            padding: 2px 8px;
            border-radius: 4px;
            color: white;
        }
        .score-high { background-color: #28a745; }
        .score-medium { background-color: #ffc107; color: #000; }
        .score-low { background-color: #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🛡️ KinderShield Evaluation Report</h1>
            <p>AI Safety Assessment for Child-Appropriate Content</p>
        </div>
        
        <div class="summary">
            <div class="metric">
                <div class="metric-value">{{ total_tests }}</div>
                <div class="metric-label">Total Tests</div>
            </div>
            <div class="metric">
                <div class="metric-value">{{ total_passed }}</div>
                <div class="metric-label">Passed</div>
            </div>
            <div class="metric">
                <div class="metric-value">{{ total_failed }}</div>
                <div class="metric-label">Failed</div>
            </div>
            <div class="metric">
                <div class="metric-value">{{ "%.1f"|format(pass_rate) }}%</div>
                <div class="metric-label">Pass Rate</div>
            </div>
            <div class="metric">
                <div class="metric-value">{{ "%.2f"|format(overall_score) }}</div>
                <div class="metric-label">Overall Score</div>
            </div>
        </div>
        
        {% for suite in results %}
        <div class="suite">
            <div class="suite-header">
                {{ suite.suite_name }} ({{ suite.age_group }})
                <span style="float: right;">
                    {{ suite.summary.passed }}/{{ suite.summary.total }} passed
                    ({{ "%.1f"|format(suite.summary.average_score * 100) }}%)
                </span>
            </div>
            
            {% for test in suite.tests %}
            <div class="test {{ 'test-passed' if test.evaluation.passed else 'test-failed' }}">
                <div class="test-id">
                    Test {{ test.id }}
                    <span class="score {{ 'score-high' if test.evaluation.score >= 0.8 else ('score-medium' if test.evaluation.score >= 0.5 else 'score-low') }}">
                        {{ "%.2f"|format(test.evaluation.score) }}
                    </span>
                </div>
                <div class="test-details">
                    <strong>Prompt:</strong> {{ test.prompt }}<br>
                    <strong>Response:</strong> {{ test.response }}<br>
                    <strong>Rule:</strong> {{ test.rule }}<br>
                    <strong>Result:</strong> {{ test.evaluation.reason }}
                </div>
            </div>
            {% endfor %}
        </div>
        {% endfor %}
    </div>
</body>
</html>
        """