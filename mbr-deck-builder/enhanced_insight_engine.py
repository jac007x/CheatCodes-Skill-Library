"""Enhanced Phase 2 Analyzer - Phase 1 Improvements for MBR Engine

This module enhances the basic insight generation with:
- Owner assignment for recommendations
- Success criteria for each recommendation
- Recommendation prioritization (impact scoring)
- Confidence scoring for all insights
- Trend analysis with momentum detection

Status: Production Ready
Author: Code Puppy 🐶
Date: March 16, 2026
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
import statistics
from datetime import datetime
import functools

# Import canonical enums from central source
from enums import (
    RecommendationSeverity,
    TrendDirection,
    ConfidenceLevel,
)


@dataclass
class Trend:
    """Trend analysis for a metric"""
    direction: TrendDirection
    momentum: str  # "accelerating", "stable", "decelerating"
    volatility: float  # 0-1, higher = more volatile
    confidence: ConfidenceLevel
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "direction": self.direction.value,
            "momentum": self.momentum,
            "volatility": round(self.volatility, 2),
            "confidence": f"{self.confidence.value*100:.0f}%"
        }


@dataclass
class Recommendation:
    """Enhanced recommendation with context"""
    insight: str  # "Revenue exceeding target"
    recommendation: str  # "Accelerate digital expansion"
    owner: str  # "Marketing Team"
    owner_function: str  # "Marketing"
    severity: RecommendationSeverity
    impact_score: float  # 0-10, how much business impact
    specificity: str  # Concrete action, not vague
    success_criteria: str  # How to measure success
    timeline: str  # When should this be done? "1 week", "2 weeks", etc
    confidence: ConfidenceLevel
    rationale: str  # Why this recommendation
    
    def to_dict(self) -> Dict[str, Any]:
        severity_map = {
            RecommendationSeverity.CRITICAL: "🔴 CRITICAL",
            RecommendationSeverity.HIGH: "🟠 HIGH",
            RecommendationSeverity.MEDIUM: "🟡 MEDIUM",
            RecommendationSeverity.LOW: "🟢 LOW",
            RecommendationSeverity.INFO: "ℹ️  INFO"
        }
        
        return {
            "severity": severity_map[self.severity],
            "owner": self.owner,
            "owner_function": self.owner_function,
            "recommendation": self.recommendation,
            "rationale": self.rationale,
            "specificity": self.specificity,
            "timeline": f"Complete within {self.timeline}",
            "success_criteria": self.success_criteria,
            "impact_score": f"{self.impact_score}/10",
            "confidence": f"{self.confidence.value*100:.0f}%",
            "priority": self.severity.value  # For sorting
        }


@dataclass
class MetricInsight:
    """Complete insight for a single metric"""
    metric_name: str
    current_value: float
    target_value: float
    prior_value: Optional[float] = None
    ly_value: Optional[float] = None
    
    # Calculations
    delta_target: float = 0.0
    delta_prior: float = 0.0
    delta_ly: float = 0.0
    
    # Analysis
    trend: Optional[Trend] = None
    narrative: str = ""
    recommendations: List[Recommendation] = field(default_factory=list)
    anomalies: List[Dict[str, Any]] = field(default_factory=list)
    
    # Metadata
    confidence: ConfidenceLevel = ConfidenceLevel.HIGH
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def calculate_deltas(self):
        """Calculate all deltas"""
        if self.target_value > 0:
            self.delta_target = (self.current_value - self.target_value) / self.target_value
        
        if self.prior_value and self.prior_value > 0:
            self.delta_prior = (self.current_value - self.prior_value) / self.prior_value
        
        if self.ly_value and self.ly_value > 0:
            self.delta_ly = (self.current_value - self.ly_value) / self.ly_value
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric": self.metric_name,
            "current": self.current_value,
            "target": self.target_value,
            "prior_month": self.prior_value,
            "same_period_ly": self.ly_value,
            "delta_vs_target": f"{self.delta_target*100:+.1f}%",
            "delta_vs_prior": f"{self.delta_prior*100:+.1f}%" if self.prior_value else "N/A",
            "delta_vs_ly": f"{self.delta_ly*100:+.1f}%" if self.ly_value else "N/A",
            "trend": self.trend.to_dict() if self.trend else None,
            "narrative": self.narrative,
            "recommendations": [r.to_dict() for r in self.recommendations],
            "anomalies": self.anomalies,
            "confidence": f"{self.confidence.value*100:.0f}%"
        }


class TrendAnalyzer:
    """Analyzes trends in metrics"""
    
    @staticmethod
    def analyze(current: float, prior: float, two_prior: Optional[float] = None) -> Trend:
        """Analyze trend direction and momentum
        
        Args:
            current: Current period value
            prior: Prior period value
            two_prior: Two periods ago (for momentum)
        
        Returns:
            Trend object with direction, momentum, volatility
        """
        # Direction
        if current > prior * 1.01:  # 1% threshold to avoid noise
            direction = TrendDirection.UP
        elif current < prior * 0.99:
            direction = TrendDirection.DOWN
        else:
            direction = TrendDirection.FLAT
        
        # Momentum
        momentum = "stable"
        if two_prior:
            prior_delta = (prior - two_prior) / two_prior if two_prior != 0 else 0
            current_delta = (current - prior) / prior if prior != 0 else 0
            
            if current_delta > prior_delta * 1.1:
                momentum = "accelerating"
            elif current_delta < prior_delta * 0.9:
                momentum = "decelerating"
        
        # Volatility (simplified: 0 = stable, 1 = very volatile)
        volatility = 0.3 if direction == TrendDirection.FLAT else 0.5
        
        # Confidence based on consistency
        if direction == TrendDirection.FLAT:
            confidence = ConfidenceLevel.VERY_HIGH
        elif momentum == "stable":
            confidence = ConfidenceLevel.HIGH
        else:
            confidence = ConfidenceLevel.MEDIUM
        
        return Trend(
            direction=direction,
            momentum=momentum,
            volatility=volatility,
            confidence=confidence
        )


class RecommendationEngine:
    """Generates smart recommendations with owners and success criteria"""
    
    # Recommendation templates by scenario
    TEMPLATES = {
        "positive_momentum": {
            "recommendation": "Capitalize on {metric} momentum",
            "owner_function": "{primary_owner}",
            "severity": RecommendationSeverity.HIGH,
            "specificity": "Accelerate successful initiatives, increase budget/resources",
            "success_criteria": "{metric} maintains/exceeds current growth rate (+{growth}%)",
            "timeline": "1-2 weeks",
            "impact_score": 8,
        },
        "negative_trend": {
            "recommendation": "Investigate and address {metric} decline",
            "owner_function": "{primary_owner}",
            "severity": RecommendationSeverity.HIGH,
            "specificity": "Root cause analysis, then remediation plan",
            "success_criteria": "Root cause identified; decline halts or reverses",
            "timeline": "1 week for analysis, 2 weeks for plan",
            "impact_score": 9,
        },
        "target_miss": {
            "recommendation": "Adjust {metric} target or strategy",
            "owner_function": "{primary_owner}",
            "severity": RecommendationSeverity.MEDIUM,
            "specificity": "Review forecast model; adjust target realism",
            "success_criteria": "Target updated with revised forecast model",
            "timeline": "3-5 days",
            "impact_score": 6,
        },
        "outperformance": {
            "recommendation": "Explore if {metric} outperformance is sustainable",
            "owner_function": "{primary_owner}",
            "severity": RecommendationSeverity.MEDIUM,
            "specificity": "Analyze drivers; stress-test assumptions",
            "success_criteria": "Drivers documented; sustainability confirmed or caveated",
            "timeline": "1 week",
            "impact_score": 7,
        },
    }
    
    # Owner mapping by metric type
    OWNER_MAP = {
        "revenue": {"owner": "Finance/Revenue Team", "function": "Finance"},
        "cac": {"owner": "Marketing Team", "function": "Marketing"},
        "conversion": {"owner": "Product Team", "function": "Product"},
        "ltv": {"owner": "Finance/Product Team", "function": "Finance"},
        "churn": {"owner": "Customer Success Team", "function": "Operations"},
        "nps": {"owner": "Customer Success Team", "function": "Operations"},
        "uptime": {"owner": "Engineering Team", "function": "Engineering"},
        "default": {"owner": "Data Team", "function": "Analytics"},
    }
    
    @staticmethod
    def get_owner(metric_name: str) -> Dict[str, str]:
        """Get owner for a metric"""
        metric_lower = metric_name.lower()
        for key, owner_info in RecommendationEngine.OWNER_MAP.items():
            if key in metric_lower:
                return owner_info
        return RecommendationEngine.OWNER_MAP["default"]
    
    @staticmethod
    def generate_recommendation(
        metric_name: str,
        current: float,
        target: float,
        prior: Optional[float] = None,
        trend: Optional[Trend] = None,
        delta_target: float = 0.0,
        delta_prior: float = 0.0,
    ) -> Optional[Recommendation]:
        """Generate recommendation based on metric state
        
        Returns:
            Recommendation object or None if no action needed
        """
        
        owner_info = RecommendationEngine.get_owner(metric_name)
        owner = owner_info["owner"]
        owner_function = owner_info["function"]
        
        # Determine scenario - use simpler conditions
        if delta_target > 0.05:  # Beating target by 5%+
            scenario = "outperformance"
            template = RecommendationEngine.TEMPLATES[scenario]
            recommendation = template["recommendation"].format(metric=metric_name)
            rationale = f"{metric_name} outperforming target (+{delta_target*100:.1f}%). Ensure sustainability."
            confidence = ConfidenceLevel.HIGH
            
        elif delta_target < -0.10:  # Missing target by 10%+
            scenario = "target_miss"
            template = RecommendationEngine.TEMPLATES[scenario]
            recommendation = template["recommendation"].format(metric=metric_name)
            rationale = f"{metric_name} missing target by {abs(delta_target)*100:.1f}%. Review forecast accuracy."
            confidence = ConfidenceLevel.HIGH
            
        elif prior and delta_prior > 0.05:  # Up 5%+ MoM
            scenario = "positive_momentum"
            template = RecommendationEngine.TEMPLATES[scenario]
            recommendation = template["recommendation"].format(metric=metric_name, growth=f"{delta_prior*100:.1f}")
            rationale = f"{metric_name} growing strong (+{delta_prior*100:.1f}% MoM)."
            confidence = ConfidenceLevel.HIGH
            
        elif prior and delta_prior < -0.05:  # Down 5%+ MoM
            scenario = "negative_trend"
            template = RecommendationEngine.TEMPLATES[scenario]
            recommendation = template["recommendation"].format(metric=metric_name)
            rationale = f"{metric_name} declining ({delta_prior*100:.1f}% MoM). Pattern shift requires attention."
            confidence = ConfidenceLevel.HIGH
            
        else:
            # Default: always generate outperformance/stability recommendation
            scenario = "outperformance"
            template = RecommendationEngine.TEMPLATES[scenario]
            recommendation = template["recommendation"].format(metric=metric_name)
            rationale = f"{metric_name}: {current:.1f} vs target {target:.1f}. Maintain current strategy."
            confidence = ConfidenceLevel.MEDIUM
        
        template = RecommendationEngine.TEMPLATES[scenario]
        
        return Recommendation(
            insight=f"{metric_name} is {trend.direction.value if trend else 'changing'}",
            recommendation=recommendation,
            owner=owner,
            owner_function=owner_function,
            severity=template["severity"],
            impact_score=template["impact_score"],
            specificity=template["specificity"],
            success_criteria=template["success_criteria"],
            timeline=template["timeline"],
            confidence=confidence,
            rationale=rationale
        )


class ConfidenceScorer:
    """Scores confidence in insights"""
    
    @staticmethod
    def score_forecast(forecast_accuracy_history: List[float]) -> ConfidenceLevel:
        """Score confidence in forecasting based on historical accuracy"""
        if not forecast_accuracy_history:
            return ConfidenceLevel.MEDIUM
        
        avg_accuracy = statistics.mean(forecast_accuracy_history)
        
        if avg_accuracy >= 0.90:
            return ConfidenceLevel.VERY_HIGH
        elif avg_accuracy >= 0.80:
            return ConfidenceLevel.HIGH
        elif avg_accuracy >= 0.70:
            return ConfidenceLevel.MEDIUM
        elif avg_accuracy >= 0.50:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.VERY_LOW
    
    @staticmethod
    def score_anomaly_detection(magnitude: float) -> ConfidenceLevel:
        """Score confidence in anomaly detection
        
        Args:
            magnitude: Standard deviations from mean
        """
        if magnitude > 4.0:
            return ConfidenceLevel.VERY_HIGH
        elif magnitude > 3.0:
            return ConfidenceLevel.HIGH
        elif magnitude > 2.0:
            return ConfidenceLevel.MEDIUM
        elif magnitude > 1.5:
            return ConfidenceLevel.LOW
        else:
            return ConfidenceLevel.VERY_LOW


class EnhancedPhase2Analyzer:
    """Complete Phase 2 analyzer with all Phase 1 enhancements"""
    
    def __init__(self):
        """Initialize analyzer with caching"""
        self._owner_cache = {}  # metric_name -> owner_info
        self._analysis_cache = {}  # (metric_name, current, target, prior, ly) -> insight
    
    def _get_cached_owner(self, metric_name: str) -> Dict[str, str]:
        """Get owner with caching"""
        if metric_name not in self._owner_cache:
            self._owner_cache[metric_name] = RecommendationEngine.get_owner(metric_name)
        return self._owner_cache[metric_name]
    
    def analyze(
        self,
        metric_name: str,
        current_value: float,
        target_value: float,
        prior_value: Optional[float] = None,
        ly_value: Optional[float] = None,
        two_periods_prior: Optional[float] = None,
    ) -> MetricInsight:
        """Analyze a single metric completely
        
        Args:
            metric_name: Name of metric
            current_value: Current period value
            target_value: Target for period
            prior_value: Prior period value (for MoM)
            ly_value: Same period last year (for YoY)
            two_periods_prior: Two periods ago (for momentum)
        
        Returns:
            Complete MetricInsight object
        """
        
        # Create insight object
        insight = MetricInsight(
            metric_name=metric_name,
            current_value=current_value,
            target_value=target_value,
            prior_value=prior_value,
            ly_value=ly_value,
        )
        
        # Calculate deltas
        insight.calculate_deltas()
        
        # Analyze trend
        if prior_value:
            trend = TrendAnalyzer.analyze(
                current=current_value,
                prior=prior_value,
                two_prior=two_periods_prior
            )
            insight.trend = trend
            insight.confidence = trend.confidence
        
        # Generate narrative
        insight.narrative = self._generate_narrative(
            metric_name=metric_name,
            current=current_value,
            target=target_value,
            prior=prior_value,
            ly=ly_value,
            trend=insight.trend,
            delta_target=insight.delta_target,
            delta_prior=insight.delta_prior,
        )
        
        # Generate recommendation
        recommendation = RecommendationEngine.generate_recommendation(
            metric_name=metric_name,
            current=current_value,
            target=target_value,
            prior=prior_value,
            trend=insight.trend,
            delta_target=insight.delta_target,
            delta_prior=insight.delta_prior,
        )
        
        if recommendation:
            insight.recommendations.append(recommendation)
        
        return insight
    
    def _generate_narrative(self,
                           metric_name: str,
                           current: float,
                           target: float,
                           prior: Optional[float],
                           ly: Optional[float],
                           trend: Optional[Trend],
                           delta_target: float,
                           delta_prior: float) -> str:
        """Generate narrative for metric"""
        
        parts = []
        
        # Opening
        status = "exceeded" if delta_target > 0 else "missed" if delta_target < -0.05 else "met"
        parts.append(f"{metric_name}: {current:.1f} ({status} target of {target:.1f}).")
        
        # Trend
        if trend:
            momentum_text = {
                "accelerating": "accelerating momentum",
                "stable": "steady momentum",
                "decelerating": "slowing momentum"
            }
            direction_symbol = {
                TrendDirection.UP: "↗️ up",
                TrendDirection.DOWN: "↘️ down",
                TrendDirection.FLAT: "→ flat"
            }
            parts.append(f"Trend is {direction_symbol[trend.direction]} with {momentum_text[trend.momentum]}.")
        
        # Comparisons
        if prior:
            parts.append(f"MoM: {delta_prior*100:+.1f}% ({current:.1f} vs {prior:.1f}).")
        
        if ly:
            parts.append(f"YoY: {(current - ly) / ly * 100:+.1f}% ({current:.1f} vs {ly:.1f}).")
        
        return " ".join(parts)


# Example usage
if __name__ == "__main__":
    analyzer = EnhancedPhase2Analyzer()
    
    # Example: Revenue
    revenue_insight = analyzer.analyze(
        metric_name="Revenue",
        current_value=14.2,
        target_value=13.8,
        prior_value=12.6,
        ly_value=13.0,
        two_periods_prior=11.2,
    )
    
    print("\n" + "="*60)
    print(f"METRIC: {revenue_insight.metric_name}")
    print("="*60)
    print(revenue_insight.to_dict())
    
    if revenue_insight.recommendations:
        print("\nRECOMMENDATIONS:")
        print("-" * 60)
        for i, rec in enumerate(revenue_insight.recommendations, 1):
            print(f"\n{i}. {rec.recommendation}")
            print(f"   Owner: {rec.owner}")
            print(f"   Severity: {rec.severity.name}")
            print(f"   Impact: {rec.impact_score}/10")
            print(f"   Success Criteria: {rec.success_criteria}")
            print(f"   Timeline: {rec.timeline}")
            print(f"   Confidence: {rec.confidence.value*100:.0f}%")