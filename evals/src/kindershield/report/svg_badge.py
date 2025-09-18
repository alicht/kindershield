"""SVG badge generation for KinderShield evaluations."""

from typing import List, Dict, Any
from pathlib import Path


class SVGBadgeGenerator:
    """Generator for SVG badges showing evaluation status."""
    
    def __init__(self, output_dir: str = "reports"):
        """Initialize the SVG badge generator."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_badge(self, results: List[Dict[str, Any]], output_filename: str = "badge.svg") -> str:
        """Generate an SVG badge from evaluation results."""
        # Calculate overall statistics
        total_tests = sum(r["summary"]["total"] for r in results)
        total_passed = sum(r["summary"]["passed"] for r in results)
        pass_rate = total_passed / max(total_tests, 1) * 100
        
        # Determine badge color based on pass rate
        if pass_rate >= 90:
            color = "#4c1"  # Green
            status = "excellent"
        elif pass_rate >= 80:
            color = "#97ca00"  # Light green
            status = "good"
        elif pass_rate >= 70:
            color = "#dfb317"  # Yellow
            status = "fair"
        elif pass_rate >= 60:
            color = "#fe7d37"  # Orange
            status = "poor"
        else:
            color = "#e05d44"  # Red
            status = "failing"
        
        # Generate SVG content
        svg_content = self._generate_svg(pass_rate, color)
        
        output_path = self.output_dir / output_filename
        with open(output_path, 'w') as f:
            f.write(svg_content)
        
        return str(output_path)
    
    def generate_suite_badge(self, result: Dict[str, Any], output_filename: str = None) -> str:
        """Generate an SVG badge for a single test suite."""
        if output_filename is None:
            suite_name = result.get("suite_name", "unknown").lower().replace(" ", "_")
            output_filename = f"{suite_name}_badge.svg"
        
        summary = result.get("summary", {})
        total = summary.get("total", 0)
        passed = summary.get("passed", 0)
        pass_rate = (passed / max(total, 1)) * 100
        
        # Determine badge color based on pass rate
        if pass_rate >= 90:
            color = "#4c1"  # Green
        elif pass_rate >= 80:
            color = "#97ca00"  # Light green
        elif pass_rate >= 70:
            color = "#dfb317"  # Yellow
        elif pass_rate >= 60:
            color = "#fe7d37"  # Orange
        else:
            color = "#e05d44"  # Red
        
        # Generate SVG content
        svg_content = self._generate_svg(pass_rate, color, result.get("suite_name"))
        
        output_path = self.output_dir / output_filename
        with open(output_path, 'w') as f:
            f.write(svg_content)
        
        return str(output_path)
    
    def _generate_svg(self, pass_rate: float, color: str, suite_name: str = None) -> str:
        """Generate the SVG badge content."""
        score_text = f"{pass_rate:.1f}%"
        label_text = suite_name if suite_name else "KidSafe"
        
        # Calculate dynamic widths based on text length
        label_width = max(len(label_text) * 6 + 10, 60)
        value_width = max(len(score_text) * 7 + 10, 40)
        total_width = label_width + value_width
        
        return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{total_width}" height="20" role="img" aria-label="{label_text}: {score_text}">
    <title>{label_text}: {score_text}</title>
    <linearGradient id="s" x2="0" y2="100%">
        <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
        <stop offset="1" stop-opacity=".1"/>
    </linearGradient>
    <clipPath id="r">
        <rect width="{total_width}" height="20" rx="3" fill="#fff"/>
    </clipPath>
    <g clip-path="url(#r)">
        <rect width="{label_width}" height="20" fill="#555"/>
        <rect x="{label_width}" width="{value_width}" height="20" fill="{color}"/>
        <rect width="{total_width}" height="20" fill="url(#s)"/>
    </g>
    <g fill="#fff" text-anchor="middle" font-family="Verdana,Geneva,DejaVu Sans,sans-serif" text-rendering="geometricPrecision" font-size="110">
        <text aria-hidden="true" x="{label_width * 0.5 * 10}" y="150" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="{(label_width - 10) * 10}">{label_text}</text>
        <text x="{label_width * 0.5 * 10}" y="140" transform="scale(.1)" fill="#fff" textLength="{(label_width - 10) * 10}">{label_text}</text>
        <text aria-hidden="true" x="{(label_width + value_width * 0.5) * 10}" y="150" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="{(value_width - 10) * 10}">{score_text}</text>
        <text x="{(label_width + value_width * 0.5) * 10}" y="140" transform="scale(.1)" fill="#fff" textLength="{(value_width - 10) * 10}">{score_text}</text>
    </g>
</svg>"""