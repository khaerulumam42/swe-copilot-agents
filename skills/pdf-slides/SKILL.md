---
name: pdf-slides
description: Generate professional PDF slide decks from structured JSON outlines with customizable branding, charts, and styling
version: 0.1.0
tools:
  - Write
  - Read
  - Bash
dependencies:
  - reportlab>=4.2.0
  - matplotlib>=3.9.0
  - pillow>=10.4.0
  - jinja2>=3.1.0
  - pyyaml>=6.0.0
author: claude
tags:
  - pdf
  - presentation
  - charts
  - slides
---

# PDF Slide Deck Generator

Generate professional PDF slide decks from structured JSON outlines with clean corporate styling, data visualizations, and customizable branding.

## Features

- **Multiple Slide Types**: Title, content, chart, stats, two-column, and section slides
- **Data Visualizations**: Bar, line, pie, and area charts with brand colors
- **Custom Branding**: Customizable colors, fonts, logos via YAML or inline JSON
- **Professional Styling**: Clean corporate design with 16:9 aspect ratio
- **Flexible Input**: JSON outline format for programmatic generation

## Usage

### Basic Example

```json
{
  "title": "Q4 2024 Business Review",
  "subtitle": "Strategic Growth Initiatives",
  "author": "Jane Smith",
  "date": "2025-01-15",
  "branding": {
    "primary_color": "#2E5BFF",
    "secondary_color": "#6C7A9C",
    "accent_color": "#00D9A0",
    "logo_path": "/path/to/logo.png"
  },
  "slides": [
    {
      "type": "title",
      "title": "Q4 2024 Business Review",
      "subtitle": "Strategic Growth Initiatives"
    },
    {
      "type": "content",
      "title": "Executive Summary",
      "points": [
        "Revenue increased 45% YoY",
        "Expanded to 3 new markets",
        "Launched 2 new product lines"
      ]
    },
    {
      "type": "chart",
      "title": "Revenue Growth",
      "chart_type": "bar",
      "data": {
        "labels": ["Q1", "Q2", "Q3", "Q4"],
        "values": [120, 145, 168, 198]
      }
    },
    {
      "type": "stats",
      "title": "Key Metrics",
      "stats": [
        {"label": "Total Revenue", "value": "$6.2M", "change": "+45%"},
        {"label": "New Customers", "value": "2,847", "change": "+32%"},
        {"label": "Customer Satisfaction", "value": "94%", "change": "+8%"}
      ]
    }
  ]
}
```

## Slide Types

### Title Slide
Cover slide with large title, subtitle, author, and date.
```json
{
  "type": "title",
  "title": "Presentation Title",
  "subtitle": "Optional Subtitle",
  "author": "Author Name",
  "date": "2025-01-15"
}
```

### Content Slide
Bullet points with optional subsections.
```json
{
  "type": "content",
  "title": "Slide Title",
  "points": [
    "First bullet point",
    "Second bullet point",
    {
      "heading": "Subsection",
      "points": ["Sub-point 1", "Sub-point 2"]
    }
  ]
}
```

### Chart Slide
Data visualization with automatic brand styling.
```json
{
  "type": "chart",
  "title": "Chart Title",
  "chart_type": "bar",
  "data": {
    "labels": ["A", "B", "C"],
    "values": [10, 20, 30]
  }
}
```
Supported chart types: `bar`, `line`, `pie`, `area`

### Stats Slide
Key metrics with change indicators.
```json
{
  "type": "stats",
  "title": "Key Metrics",
  "stats": [
    {"label": "Metric Name", "value": "$1.2M", "change": "+25%"},
    {"label": "Another Metric", "value": "3,456", "change": "-5%"}
  ]
}
```

### Two Column Slide
Side-by-side content for comparisons.
```json
{
  "type": "two_column",
  "title": "Comparison",
  "left": {
    "title": "Option A",
    "points": ["Feature 1", "Feature 2"]
  },
  "right": {
    "title": "Option B",
    "points": ["Feature 3", "Feature 4"]
  }
}
```

### Section Slide
Section divider with large section number/title.
```json
{
  "type": "section",
  "title": "Section Name",
  "section_number": "01",
  "subtitle": "Optional subtitle"
}
```

## Branding Configuration

### Inline Branding (JSON)
```json
{
  "branding": {
    "primary_color": "#2E5BFF",
    "secondary_color": "#6C7A9C",
    "accent_color": "#00D9A0",
    "logo_path": "/path/to/logo.png",
    "logo_width": 120,
    "logo_placement": "top-right"
  }
}
```

### YAML Config File
Create a `branding.yaml` file:
```yaml
colors:
  primary: "#2E5BFF"
  secondary: "#6C7A9C"
  accent: "#00D9A0"
  background: "#FFFFFF"
  text: "#1A1A2E"
  chart_colors:
    - "#2E5BFF"
    - "#00D9A0"
    - "#FFB800"
    - "#FF6B6B"

typography:
  fonts:
    title: "Inter-Bold"
    heading: "Inter-SemiBold"
    body: "Inter-Regular"
  sizes:
    title: 48
    heading: 32
    body: 18

layout:
  logo:
    placement: "top-right"
    width: 120
    path: "/path/to/logo.png"
```

## Command-Line Usage

```bash
# Generate from JSON file
python skill.py outline.json -o output.pdf

# Use custom branding config
python skill.py outline.json -o output.pdf -b branding.yaml

# Validate outline without generating
python skill.py outline.json --validate
```

## API Usage

```python
from src.generator import PDFSlideGenerator

# Create generator with branding
gen = PDFSlideGenerator(branding_config="config/default_branding.yaml")

# Generate from outline dict
pdf_bytes = gen.generate_from_outline(outline_dict)

# Or generate from JSON file
pdf_bytes = gen.generate_from_file("outline.json")

# Save to file
gen.save_pdf(outline_dict, "output.pdf")
```

## Output

- **Format**: PDF with 16:9 aspect ratio (1280x720)
- **Quality**: Print-ready, vector-based where possible
- **Compatibility**: Works with all PDF viewers and printers
