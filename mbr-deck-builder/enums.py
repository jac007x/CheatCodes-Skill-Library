#!/usr/bin/env python3
"""
Canonical Enums for MBR System

Single source of truth for all enums.
All code imports from here.
"""

from enum import Enum


class TrendDirection(Enum):
    """Metric trend direction"""
    UP = "up"
    DOWN = "down"
    FLAT = "flat"


class Momentum(Enum):
    """Momentum indicator"""
    ACCELERATING = "accelerating"
    STABLE = "stable"
    DECELERATING = "decelerating"


class NarrativeStyle(Enum):
    """Narrative writing style"""
    EXECUTIVE = "executive"
    INVESTOR = "investor"
    TECHNICAL = "technical"
    BOARD = "board"
    CAUTIOUS = "cautious"
    OPTIMISTIC = "optimistic"


class AudienceRole(Enum):
    """Executive roles for role-specific summaries"""
    CFO = "cfo"
    COO = "coo"
    CTO = "cto"
    CMO = "cmo"
    CEO = "ceo"
    BOARD = "board"


class RecommendationSeverity(Enum):
    """Recommendation priority levels"""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    INFO = 1


class ConfidenceLevel(Enum):
    """Confidence in insights (0-1 scale)"""
    VERY_HIGH = 0.95
    HIGH = 0.85
    MEDIUM = 0.70
    LOW = 0.50
    VERY_LOW = 0.30