#!/usr/bin/env python3
"""
MBR Configuration Management
Handles data source configs, chart specs, design system settings
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class ChartType(Enum):
    """Supported chart types for MBR"""
    BAR = "bar"
    LINE = "line"
    COMBO = "combo"  # bar + line
    AREA = "area"
    TABLE = "table"
    KPI_CARD = "kpi_card"


class WalmartColor(Enum):
    """Walmart brand color palette"""
    BLUE_100 = "#0053E2"  # Primary
    BLUE_110 = "#0053E2"
    BLUE_130 = "#003B99"
    SPARK_100 = "#FFC220"  # Accent
    SPARK_140 = "#995213"  # Warning
    SPARK_10 = "#FFFAF0"  # Warning background
    RED_100 = "#EA1100"  # Danger
    GREEN_100 = "#2A8703"  # Success
    GRAY_10 = "#F5F5F5"  # Light background
    GRAY_50 = "#DFDFDF"  # Light borders
    GRAY_100 = "#BFBFBF"  # Medium
    GRAY_160 = "#2E2F32"  # Dark text
    BLACK = "#000000"
    WHITE = "#FFFFFF"


@dataclass
class DesignSystemConfig:
    """Design system settings for MBR deck"""
    primary_color: str = WalmartColor.BLUE_100.value
    accent_color: str = WalmartColor.SPARK_100.value
    success_color: str = WalmartColor.GREEN_100.value
    error_color: str = WalmartColor.RED_100.value
    warning_color: str = WalmartColor.SPARK_140.value
    text_color: str = WalmartColor.GRAY_160.value
    bg_color: str = WalmartColor.WHITE.value
    bg_light: str = WalmartColor.GRAY_10.value

    # Typography
    heading_1_size: int = 32
    heading_2_size: int = 24
    body_size: int = 14
    caption_size: int = 10

    # Spacing (8px unit system)
    spacing_xs: int = 4
    spacing_sm: int = 8
    spacing_md: int = 16
    spacing_lg: int = 24
    spacing_xl: int = 32

    # Chart defaults
    chart_height: int = 300
    chart_width: int = 600
    table_max_rows: int = 15
    table_min_cols: int = 3
    table_max_cols: int = 8


@dataclass
class DataSourceConfig:
    """Configuration for data sources"""
    source_type: str  # "bq", "pbi", "csv"
    credentials: Optional[Dict[str, str]] = None
    queries: Optional[Dict[str, str]] = None  # For BQ
    workspace: Optional[str] = None  # For PBI
    dataset: Optional[str] = None  # For PBI
    files: Optional[List[str]] = None  # For CSV


@dataclass
class MetricConfig:
    """Configuration for metric definitions"""
    name: str
    source_field: str
    unit: str = ""
    chart_type: ChartType = ChartType.COMBO
    show_target: bool = True
    show_prior: bool = True
    show_ly: bool = True
    segment_breakdown: bool = False
    threshold_warning: Optional[float] = None
    threshold_critical: Optional[float] = None


@dataclass
class DeckConfig:
    """Overall deck configuration"""
    period: str
    team: str
    title: str
    design_system: DesignSystemConfig = field(default_factory=DesignSystemConfig)
    data_source: Optional[DataSourceConfig] = None
    metrics: List[MetricConfig] = field(default_factory=list)
    include_appendix: bool = True
    include_risks: bool = True
    include_wins: bool = True
    max_iterations: int = 3
    target_qa_score: float = 4.0

    def validate(self) -> tuple[bool, List[str]]:
        """Validate configuration"""
        issues = []

        if not self.period:
            issues.append("Missing period")
        if not self.team:
            issues.append("Missing team")
        if not self.title:
            issues.append("Missing title")
        if len(self.metrics) == 0:
            issues.append("No metrics configured")
        if not self.data_source:
            issues.append("No data source configured")

        return len(issues) == 0, issues


@dataclass
class QAConfig:
    """QA thresholds and settings"""
    min_overall_score: float = 4.0
    check_action_titles: bool = True
    check_chart_labels: bool = True
    check_source_citations: bool = True
    check_brand_colors: bool = True
    check_word_count: bool = True
    max_words_per_slide: int = 100
    check_table_alignment: bool = True
    check_color_consistency: bool = True

    # Weighted scoring
    weight_action_title: float = 0.15
    weight_visuals: float = 0.25
    weight_data_accuracy: float = 0.25
    weight_design: float = 0.20
    weight_clarity: float = 0.15


class Config:
    """Global configuration manager"""

    # Default deck configuration
    DEFAULT_DECK: DeckConfig = DeckConfig(
        period="December 2025",
        team="Revenue Operations",
        title="Monthly Business Review",
    )

    # Default QA configuration
    DEFAULT_QA: QAConfig = QAConfig()

    @staticmethod
    def load_from_file(config_file: str) -> DeckConfig:
        """Load configuration from JSON file"""
        import json

        with open(config_file, "r") as f:
            data = json.load(f)
        # TODO: Parse JSON into DeckConfig
        return Config.DEFAULT_DECK

    @staticmethod
    def load_from_dict(config_dict: Dict) -> DeckConfig:
        """Load configuration from dictionary"""
        # TODO: Parse dict into DeckConfig
        return Config.DEFAULT_DECK