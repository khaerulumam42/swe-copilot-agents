"""Main PDF slide deck generator orchestrator."""

from io import BytesIO
from pathlib import Path
from typing import Optional

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import landscape, A4

from .slides import (
    TitleSlide,
    ContentSlide,
    ChartSlide,
    StatsSlide,
    TwoColumnSlide,
    SectionSlide,
)
from .branding.brand_manager import BrandManager
from .utils.validators import Validators


class PDFSlideGenerator:
    """Main orchestrator for generating PDF slide decks.

    Takes a JSON outline and produces a professionally styled PDF.
    """

    # Slide type mapping
    SLIDE_CLASSES = {
        "title": TitleSlide,
        "content": ContentSlide,
        "chart": ChartSlide,
        "stats": StatsSlide,
        "two_column": TwoColumnSlide,
        "section": SectionSlide,
    }

    def __init__(
        self,
        branding_config: Optional[str | Path] = None,
        inline_branding: Optional[dict] = None,
    ):
        """Initialize the PDF generator.

        Args:
            branding_config: Optional path to YAML branding config
            inline_branding: Optional inline branding dict from JSON
        """
        self.brand_manager = BrandManager(branding_config, inline_branding)
        self._update_brand_metadata(inline_branding or {})

    def _update_brand_metadata(self, outline: dict) -> None:
        """Update brand manager with deck metadata from outline.

        Args:
            outline: Full outline dict
        """
        # Update author and date from outline root level
        if "author" in outline:
            self.brand_manager.deck_author = outline["author"]
        if "date" in outline:
            self.brand_manager.deck_date = outline["date"]

    def generate_from_outline(self, outline: dict) -> bytes:
        """Generate PDF from outline dictionary.

        Args:
            outline: Complete outline with slides array

        Returns:
            PDF file as bytes

        Raises:
            ValueError: If outline validation fails
        """
        # Validate outline
        errors = Validators.validate_outline(outline)
        if errors:
            raise ValueError(f"Outline validation failed:\n" + "\n".join(errors))

        # Update branding with outline metadata
        self._update_brand_metadata(outline)

        # Create PDF buffer
        buffer = BytesIO()

        # Create canvas with 16:9 landscape format
        from reportlab.lib.units import inch
        width = 10 * inch
        height = 5.625 * inch
        canvas = Canvas(buffer, pagesize=(width, height))

        # Get slides from outline
        slides_data = outline.get("slides", [])
        total_slides = len(slides_data)

        # Generate each slide
        for i, slide_data in enumerate(slides_data):
            # Create new page for each slide (except first which is already created)
            if i > 0:
                canvas.showPage()

            # Create slide instance
            slide = self._create_slide(slide_data)

            # Render the slide
            slide.render(canvas)

            # Add footer with page numbers (if not a title slide)
            if slide_data.get("type") != "title":
                # Page numbers are 1-indexed for human reading
                # Title slide is usually unnumbered or page 1
                page_num = i + 1
                slide.render_footer(canvas, page_num, total_slides)

        # Save PDF
        canvas.save()

        # Return bytes
        buffer.seek(0)
        return buffer.read()

    def _create_slide(self, slide_data: dict):
        """Create a slide instance from data.

        Args:
            slide_data: Slide configuration dict

        Returns:
            BaseSlide instance

        Raises:
            ValueError: If slide type is unknown
        """
        slide_type = slide_data.get("type", "content")

        slide_class = self.SLIDE_CLASSES.get(slide_type)
        if not slide_class:
            raise ValueError(
                f"Unknown slide type: {slide_type}. "
                f"Supported types: {', '.join(self.SLIDE_CLASSES.keys())}"
            )

        return slide_class(slide_data, self.brand_manager)

    def generate_from_file(self, json_path: str | Path) -> bytes:
        """Generate PDF from JSON file.

        Args:
            json_path: Path to JSON outline file

        Returns:
            PDF file as bytes

        Raises:
            FileNotFoundError: If JSON file doesn't exist
            ValueError: If JSON is invalid
        """
        import json

        json_path = Path(json_path)
        if not json_path.exists():
            raise FileNotFoundError(f"Outline file not found: {json_path}")

        try:
            with open(json_path, "r") as f:
                outline = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {json_path}: {e}")

        return self.generate_from_outline(outline)

    def save_pdf(self, outline: dict, output_path: str | Path) -> None:
        """Generate and save PDF to file.

        Args:
            outline: Complete outline with slides array
            output_path: Where to save the PDF
        """
        pdf_bytes = self.generate_from_outline(outline)

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "wb") as f:
            f.write(pdf_bytes)

    def save_pdf_from_file(self, json_path: str | Path, output_path: str | Path) -> None:
        """Generate PDF from JSON file and save to output path.

        Args:
            json_path: Path to JSON outline file
            output_path: Where to save the PDF
        """
        pdf_bytes = self.generate_from_file(json_path)

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "wb") as f:
            f.write(pdf_bytes)
