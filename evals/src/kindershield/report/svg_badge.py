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
        svg_content = self._generate_svg(pass_rate, color, status)
        
        output_path = self.output_dir / output_filename
        with open(output_path, 'w') as f:
            f.write(svg_content)
        
        return str(output_path)
    
    def _generate_svg(self, pass_rate: float, color: str, status: str) -> str:
        """Generate the SVG badge content."""
        score_text = f"{pass_rate:.1f}%"
        
        return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="140" height="20">
    <linearGradient id="b" x2="0" y2="100%">
        <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
        <stop offset="1" stop-opacity=".1"/>
    </linearGradient>
    <clipPath id="a">
        <rect width="140" height="20" rx="3" fill="#fff"/>
    </clipPath>
    <g clip-path="url(#a)">
        <path fill="#555" d="M0 0h75v20H0z"/>
        <path fill="{color}" d="M75 0h65v20H75z"/>
        <path fill="url(#b)" d="M0 0h140v20H0z"/>
    </g>
    <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="110">
        <text x="385" y="150" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="650">KinderShield</text>
        <text x="385" y="140" transform="scale(.1)" textLength="650">KinderShield</text>
        <text x="1065" y="150" fill="#010101" fill-opacity=".3" transform="scale(.1)" textLength="550">{score_text}</text>
        <text x="1065" y="140" transform="scale(.1)" textLength="550">{score_text}</text>
    </g>
</svg>"""