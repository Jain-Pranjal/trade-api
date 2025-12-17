from pathlib import Path
from datetime import datetime

def generate_markdown(sector: str, analysis: str) -> str:
    """Generate markdown report content"""
    return f"""# {sector.title()} Sector Market Analysis (India)

**Generated on:** {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

## Overview
This report provides a trade opportunity analysis for the **{sector}** sector.

## Market Analysis & Trade Insights
{analysis}

## Disclaimer
This report is AI-generated and for educational purposes only.
"""

def save_markdown_report(sector: str, report_content: str) -> str:
    """Save markdown report to local file and return file path"""
    
    # creating reports directory if it doesn't exist
    reports_dir = Path(__file__).parent.parent / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    # Generating filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{sector.lower().replace(' ', '_')}_{timestamp}.md"
    filepath = reports_dir / filename
    
    # Write report to file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    return str(filepath)
