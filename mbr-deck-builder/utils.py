#!/usr/bin/env python3
"""
Utility functions for MBR engine
Date handling, formatting, validation
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import json


class DateUtils:
    """Utilities for date/period handling"""

    @staticmethod
    def get_current_period() -> str:
        """Get current month period as 'Month YYYY'"""
        now = datetime.now()
        return now.strftime("%B %Y")

    @staticmethod
    def get_prior_period() -> str:
        """Get prior month period"""
        now = datetime.now()
        prior = now - timedelta(days=30)  # Approximate
        return prior.strftime("%B %Y")

    @staticmethod
    def get_same_period_ly() -> str:
        """Get same period last year"""
        now = datetime.now()
        ly = now - timedelta(days=365)
        return ly.strftime("%B %Y")


class NumberFormatter:
    """Format numbers for display in deck"""

    @staticmethod
    def format_currency(value: float, decimals: int = 1) -> str:
        """Format as currency (e.g., $14.2M)"""
        if abs(value) >= 1_000_000:
            return f"${value / 1_000_000:.{decimals}f}M"
        elif abs(value) >= 1_000:
            return f"${value / 1_000:.{decimals}f}K"
        else:
            return f"${value:,.0f}"

    @staticmethod
    def format_percentage(value: float, decimals: int = 1, show_sign: bool = True) -> str:
        """Format as percentage (e.g., +3.1%, -2.5%)"""
        sign = "+" if value > 0 and show_sign else ""
        return f"{sign}{value:.{decimals}f}%"

    @staticmethod
    def format_count(value: int) -> str:
        """Format as count with separators (e.g., 45,000)"""
        return f"{value:,}"

    @staticmethod
    def format_delta(current: float, prior: float, decimals: int = 1) -> Tuple[float, str]:
        """
        Calculate delta and return value + formatted string
        
        Returns:
            (delta_percentage, formatted_string)
            e.g., (12.3, "+12.3% vs prior")
        """
        if prior == 0:
            return 0, "N/A"

        delta = ((current - prior) / prior) * 100
        sign = "+" if delta > 0 else ""
        return delta, f"{sign}{delta:.{decimals}f}% vs prior"


class ColorSelector:
    """Select appropriate color based on value or status"""

    from config import WalmartColor

    @staticmethod
    def get_status_color(status: str) -> str:
        """Get color for status"""
        status_map = {
            "positive": WalmartColor.GREEN_100.value,
            "negative": WalmartColor.RED_100.value,
            "neutral": WalmartColor.GRAY_100.value,
            "warning": WalmartColor.SPARK_140.value,
        }
        return status_map.get(status, WalmartColor.GRAY_100.value)

    @staticmethod
    def get_delta_color(delta: float) -> str:
        """Get color based on delta value"""
        if delta > 0:
            return WalmartColor.GREEN_100.value
        elif delta < 0:
            return WalmartColor.RED_100.value
        else:
            return WalmartColor.GRAY_100.value


class TextFormatter:
    """Format text for deck slides"""

    MAX_TITLE_LENGTH = 100
    MAX_INSIGHT_LENGTH = 200
    MAX_SLIDE_WORDS = 100

    @staticmethod
    def validate_title(title: str) -> Tuple[bool, str]:
        """
        Validate slide title
        
        Returns:
            (is_valid, error_message)
        """
        if not title or len(title.strip()) == 0:
            return False, "Title cannot be empty"
        if len(title) > TextFormatter.MAX_TITLE_LENGTH:
            return False, f"Title too long ({len(title)} > {TextFormatter.MAX_TITLE_LENGTH})"
        # Title must start with action verb
        action_verbs = ["increased", "decreased", "improved", "declined", "grew", "exceeded", "missed"]
        if not any(title.lower().startswith(v) for v in action_verbs):
            return False, "Title should start with action verb (e.g., 'Increased...', 'Exceeded...')"
        return True, ""

    @staticmethod
    def word_count(text: str) -> int:
        """Count words in text"""
        return len(text.split())

    @staticmethod
    def validate_slide_content(text: str) -> Tuple[bool, str]:
        """
        Validate slide content length
        
        Returns:
            (is_valid, error_message)
        """
        words = TextFormatter.word_count(text)
        if words > TextFormatter.MAX_SLIDE_WORDS:
            return False, f"Too many words ({words} > {TextFormatter.MAX_SLIDE_WORDS}). Remove non-essential text."
        return True, ""

    @staticmethod
    def truncate(text: str, max_length: int, suffix: str = "...") -> str:
        """Truncate text to max length"""
        if len(text) <= max_length:
            return text
        return text[: max_length - len(suffix)] + suffix


class JsonUtils:
    """JSON serialization helpers"""

    @staticmethod
    def to_json(obj: Any, pretty: bool = False) -> str:
        """Convert object to JSON string"""
        indent = 2 if pretty else None
        return json.dumps(obj, indent=indent, default=str)

    @staticmethod
    def to_file(obj: Any, filename: str, pretty: bool = True) -> None:
        """Write object to JSON file"""
        with open(filename, "w") as f:
            json.dump(obj, f, indent=2 if pretty else None, default=str)

    @staticmethod
    def from_file(filename: str) -> Dict[str, Any]:
        """Load object from JSON file"""
        with open(filename, "r") as f:
            return json.load(f)


class DataValidator:
    """Validate data quality"""

    @staticmethod
    def validate_metric_values(
        current: float, target: float, prior: float, ly: float
    ) -> Tuple[bool, List[str]]:
        """
        Validate metric values
        
        Returns:
            (is_valid, issues)
        """
        issues = []

        if current is None or not isinstance(current, (int, float)):
            issues.append("Current value is invalid")
        if target is None or not isinstance(target, (int, float)) or target == 0:
            issues.append("Target value is invalid")
        if prior is None or not isinstance(prior, (int, float)):
            issues.append("Prior period value is invalid")
        if ly is None or not isinstance(ly, (int, float)):
            issues.append("Year-over-year value is invalid")

        return len(issues) == 0, issues

    @staticmethod
    def check_sanity(
        current: float, target: float, prior: float, ly: float
    ) -> Tuple[bool, List[str]]:
        """
        Perform sanity checks on metric values
        
        Returns:
            (is_sane, warnings)
        """
        warnings = []

        # Check for extreme deltas
        if prior > 0 and abs((current - prior) / prior) > 5:  # 500% delta
            warnings.append("Extreme delta vs prior period (>500%)")
        if ly > 0 and abs((current - ly) / ly) > 5:  # 500% delta
            warnings.append("Extreme delta vs year-over-year (>500%)")

        # Check if target is realistic
        if target > 0 and abs((target - prior) / prior) > 1:  # 100% delta from prior
            warnings.append("Target differs dramatically from prior period")

        return len(warnings) == 0, warnings