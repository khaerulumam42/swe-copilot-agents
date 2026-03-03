"""Stats slide implementation for key metrics display."""

from typing import Dict, Any
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.units import inch

from .base_slide import BaseSlide


class StatsSlide(BaseSlide):
    """Slide displaying key metrics/statistics with change indicators.

    Each stat shows a label, value, and optional change percentage.
    """

    def render(self, canvas: Canvas) -> None:
        """Render the stats slide.

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
        text_light = self.brand.get_color("text_light")
        success_color = self.brand.get_color("success")
        error_color = self.brand.get_color("error")
        accent_color = self.brand.get_color("accent")

        title_font = self.brand.get_font("title")
        title_size = self.brand.get_size("title") * 0.7  # Smaller for stats

        label_font = self.brand.get_font("body")
        label_size = self.brand.get_size("body")

        change_font = self.brand.get_font("caption")
        change_size = self.brand.get_size("caption")

        # Get stats from data
        stats = self.data.get("stats", [])

        # Calculate grid layout
        num_stats = len(stats)
        if num_stats == 0:
            return

        # Determine grid dimensions
        if num_stats <= 2:
            cols = 1
            rows = num_stats
        elif num_stats <= 4:
            cols = 2
            rows = (num_stats + 1) // 2
        else:
            cols = 3
            rows = (num_stats + 2) // 3

        # Calculate cell dimensions
        cell_width = width / cols
        cell_height = 180  # Fixed height per stat

        # Render each stat
        for i, stat in enumerate(stats):
            row = i // cols
            col = i % cols

            # Calculate position
            cell_x = x + col * cell_width
            cell_y = y + height - (row + 1) * cell_height

            # Draw stat card
            self._draw_stat_card(
                canvas,
                stat,
                cell_x,
                cell_y,
                cell_width - 20,  # Padding
                cell_height,
                title_font,
                title_size,
                label_font,
                label_size,
                change_font,
                change_size,
                primary_color,
                text_color,
                text_light,
                success_color,
                error_color,
                accent_color,
            )

        # Render footer
        self.render_footer(canvas, 0, 0)  # Page numbers set by generator

    def _draw_stat_card(
        self,
        canvas: Canvas,
        stat: Dict[str, Any],
        x: float,
        y: float,
        width: float,
        height: float,
        title_font: str,
        title_size: int,
        label_font: str,
        label_size: int,
        change_font: str,
        change_size: int,
        primary_color,
        text_color,
        text_light,
        success_color,
        error_color,
        accent_color,
    ) -> None:
        """Draw a single stat card.

        Args:
            canvas: ReportLab Canvas
            stat: Stat dict with label, value, and optional change
            x, y, width, height: Card bounds
            title_font, title_size: Value font settings
            label_font, label_size: Label font settings
            change_font, change_size: Change indicator font settings
            primary_color, text_color, text_light: Color options
            success_color, error_color: Change color options
            accent_color: Accent color
        """
        label = stat.get("label", "")
        value = stat.get("value", "")
        change = stat.get("change", "")

        # Draw accent bar at top
        canvas.setFillColor(accent_color)
        canvas.rect(x, y + height - 4, width, 4, fill=True, stroke=False)

        # Draw label
        canvas.setFillColor(text_light)
        canvas.setFont(label_font, label_size)
        canvas.drawString(x, y + height - 30, label)

        # Draw value
        canvas.setFillColor(primary_color)
        canvas.setFont(title_font, title_size)
        canvas.drawString(x, y + height - 80, value)

        # Draw change indicator if present
        if change:
            # Determine color based on positive/negative
            is_positive = change.startswith("+")
            change_color = success_color if is_positive else error_color

            canvas.setFillColor(change_color)
            canvas.setFont(change_font, change_size)
            canvas.drawString(x, y + height - 110, change)
