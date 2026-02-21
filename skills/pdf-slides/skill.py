#!/usr/bin/env python3
"""CLI entry point for PDF Slide Deck Generator skill."""

import argparse
import json
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.generator import PDFSlideGenerator
from src.utils.validators import Validators


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate professional PDF slide decks from JSON outlines",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate PDF from JSON outline
  python skill.py outline.json -o output.pdf

  # Use custom branding configuration
  python skill.py outline.json -o output.pdf -b branding.yaml

  # Validate outline without generating
  python skill.py outline.json --validate

  # Generate with inline branding override
  python skill.py outline.json -o output.pdf --primary "#FF5733"
        """
    )

    parser.add_argument(
        "outline",
        help="Path to JSON outline file or '-' for stdin"
    )

    parser.add_argument(
        "-o", "--output",
        required=True,
        help="Output PDF file path"
    )

    parser.add_argument(
        "-b", "--branding",
        help="Path to YAML branding configuration file"
    )

    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate outline without generating PDF"
    )

    # Branding override options
    parser.add_argument("--primary", help="Primary color hex (e.g., #2E5BFF)")
    parser.add_argument("--secondary", help="Secondary color hex")
    parser.add_argument("--accent", help="Accent color hex")
    parser.add_argument("--logo", help="Path to logo image file")

    args = parser.parse_args()

    # Load outline from file or stdin
    try:
        if args.outline == "-":
            outline = json.load(sys.stdin)
        else:
            outline_path = Path(args.outline)
            if not outline_path.exists():
                print(f"Error: Outline file not found: {args.outline}", file=sys.stderr)
                sys.exit(1)
            with open(outline_path, "r") as f:
                outline = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in outline: {e}", file=sys.stderr)
        sys.exit(1)

    # Validate outline
    errors = Validators.validate_outline(outline)
    if errors:
        print("Outline validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        sys.exit(1)

    if args.validate:
        print("✓ Outline is valid")
        sys.exit(0)

    # Prepare inline branding from CLI overrides
    inline_branding = {}
    if args.primary:
        inline_branding["primary_color"] = args.primary
    if args.secondary:
        inline_branding["secondary_color"] = args.secondary
    if args.accent:
        inline_branding["accent_color"] = args.accent
    if args.logo:
        inline_branding["logo_path"] = args.logo

    # Merge with outline branding if present
    if "branding" in outline:
        outline_branding = outline["branding"]
        # CLI overrides take precedence
        outline_branding.update(inline_branding)
        inline_branding = outline_branding

    # Create generator
    try:
        generator = PDFSlideGenerator(
            branding_config=args.branding,
            inline_branding=inline_branding if inline_branding else None,
        )
    except Exception as e:
        print(f"Error initializing generator: {e}", file=sys.stderr)
        sys.exit(1)

    # Generate PDF
    try:
        pdf_bytes = generator.generate_from_outline(outline)

        # Write to output file
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(pdf_bytes)

        print(f"✓ Generated PDF: {args.output}")
        print(f"  Pages: {len(outline.get('slides', []))}")

    except Exception as e:
        print(f"Error generating PDF: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
