"""Content slide with bullet points."""

from typing import List
from reportlab.pdfgen.canvas import Canvas

from .base_slide import BaseSlide


class ContentSlide(BaseSlide):
    """Content slide with bullet points.

    Supports hierarchical bullet points and subsections.
    """

    def render(self, canvas: Canvas) -> None:
        """Render the content slide.

        Args:
            canvas: ReportLab Canvas to draw on
        """
        # Render header
        self.render_header(canvas)

        # Get content area
        x, y, width, height = self.get_content_bounds()

        # Get brand styling
        primary_color = self.brand.get_color("primary")
        text_color = self.brand.get_color("text")
        bullet_color = self.brand.get_color("accent")

        body_font = self.brand.get_font("body")
        body_size = self.brand.get_size("body")

        heading_font = self.brand.get_font("subheading")
        heading_size = self.brand.get_size("subheading")

        # Get points from data
        points = self.data.get("points", [])

        # Render each bullet point
        line_spacing = body_size * 1.8
        current_y = y + height - body_size

        for point in points:
            if isinstance(point, str):
                # Simple bullet point
                current_y = self._draw_bullet(
                    canvas,
                    point,
                    x,
                    current_y,
                    body_font,
                    body_size,
                    text_color,
                    bullet_color,
                )
            elif isinstance(point, dict):
                # Subsection with heading and sub-points
                if "heading" in point:
                    # Draw section heading
                    canvas.setFillColor(primary_color)
                    canvas.setFont(heading_font, heading_size)
                    canvas.drawString(x, current_y, point["heading"])
                    current_y -= line_spacing * 1.2

                # Draw sub-points with indent
                sub_points = point.get("points", [])
                for sub_point in sub_points:
                    current_y = self._draw_bullet(
                        canvas,
                        sub_point,
                        x + 20,
                        current_y,
                        body_font,
                        body_size,
                        text_color,
                        bullet_color,
                    )

            current_y -= line_spacing * 0.3  # Extra spacing between main points

        # Render footer
        self.render_footer(canvas, 0, 0)  # Page numbers set by generator

    def _draw_bullet(
        self,
        canvas: Canvas,
        text: str,
        x: float,
        y: float,
        font: str,
        size: int,
        text_color,
        bullet_color,
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
            text_color: Text color
            bullet_color: Bullet color
            indent: Indent for text after bullet

        Returns:
            New Y position after drawing
        """
        # Draw bullet
        canvas.setFillColor(bullet_color)
        canvas.setFont(font, size)
        canvas.drawString(x, y, "•")

        # Check if text needs wrapping
        max_width = self.WIDTH - self.MARGIN_LEFT - self.MARGIN_RIGHT - x - indent
        text_width = canvas.stringWidth(text, font, size)

        if text_width > max_width:
            # Simple text wrapping
            words = text.split()
            lines = []
            current_line = []
            current_width = 0

            for word in words:
                word_width = canvas.stringWidth(word + " ", font, size)
                if current_width + word_width > max_width:
                    if current_line:
                        lines.append(" ".join(current_line))
                    current_line = [word]
                    current_width = word_width
                else:
                    current_line.append(word)
                    current_width += word_width

            if current_line:
                lines.append(" ".join(current_line))

            # Draw wrapped lines
            canvas.setFillColor(text_color)
            for i, line in enumerate(lines):
                canvas.drawString(x + indent, y - i * size * 1.3, line)

            return y - (len(lines) - 1) * size * 1.3
        else:
            # Draw single line
            canvas.setFillColor(text_color)
            canvas.drawString(x + indent, y, text)
            return y
