"""Chart styling manager for matplotlib integration."""

from typing import Optional
import matplotlib.pyplot as plt
import matplotlib as mpl


class StyleManager:
    """Manages matplotlib chart styling with brand colors.

    Applies consistent styling to all charts including colors,
    fonts, grid settings, and other visual properties.
    """

    def __init__(self, color_palette):
        """Initialize style manager with brand colors.

        Args:
            color_palette: ColorPalette instance for brand colors
        """
        self.color_palette = color_palette
        self._configure_matplotlib()

    def _configure_matplotlib(self) -> None:
        """Configure global matplotlib settings."""
        # Use Agg backend for non-interactive rendering
        mpl.use('Agg')

        # Set default styling
        plt.rcParams.update({
            'font.family': 'sans-serif',
            'font.sans-serif': ['Helvetica', 'Arial', 'DejaVu Sans'],
            'axes.edgecolor': '#E0E0E0',
            'axes.linewidth': 1,
            'grid.alpha': 0.3,
            'grid.linestyle': '--',
            'grid.linewidth': 0.5,
        })

    def get_colors(self, n: int) -> list[str]:
        """Get n chart colors from brand palette.

        Args:
            n: Number of colors needed

        Returns:
            List of hex color strings
        """
        return [self.color_palette.get_chart_hex(i) for i in range(n)]

    def apply_bar_style(self, ax: plt.Axes, data_len: int) -> None:
        """Apply styling to bar chart.

        Args:
            ax: Matplotlib axes
            data_len: Number of data points (for color selection)
        """
        colors = self.get_colors(data_len)

        # Apply colors to bars
        for i, bar in enumerate(ax.patches):
            bar.set_color(colors[i % len(colors)])
            bar.set_edgecolor('white')
            bar.set_linewidth(0.5)

        # Style grid
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)

        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    def apply_line_style(self, ax: plt.Axes, line_index: int = 0) -> None:
        """Apply styling to line chart.

        Args:
            ax: Matplotlib axes
            line_index: Index for color selection
        """
        color = self.color_palette.get_chart_hex(line_index)

        # Style the line
        for line in ax.lines:
            line.set_color(color)
            line.set_linewidth(2.5)
            line.set_marker('o')
            line.set_markersize(8)
            line.set_markerfacecolor('white')
            line.set_markeredgecolor(color)
            line.set_markeredgewidth(2)

        # Style fill (if area chart)
        for collection in ax.collections:
            collection.set_facecolor(color)
            collection.set_alpha(0.2)

        # Style grid
        ax.grid(alpha=0.3, linestyle='--')
        ax.set_axisbelow(True)

        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

    def apply_pie_style(self, ax: plt.Axes, data_len: int) -> None:
        """Apply styling to pie chart.

        Args:
            ax: Matplotlib axes
            data_len: Number of data points
        """
        colors = self.get_colors(data_len)

        # Style wedges
        for wedge, color in zip(ax.patches, colors):
            wedge.set_facecolor(color)
            wedge.set_edgecolor('white')
            wedge.set_linewidth(2)

        # Equal aspect ratio ensures circular pie
        ax.set_aspect('equal')

    def apply_area_style(self, ax: plt.Axes, line_index: int = 0) -> None:
        """Apply styling to area chart.

        Args:
            ax: Matplotlib axes
            line_index: Index for color selection
        """
        self.apply_line_style(ax, line_index)

        # Add fill with transparency
        color = self.color_palette.get_chart_hex(line_index)
        from matplotlib.colors import to_hex
        from matplotlib.patches import Polygon

        # Convert hex to rgba with alpha
        for collection in ax.collections:
            collection.set_alpha(0.3)

    def set_figure_size(
        self,
        fig: plt.Figure,
        width: float = 8,
        height: float = 4.5,
    ) -> None:
        """Set figure size with tight layout.

        Args:
            fig: Matplotlib figure
            width: Width in inches
            height: Height in inches
        """
        fig.set_size_inches(width, height)
        fig.set_tight_layout(True)

    def remove_axes_frame(self, ax: plt.Axes) -> None:
        """Remove axes frame for cleaner look.

        Args:
            ax: Matplotlib axes
        """
        ax.set_frame_on(False)
        ax.ax = None
        ax.set_xticks([])
        ax.set_yticks([])

    def format_value_labels(
        self,
        ax: plt.Axes,
        chart_type: str = "bar",
    ) -> None:
        """Add value labels to chart elements.

        Args:
            ax: Matplotlib axes
            chart_type: Type of chart for label placement
        """
        if chart_type == "bar":
            for bar in ax.patches:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height,
                    f'{height:.0f}',
                    ha='center',
                    va='bottom',
                    fontsize=10,
                )
        elif chart_type == "pie":
            percentages = [f'{p:.1f}%' for p in ax.patches[0].get_height()]
            # Pie labels are handled by autopct
