"""PDF helper utilities for ReportLab."""

from typing import Tuple
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.colors import Color
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


class PDFHelpers:
    """Helper functions for common PDF operations."""

    @staticmethod
    def draw_text(
        canvas: Canvas,
        text: str,
        x: float,
        y: float,
        font: str,
        size: int,
        color: Color,
        align: str = "left",
        max_width: float | None = None,
    ) -> float:
        """Draw text with optional wrapping.

        Args:
            canvas: ReportLab Canvas
            text: Text to draw
            x: X position
            y: Y position
            font: Font name
            size: Font size
            color: Text color
            align: Text alignment (left, center, right)
            max_width: Optional max width for wrapping

        Returns:
            Y position after drawing (for chaining)
        """
        canvas.setFillColor(color)
        canvas.setFont(font, size)

        if max_width and len(text) * size * 0.5 > max_width:
            # Use Paragraph for text wrapping
            style = ParagraphStyle(
                "custom",
                fontName=font,
                fontSize=size,
                textColor=color,
                alignment={"left": 0, "center": 1, "right": 2}[align],
            )
            p = Paragraph(text, style)
            w, h = p.wrap(max_width, 500)
            p.drawOn(canvas, x, y - h)
            return y - h

        # Simple text drawing
        if align == "center":
            canvas.drawCentredString(x, y, text)
        elif align == "right":
            canvas.drawRightString(x, y, text)
        else:
            canvas.drawString(x, y, text)

        return y

    @staticmethod
    def draw_bullet_point(
        canvas: Canvas,
        text: str,
        x: float,
        y: float,
        font: str,
        size: int,
        color: Color,
        bullet_color: Color | None = None,
        indent: float = 20,
    ) -> float:
        """Draw a bullet point with text.

        Args:
            canvas: ReportLab Canvas
            text: Bullet text
            x: X position
            y: Y position
            font: Font name
            size: Font size
            color: Text color
            bullet_color: Optional bullet color (defaults to text color)
            indent: Bullet indent

        Returns:
            Y position after drawing
        """
        bullet_color = bullet_color or color

        # Draw bullet
        canvas.setFillColor(bullet_color)
        canvas.setFont(font, size)
        canvas.drawString(x, y, "•")

        # Draw text with indent
        return PDFHelpers.draw_text(
            canvas, text, x + indent, y, font, size, color, max_width=500
        )

    @staticmethod
    def draw_box(
        canvas: Canvas,
        x: float,
        y: float,
        width: float,
        height: float,
        fill_color: Color | None = None,
        stroke_color: Color | None = None,
        stroke_width: float = 1,
        corner_radius: float = 0,
    ) -> None:
        """Draw a rectangular box with optional fill and stroke.

        Args:
            canvas: ReportLab Canvas
            x: X position
            y: Y position
            width: Box width
            height: Box height
            fill_color: Optional fill color
            stroke_color: Optional stroke color
            stroke_width: Stroke width
            corner_radius: Corner radius for rounded corners
        """
        if corner_radius > 0:
            canvas.roundRect(
                x, y, width, height,
                radius=corner_radius,
                fill=fill_color is not None,
                stroke=stroke_color is not None
            )
        else:
            if fill_color:
                canvas.setFillColor(fill_color)
            if stroke_color:
                canvas.setStrokeColor(stroke_color)
            canvas.setLineWidth(stroke_width)
            canvas.rect(x, y, width, height, fill=fill_color is not None, stroke=stroke_color is not None)

    @staticmethod
    def draw_divider(
        canvas: Canvas,
        x: float,
        y: float,
        width: float,
        color: Color,
        thickness: float = 1,
    ) -> None:
        """Draw a horizontal divider line.

        Args:
            canvas: ReportLab Canvas
            x: X start position
            y: Y position
            width: Line width
            color: Line color
            thickness: Line thickness
        """
        canvas.setStrokeColor(color)
        canvas.setLineWidth(thickness)
        canvas.line(x, y, x + width, y)

    @staticmethod
    def measure_text(
        canvas: Canvas,
        text: str,
        font: str,
        size: int,
    ) -> Tuple[float, float]:
        """Measure text dimensions.

        Args:
            canvas: ReportLab Canvas
            text: Text to measure
            font: Font name
            size: Font size

        Returns:
            Tuple of (width, height)
        """
        canvas.setFont(font, size)
        return (canvas.stringWidth(text, font, size), size)

    @staticmethod
    def hex_to_reportlab_color(hex_color: str) -> Color:
        """Convert hex color string to ReportLab Color.

        Args:
            hex_color: Hex color string (e.g., '#2E5BFF')

        Returns:
            ReportLab Color object
        """
        from reportlab.lib.colors import HexColor
        return HexColor(hex_color)
