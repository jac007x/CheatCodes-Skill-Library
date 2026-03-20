"""Performance Tracker - Measures MBR System Quality & Impact

Tracks:
- Recommendation adoption rates
- Forecast accuracy
- Anomaly detection quality
- Execution speed
- Business impact
- Stakeholder satisfaction

Status: Production Ready
Author: Code Puppy 🐶
Date: March 16, 2026
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
import json


@dataclass
class MetricPerformance:
    """Performance stats for a metric"""
    metric_name: str
    forecast_value: float
    actual_value: float
    forecast_accuracy: float = 0.0
    recommendations_count: int = 0
    recommendations_adopted: int = 0
    adoption_rate: float = 0.0
    impact_score: float = 0.0  # 0-10
    
    def calculate_forecast_accuracy(self):
        """Calculate forecast accuracy as percentage"""
        if self.forecast_value == 0:
            self.forecast_accuracy = 0.0
        else:
            error = abs(self.actual_value - self.forecast_value) / self.forecast_value
            self.forecast_accuracy = max(0, 1 - error)
    
    def calculate_adoption_rate(self):
        """Calculate adoption rate of recommendations"""
        if self.recommendations_count == 0:
            self.adoption_rate = 0.0
        else:
            self.adoption_rate = self.recommendations_adopted / self.recommendations_count
    
    def to_dict(self) -> Dict:
        return {
            "metric": self.metric_name,
            "forecast": self.forecast_value,
            "actual": self.actual_value,
            "forecast_accuracy": f"{self.forecast_accuracy*100:.1f}%",
            "recommendations": self.recommendations_count,
            "adopted": self.recommendations_adopted,
            "adoption_rate": f"{self.adoption_rate*100:.1f}%",
            "impact_score": f"{self.impact_score}/10"
        }


@dataclass
class ExecutionMetrics:
    """Tracks execution performance"""
    mbr_generation_time_hours: float
    recommendation_turnaround_time_hours: float
    jira_creation_time_hours: float
    publication_delay_hours: float
    total_cycle_time_hours: float = 0.0
    
    def calculate_total(self):
        """Calculate total cycle time"""
        self.total_cycle_time_hours = (
            self.mbr_generation_time_hours +
            self.recommendation_turnaround_time_hours +
            self.jira_creation_time_hours +
            self.publication_delay_hours
        )
    
    def to_dict(self) -> Dict:
        return {
            "mbr_generation_hours": self.mbr_generation_time_hours,
            "recommendation_turnaround_hours": self.recommendation_turnaround_time_hours,
            "jira_creation_hours": self.jira_creation_time_hours,
            "publication_delay_hours": self.publication_delay_hours,
            "total_cycle_time_hours": self.total_cycle_time_hours
        }


@dataclass
class AnomalyDetectionPerformance:
    """Tracks anomaly detection quality"""
    total_anomalies_detected: int = 0
    true_positives: int = 0  # Real anomalies
    false_positives: int = 0  # False alarms
    false_negatives: int = 0  # Missed anomalies
    sensitivity: float = 0.0  # True positive rate
    precision: float = 0.0  # Accuracy
    f1_score: float = 0.0  # Balanced metric
    
    def calculate_metrics(self):
        """Calculate detection metrics"""
        # Sensitivity: true_positives / (true_positives + false_negatives)
        if self.true_positives + self.false_negatives > 0:
            self.sensitivity = self.true_positives / (self.true_positives + self.false_negatives)
        
        # Precision: true_positives / (true_positives + false_positives)
        if self.true_positives + self.false_positives > 0:
            self.precision = self.true_positives / (self.true_positives + self.false_positives)
        
        # F1 Score: 2 * (precision * sensitivity) / (precision + sensitivity)
        if self.precision + self.sensitivity > 0:
            self.f1_score = 2 * (self.precision * self.sensitivity) / (self.precision + self.sensitivity)
    
    def to_dict(self) -> Dict:
        return {
            "total_detected": self.total_anomalies_detected,
            "true_positives": self.true_positives,
            "false_positives": self.false_positives,
            "false_negatives": self.false_negatives,
            "sensitivity": f"{self.sensitivity*100:.1f}%",
            "precision": f"{self.precision*100:.1f}%",
            "f1_score": f"{self.f1_score:.3f}"
        }


@dataclass
class StakeholderSatisfaction:
    """Tracks stakeholder satisfaction metrics"""
    nps_score: float = 0.0  # Net Promoter Score (-100 to +100)
    usefulness_rating: float = 0.0  # 1-5
    clarity_rating: float = 0.0  # 1-5
    actionability_rating: float = 0.0  # 1-5
    overall_satisfaction: float = 0.0  # 1-5
    
    # Breakdown
    promoters: int = 0  # 9-10
    passives: int = 0  # 7-8
    detractors: int = 0  # 0-6
    
    def calculate_nps(self):
        """Calculate NPS from promoters/detractors"""
        total = self.promoters + self.passives + self.detractors
        if total > 0:
            self.nps_score = ((self.promoters - self.detractors) / total) * 100
    
    def calculate_overall_satisfaction(self):
        """Calculate overall from component ratings"""
        ratings = [self.usefulness_rating, self.clarity_rating, self.actionability_rating]
        if any(ratings):
            self.overall_satisfaction = sum(ratings) / len(ratings)
    
    def to_dict(self) -> Dict:
        return {
            "nps_score": f"{self.nps_score:.0f}",
            "promoters": self.promoters,
            "passives": self.passives,
            "detractors": self.detractors,
            "usefulness_rating": f"{self.usefulness_rating:.1f}/5",
            "clarity_rating": f"{self.clarity_rating:.1f}/5",
            "actionability_rating": f"{self.actionability_rating:.1f}/5",
            "overall_satisfaction": f"{self.overall_satisfaction:.1f}/5"
        }


@dataclass
class BusinessImpact:
    """Tracks business impact from MBR recommendations"""
    revenue_impact_dollars: float = 0.0
    efficiency_gain_percent: float = 0.0
    risk_avoided_dollars: float = 0.0
    customer_satisfaction_delta: float = 0.0  # NPS point change
    decision_speed_improvement_percent: float = 0.0
    
    total_value_created: float = 0.0
    
    def calculate_total_value(self):
        """Sum all impact sources"""
        # Rough calculation: revenue + efficiency value + risk avoided
        # (Note: customer satisfaction delta harder to monetize, so weight lightly)
        efficiency_dollars = self.efficiency_gain_percent * 100000  # Rough estimate
        customer_value = self.customer_satisfaction_delta * 50000  # Rough estimate
        
        self.total_value_created = (
            self.revenue_impact_dollars +
            efficiency_dollars +
            self.risk_avoided_dollars +
            customer_value
        )
    
    def to_dict(self) -> Dict:
        return {
            "revenue_impact": f"${self.revenue_impact_dollars:,.0f}",
            "efficiency_gain": f"{self.efficiency_gain_percent:+.1f}%",
            "risk_avoided": f"${self.risk_avoided_dollars:,.0f}",
            "customer_satisfaction_delta": f"{self.customer_satisfaction_delta:+.1f} pts",
            "decision_speed_improvement": f"{self.decision_speed_improvement_percent:+.1f}%",
            "total_value_created": f"${self.total_value_created:,.0f}"
        }


@dataclass
class MBRPerformanceReport:
    """Complete performance report for an MBR month"""
    mbr_month: str
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    # Components
    metric_performance: List[MetricPerformance] = field(default_factory=list)
    execution_metrics: Optional[ExecutionMetrics] = None
    anomaly_detection: Optional[AnomalyDetectionPerformance] = None
    stakeholder_satisfaction: Optional[StakeholderSatisfaction] = None
    business_impact: Optional[BusinessImpact] = None
    
    # Summary scores
    quality_score: float = 0.0  # 0-10
    adoption_score: float = 0.0  # 0-10
    impact_score: float = 0.0  # 0-10
    overall_score: float = 0.0  # 0-10
    
    def calculate_quality_score(self) -> float:
        """Calculate quality score based on components"""
        components = []
        
        # Forecast accuracy contribution
        if self.metric_performance:
            avg_accuracy = sum(m.forecast_accuracy for m in self.metric_performance) / len(self.metric_performance)
            components.append(avg_accuracy * 10)
        
        # Anomaly detection quality
        if self.anomaly_detection:
            components.append(self.anomaly_detection.f1_score * 10)
        
        # Clarity/usefulness
        if self.stakeholder_satisfaction:
            components.append(self.stakeholder_satisfaction.clarity_rating * 2)
            components.append(self.stakeholder_satisfaction.usefulness_rating * 2)
        
        if components:
            self.quality_score = sum(components) / len(components)
        
        return round(self.quality_score, 2)
    
    def calculate_adoption_score(self) -> float:
        """Calculate adoption score"""
        components = []
        
        # Recommendation adoption rates
        if self.metric_performance:
            avg_adoption = sum(m.adoption_rate for m in self.metric_performance) / len(self.metric_performance)
            components.append(avg_adoption * 10)
        
        # Stakeholder actionability rating
        if self.stakeholder_satisfaction:
            components.append(self.stakeholder_satisfaction.actionability_rating * 2)
        
        if components:
            self.adoption_score = sum(components) / len(components)
        
        return round(self.adoption_score, 2)
    
    def calculate_impact_score(self) -> float:
        """Calculate impact score"""
        components = []
        
        # Business value created
        if self.business_impact:
            # Normalize to 10-point scale (assume $500k is excellent)
            impact_value = min(10, self.business_impact.total_value_created / 50000)
            components.append(impact_value)
        
        # Metric improvements
        if self.metric_performance:
            avg_impact = sum(m.impact_score for m in self.metric_performance) / len(self.metric_performance)
            components.append(avg_impact)
        
        if components:
            self.impact_score = sum(components) / len(components)
        
        return round(self.impact_score, 2)
    
    def calculate_overall_score(self) -> float:
        """Calculate overall score (weighted average)"""
        # Weights: Quality 40%, Adoption 35%, Impact 25%
        self.overall_score = (
            self.calculate_quality_score() * 0.40 +
            self.calculate_adoption_score() * 0.35 +
            self.calculate_impact_score() * 0.25
        )
        
        return round(self.overall_score, 2)
    
    def grade(self) -> str:
        """Convert score to letter grade"""
        score = self.calculate_overall_score()
        
        if score >= 9.0:
            return "A+"
        elif score >= 8.5:
            return "A"
        elif score >= 8.0:
            return "A-"
        elif score >= 7.5:
            return "B+"
        elif score >= 7.0:
            return "B"
        elif score >= 6.5:
            return "B-"
        elif score >= 6.0:
            return "C+"
        elif score >= 5.0:
            return "C"
        else:
            return "Below C"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "mbr_month": self.mbr_month,
            "generated_at": self.generated_at,
            "quality_score": f"{self.calculate_quality_score():.1f}/10",
            "adoption_score": f"{self.calculate_adoption_score():.1f}/10",
            "impact_score": f"{self.calculate_impact_score():.1f}/10",
            "overall_score": f"{self.calculate_overall_score():.1f}/10",
            "grade": self.grade(),
            "metrics": [m.to_dict() for m in self.metric_performance],
            "execution": self.execution_metrics.to_dict() if self.execution_metrics else None,
            "anomaly_detection": self.anomaly_detection.to_dict() if self.anomaly_detection else None,
            "satisfaction": self.stakeholder_satisfaction.to_dict() if self.stakeholder_satisfaction else None,
            "business_impact": self.business_impact.to_dict() if self.business_impact else None,
        }
    
    def report(self) -> str:
        """Generate text report"""
        lines = []
        lines.append("\n" + "="*70)
        lines.append(f"MBR PERFORMANCE REPORT: {self.mbr_month}")
        lines.append("="*70)
        
        # Overall scores
        lines.append("\n📊 PERFORMANCE SUMMARY:")
        lines.append("-" * 70)
        lines.append(f"Overall Score: {self.calculate_overall_score():.1f}/10 ({self.grade()})")
        lines.append(f"Quality Score: {self.calculate_quality_score():.1f}/10")
        lines.append(f"Adoption Score: {self.calculate_adoption_score():.1f}/10")
        lines.append(f"Impact Score: {self.calculate_impact_score():.1f}/10")
        
        # Metric performance
        if self.metric_performance:
            lines.append("\n📈 METRIC PERFORMANCE:")
            lines.append("-" * 70)
            for metric in self.metric_performance:
                lines.append(f"\n{metric.metric_name}:")
                lines.append(f"  Forecast Accuracy: {metric.forecast_accuracy*100:.1f}%")
                lines.append(f"  Adoption Rate: {metric.adoption_rate*100:.1f}%")
        
        # Execution metrics
        if self.execution_metrics:
            lines.append("\n⏱️ EXECUTION METRICS:")
            lines.append("-" * 70)
            lines.append(f"Total Cycle Time: {self.execution_metrics.total_cycle_time_hours:.1f} hours")
        
        # Business impact
        if self.business_impact:
            lines.append("\n💰 BUSINESS IMPACT:")
            lines.append("-" * 70)
            lines.append(f"Total Value Created: ${self.business_impact.total_value_created:,.0f}")
        
        lines.append("\n" + "="*70)
        
        return "\n".join(lines)


class PerformanceTracker:
    """Main performance tracking interface"""
    
    def __init__(self):
        self.reports: Dict[str, MBRPerformanceReport] = {}
    
    def create_report(self, mbr_month: str) -> MBRPerformanceReport:
        """Create new performance report"""
        report = MBRPerformanceReport(mbr_month=mbr_month)
        self.reports[mbr_month] = report
        return report
    
    def get_report(self, mbr_month: str) -> Optional[MBRPerformanceReport]:
        """Get existing report"""
        return self.reports.get(mbr_month)
    
    def compare_periods(self, month1: str, month2: str) -> Dict:
        """Compare two months"""
        report1 = self.get_report(month1)
        report2 = self.get_report(month2)
        
        if not report1 or not report2:
            return {"error": "One or both reports not found"}
        
        return {
            "month1": month1,
            "month2": month2,
            "score_improvement": f"{report2.calculate_overall_score() - report1.calculate_overall_score():+.1f}",
            "quality_improvement": f"{report2.calculate_quality_score() - report1.calculate_quality_score():+.1f}",
            "adoption_improvement": f"{report2.calculate_adoption_score() - report1.calculate_adoption_score():+.1f}",
            "impact_improvement": f"{report2.calculate_impact_score() - report1.calculate_impact_score():+.1f}",
        }


# Example usage
if __name__ == "__main__":
    tracker = PerformanceTracker()
    
    # Create report for March
    report = tracker.create_report("March 2026")
    
    # Add metric performance
    revenue_perf = MetricPerformance(
        metric_name="Revenue",
        forecast_value=13.8,
        actual_value=14.2,
        recommendations_count=3,
        recommendations_adopted=2,
        impact_score=8.5
    )
    revenue_perf.calculate_forecast_accuracy()
    revenue_perf.calculate_adoption_rate()
    report.metric_performance.append(revenue_perf)
    
    # Add execution metrics
    report.execution_metrics = ExecutionMetrics(
        mbr_generation_time_hours=3.5,
        recommendation_turnaround_time_hours=2.0,
        jira_creation_time_hours=1.0,
        publication_delay_hours=0.5
    )
    report.execution_metrics.calculate_total()
    
    # Add business impact
    report.business_impact = BusinessImpact(
        revenue_impact_dollars=250000,
        efficiency_gain_percent=5.2,
        risk_avoided_dollars=100000,
        customer_satisfaction_delta=2.5
    )
    report.business_impact.calculate_total_value()
    
    # Add satisfaction
    report.stakeholder_satisfaction = StakeholderSatisfaction(
        promoters=8,
        passives=3,
        detractors=1,
        usefulness_rating=4.2,
        clarity_rating=4.1,
        actionability_rating=3.9
    )
    report.stakeholder_satisfaction.calculate_nps()
    report.stakeholder_satisfaction.calculate_overall_satisfaction()
    
    print(report.report())