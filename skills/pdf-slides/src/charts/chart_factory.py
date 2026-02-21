"""Chart factory for creating matplotlib charts from data."""

from io import BytesIO
from typing import Optional
import matplotlib.pyplot as plt
import numpy as np

from .style_manager import StyleManager


class ChartFactory:
    """Factory for creating styled charts from JSON data.

    Supports bar, line, pie, and area charts with brand-consistent styling.
    Returns PNG images ready for embedding in ReportLab PDFs.
    """

    def __init__(self, color_palette):
        """Initialize chart factory with brand colors.

        Args:
            color_palette: ColorPalette instance for styling
        """
        self.color_palette = color_palette
        self.style_manager = StyleManager(color_palette)

    def create_chart(
        self,
        chart_type: str,
        data: dict,
        title: Optional[str] = None,
    ) -> bytes:
        """Create a chart from data dict.

        Args:
            chart_type: Type of chart (bar, line, pie, area)
            data: Data dict with 'labels' and 'values' keys
            title: Optional chart title

        Returns:
            PNG image as bytes

        Raises:
            ValueError: If chart_type is not supported
        """
        labels = data.get("labels", [])
        values = data.get("values", [])

        if not labels or not values:
            raise ValueError("Chart data must contain 'labels' and 'values'")

        if len(labels) != len(values):
            raise ValueError("Labels and values must have the same length")

        # Route to specific chart method
        chart_methods = {
            "bar": self._create_bar_chart,
            "line": self._create_line_chart,
            "pie": self._create_pie_chart,
            "area": self._create_area_chart,
        }

        if chart_type not in chart_methods:
            raise ValueError(
                f"Unsupported chart type: {chart_type}. "
                f"Must be one of: {', '.join(chart_methods.keys())}"
            )

        return chart_methods[chart_type](labels, values, title)

    def _create_bar_chart(
        self,
        labels: list[str],
        values: list[float],
        title: Optional[str],
    ) -> bytes:
        """Create a bar chart.

        Args:
            labels: X-axis labels
            values: Bar heights
            title: Chart title

        Returns:
            PNG image as bytes
        """
        fig, ax = plt.subplots()

        x_pos = np.arange(len(labels))
        bars = ax.bar(x_pos, values)

        # Apply styling
        self.style_manager.apply_bar_style(ax, len(labels))

        # Set labels
        ax.set_xticks(x_pos)
        ax.set_xticklabels(labels, fontsize=12)
        ax.tick_params(axis='y', labelsize=10)

        if title:
            ax.set_title(title, fontsize=14, fontweight='bold', pad=15)

        # Set size and save
        self.style_manager.set_figure_size(fig, width=8, height=4.5)

        return self._fig_to_bytes(fig)

    def _create_line_chart(
        self,
        labels: list[str],
        values: list[float],
        title: Optional[str],
    ) -> bytes:
        """Create a line chart.

        Args:
            labels: X-axis labels
            values: Y-axis values
            title: Chart title

        Returns:
            PNG image as bytes
        """
        fig, ax = plt.subplots()

        x_pos = np.arange(len(labels))
        ax.plot(x_pos, values, linewidth=2.5)

        # Apply styling
        self.style_manager.apply_line_style(ax)

        # Set labels
        ax.set_xticks(x_pos)
        ax.set_xticklabels(labels, fontsize=12)
        ax.tick_params(axis='y', labelsize=10)

        if title:
            ax.set_title(title, fontsize=14, fontweight='bold', pad=15)

        # Set size and save
        self.style_manager.set_figure_size(fig, width=8, height=4.5)

        return self._fig_to_bytes(fig)

    def _create_pie_chart(
        self,
        labels: list[str],
        values: list[float],
        title: Optional[str],
    ) -> bytes:
        """Create a pie chart.

        Args:
            labels: Slice labels
            values: Slice values
            title: Chart title

        Returns:
            PNG image as bytes
        """
        fig, ax = plt.subplots()

        # Calculate percentages for labels
        total = sum(values)
        percentages = [f"{v/total*100:.1f}%" for v in values]
        labels_with_pct = [f"{l}\n{p}" for l, p in zip(labels, percentages)]

        # Create pie chart with autopct for percentage labels
        result = ax.pie(
            values,
            labels=labels_with_pct,
            autopct='%1.1f%%',
            startangle=90,
            counterclock=False,
        )

        # Handle different matplotlib versions (may return 2 or 3 values)
        if len(result) == 3:
            wedges, texts, autotexts = result
        else:
            wedges, texts = result
            autotexts = []

        # Style percentage text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')

        # Style labels
        for text in texts:
            text.set_fontsize(11)

        # Apply styling
        self.style_manager.apply_pie_style(ax, len(labels))

        if title:
            ax.set_title(title, fontsize=14, fontweight='bold', pad=15)

        # Set size and save
        self.style_manager.set_figure_size(fig, width=6, height=5)

        return self._fig_to_bytes(fig)

    def _create_area_chart(
        self,
        labels: list[str],
        values: list[float],
        title: Optional[str],
    ) -> bytes:
        """Create an area chart (filled line chart).

        Args:
            labels: X-axis labels
            values: Y-axis values
            title: Chart title

        Returns:
            PNG image as bytes
        """
        fig, ax = plt.subplots()

        x_pos = np.arange(len(labels))
        line = ax.plot(x_pos, values, linewidth=2.5)[0]
        ax.fill_between(x_pos, values, alpha=0.3)

        # Apply styling
        self.style_manager.apply_area_style(ax)

        # Set labels
        ax.set_xticks(x_pos)
        ax.set_xticklabels(labels, fontsize=12)
        ax.tick_params(axis='y', labelsize=10)

        if title:
            ax.set_title(title, fontsize=14, fontweight='bold', pad=15)

        # Set size and save
        self.style_manager.set_figure_size(fig, width=8, height=4.5)

        return self._fig_to_bytes(fig)

    def _fig_to_bytes(self, fig: plt.Figure) -> bytes:
        """Convert matplotlib figure to PNG bytes.

        Args:
            fig: Matplotlib figure

        Returns:
            PNG image data as bytes
        """
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='white')
        plt.close(fig)
        buf.seek(0)
        return buf.read()
