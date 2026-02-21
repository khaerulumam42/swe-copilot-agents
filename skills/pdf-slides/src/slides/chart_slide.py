"""Chart slide implementation."""

from io import BytesIO
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader

from .base_slide import BaseSlide
from ..charts.chart_factory import ChartFactory


class ChartSlide(BaseSlide):
    """Slide with a data visualization chart.

    Supports bar, line, pie, and area charts with brand styling.
    """

    def render(self, canvas: Canvas) -> None:
        """Render the chart slide.

        Args:
            canvas: ReportLab Canvas to draw on
        """
        # Render header
        self.render_header(canvas)

        # Get chart configuration
        chart_type = self.data.get("chart_type", "bar")
        chart_data = self.data.get("data", {})

        # Create chart image
        chart_factory = ChartFactory(self.brand.colors)
        chart_bytes = chart_factory.create_chart(chart_type, chart_data, self.title)

        # Convert to ReportLab image
        img = ImageReader(BytesIO(chart_bytes))

        # Get content area
        x, y, width, height = self.get_content_bounds()

        # Calculate image dimensions maintaining aspect ratio
        img_width, img_height = img.getSize()

        # Leave room for chart title in header, use full content width
        max_width = width
        max_height = height

        # Scale to fit while maintaining aspect ratio
        scale = min(max_width / img_width, max_height / img_height)
        scaled_width = img_width * scale
        scaled_height = img_height * scale

        # Center the chart
        x_pos = x + (max_width - scaled_width) / 2
        y_pos = y + (max_height - scaled_height) / 2

        # Draw the chart
        canvas.drawImage(
            img,
            x_pos, y_pos,
            width=scaled_width,
            height=scaled_height,
            mask='auto',
        )

        # Render footer
        self.render_footer(canvas, 0, 0)  # Page numbers set by generator
