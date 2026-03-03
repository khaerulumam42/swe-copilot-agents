"""Input validation for slide outlines."""

from typing import Any, Dict, List


class Validators:
    """Validation utilities for slide outline data."""

    VALID_SLIDE_TYPES = {
        "title",
        "content",
        "chart",
        "stats",
        "two_column",
        "section",
    }

    VALID_CHART_TYPES = {
        "bar",
        "line",
        "pie",
        "area",
    }

    @staticmethod
    def validate_outline(outline: dict) -> List[str]:
        """Validate a complete slide outline.

        Args:
            outline: Full outline dict with title, branding, slides

        Returns:
            List of error messages (empty if valid)
        """
        errors = []

        # Check required top-level fields
        if "slides" not in outline:
            errors.append("Missing required field: 'slides'")
            return errors

        if not isinstance(outline["slides"], list):
            errors.append("'slides' must be a list")
            return errors

        # Validate each slide
        for i, slide in enumerate(outline["slides"]):
            slide_errors = Validators.validate_slide(slide)
            for error in slide_errors:
                errors.append(f"Slide {i + 1}: {error}")

        return errors

    @staticmethod
    def validate_slide(slide: dict) -> List[str]:
        """Validate a single slide definition.

        Args:
            slide: Slide data dict

        Returns:
            List of error messages (empty if valid)
        """
        errors = []

        # Check required fields
        if "type" not in slide:
            errors.append("Missing required field: 'type'")
            return errors

        slide_type = slide["type"]

        # Validate slide type
        if slide_type not in Validators.VALID_SLIDE_TYPES:
            errors.append(
                f"Invalid slide type: '{slide_type}'. "
                f"Must be one of: {', '.join(Validators.VALID_SLIDE_TYPES)}"
            )

        # Type-specific validation
        if slide_type == "chart":
            errors.extend(Validators._validate_chart_slide(slide))
        elif slide_type == "stats":
            errors.extend(Validators._validate_stats_slide(slide))
        elif slide_type == "two_column":
            errors.extend(Validators._validate_two_column_slide(slide))

        return errors

    @staticmethod
    def _validate_chart_slide(slide: dict) -> List[str]:
        """Validate chart slide specific fields.

        Args:
            slide: Chart slide data dict

        Returns:
            List of error messages
        """
        errors = []

        if "chart_type" not in slide:
            errors.append("Chart slide missing 'chart_type'")
        elif slide["chart_type"] not in Validators.VALID_CHART_TYPES:
            errors.append(
                f"Invalid chart_type: '{slide.get('chart_type')}'. "
                f"Must be one of: {', '.join(Validators.VALID_CHART_TYPES)}"
            )

        if "data" not in slide:
            errors.append("Chart slide missing 'data'")
        else:
            data = slide["data"]
            if "labels" not in data or "values" not in data:
                errors.append("Chart data must contain 'labels' and 'values'")
            elif len(data.get("labels", [])) != len(data.get("values", [])):
                errors.append("Chart 'labels' and 'values' must have same length")

        return errors

    @staticmethod
    def _validate_stats_slide(slide: dict) -> List[str]:
        """Validate stats slide specific fields.

        Args:
            slide: Stats slide data dict

        Returns:
            List of error messages
        """
        errors = []

        if "stats" not in slide:
            errors.append("Stats slide missing 'stats' array")
        elif not isinstance(slide["stats"], list):
            errors.append("'stats' must be an array")
        else:
            for i, stat in enumerate(slide["stats"]):
                if not isinstance(stat, dict):
                    errors.append(f"Stat {i + 1} must be an object")
                    continue
                if "label" not in stat:
                    errors.append(f"Stat {i + 1} missing 'label'")
                if "value" not in stat:
                    errors.append(f"Stat {i + 1} missing 'value'")

        return errors

    @staticmethod
    def _validate_two_column_slide(slide: dict) -> List[str]:
        """Validate two_column slide specific fields.

        Args:
            slide: Two column slide data dict

        Returns:
            List of error messages
        """
        errors = []

        if "left" not in slide or "right" not in slide:
            errors.append("Two column slide must have 'left' and 'right' sections")
        else:
            for side in ["left", "right"]:
                if side in slide and not isinstance(slide[side], dict):
                    errors.append(f"'{side}' must be an object")

        return errors

    @staticmethod
    def is_valid_outline(outline: dict) -> bool:
        """Check if outline is valid (returns bool).

        Args:
            outline: Full outline dict

        Returns:
            True if valid, False otherwise
        """
        errors = Validators.validate_outline(outline)
        return len(errors) == 0
