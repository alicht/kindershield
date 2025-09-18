"""HTML report generation for KinderShield evaluations."""

from typing import List, Dict, Any
from pathlib import Path
from jinja2 import Template
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import base64
import io
import os


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
        
        # Generate chart data URLs
        pass_rate_chart = self._generate_pass_rate_chart(results)
        score_distribution_chart = self._generate_score_distribution_chart(results)
        
        html_content = template.render(
            results=results,
            total_tests=total_tests,
            total_passed=total_passed,
            total_failed=total_failed,
            overall_score=overall_score,
            pass_rate=total_passed / max(total_tests, 1) * 100,
            pass_rate_chart=pass_rate_chart,
            score_distribution_chart=score_distribution_chart
        )
        
        output_path = self.output_dir / output_filename
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        return str(output_path)
    
    def _generate_pass_rate_chart(self, results: List[Dict[str, Any]]) -> str:
        """Generate a bar chart showing pass rates by test suite."""
        plt.style.use('default')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        suite_names = []
        pass_rates = []
        colors = []
        
        for result in results:
            suite_name = result.get("suite_name", "Unknown")
            summary = result.get("summary", {})
            total = summary.get("total", 0)
            passed = summary.get("passed", 0)
            
            if total > 0:
                pass_rate = (passed / total) * 100
                pass_rates.append(pass_rate)
                suite_names.append(suite_name)
                
                # Color coding based on pass rate
                if pass_rate >= 80:
                    colors.append('#28a745')  # Green
                elif pass_rate >= 60:
                    colors.append('#ffc107')  # Yellow
                else:
                    colors.append('#dc3545')  # Red
        
        if not suite_names:
            return ""
        
        bars = ax.bar(suite_names, pass_rates, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
        
        # Add value labels on bars
        for bar, rate in zip(bars, pass_rates):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                   f'{rate:.1f}%', ha='center', va='bottom', fontweight='bold')
        
        ax.set_title('Test Suite Pass Rates', fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel('Pass Rate (%)', fontsize=12)
        ax.set_xlabel('Test Suite', fontsize=12)
        ax.set_ylim(0, 105)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Rotate x-axis labels if needed
        if len(suite_names) > 3:
            plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        
        # Convert to base64 for embedding
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close()
        
        return f"data:image/png;base64,{image_base64}"
    
    def _generate_score_distribution_chart(self, results: List[Dict[str, Any]]) -> str:
        """Generate a chart showing score distribution across all tests."""
        plt.style.use('default')
        fig, ax = plt.subplots(figsize=(10, 6))
        
        all_scores = []
        for result in results:
            for test in result.get("tests", []):
                score = test.get("evaluation", {}).get("score", 0)
                all_scores.append(score)
        
        if not all_scores:
            return ""
        
        # Create score bins
        bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
        labels = ['0-20%', '20-40%', '40-60%', '60-80%', '80-100%']
        colors = ['#dc3545', '#fd7e14', '#ffc107', '#20c997', '#28a745']
        
        import numpy as np
        counts, _ = np.histogram(all_scores, bins=bins)
        
        bars = ax.bar(labels, counts, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                       f'{int(count)}', ha='center', va='bottom', fontweight='bold')
        
        ax.set_title('Score Distribution Across All Tests', fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel('Number of Tests', fontsize=12)
        ax.set_xlabel('Score Range', fontsize=12)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        plt.tight_layout()
        
        # Convert to base64 for embedding
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        plt.close()
        
        return f"data:image/png;base64,{image_base64}"
    
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
        .charts-section {
            margin: 30px 0;
        }
        .chart-container {
            margin: 20px 0;
            text-align: center;
        }
        .chart-container img {
            max-width: 100%;
            height: auto;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stats-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            border-radius: 6px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stats-table th, .stats-table td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }
        .stats-table th {
            background-color: #34495e;
            color: white;
            font-weight: bold;
        }
        .stats-table tr:hover {
            background-color: #f8f9fa;
        }
        .stats-table tr:last-child td {
            border-bottom: none;
        }
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

        <!-- Charts Section -->
        {% if pass_rate_chart or score_distribution_chart %}
        <div class="charts-section">
            <h2>📊 Performance Charts</h2>
            
            {% if pass_rate_chart %}
            <div class="chart-container">
                <h3>Pass Rates by Test Suite</h3>
                <img src="{{ pass_rate_chart }}" alt="Pass Rate Chart">
            </div>
            {% endif %}
            
            {% if score_distribution_chart %}
            <div class="chart-container">
                <h3>Score Distribution</h3>
                <img src="{{ score_distribution_chart }}" alt="Score Distribution Chart">
            </div>
            {% endif %}
        </div>
        {% endif %}

        <!-- Suite Summary Table -->
        {% if results|length > 1 %}
        <div class="suite-summary">
            <h2>📋 Test Suite Summary</h2>
            <table class="stats-table">
                <thead>
                    <tr>
                        <th>Suite Name</th>
                        <th>Age Group</th>
                        <th>Total Tests</th>
                        <th>Passed</th>
                        <th>Failed</th>
                        <th>Pass Rate</th>
                        <th>Average Score</th>
                    </tr>
                </thead>
                <tbody>
                    {% for suite in results %}
                    <tr>
                        <td><strong>{{ suite.suite_name }}</strong></td>
                        <td>{{ suite.age_group }}</td>
                        <td>{{ suite.summary.total }}</td>
                        <td style="color: #28a745;">{{ suite.summary.passed }}</td>
                        <td style="color: #dc3545;">{{ suite.summary.failed }}</td>
                        <td>{{ "%.1f"|format((suite.summary.passed / suite.summary.total * 100) if suite.summary.total > 0 else 0) }}%</td>
                        <td>{{ "%.2f"|format(suite.summary.average_score) }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        {% endif %}
        
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