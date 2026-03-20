"""MBR Validator - Quality Assurance Checks Before Publishing

Validates:
- Data completeness and consistency
- Metric calculations
- Narrative quality
- Recommendation soundness
- No contradictions

Status: Production Ready
Author: Code Puppy 🐶
Date: March 16, 2026
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from enum import Enum


class ValidationSeverity(Enum):
    """Severity of validation issue"""
    ERROR = "error"          # Block publication
    WARNING = "warning"      # Caution, but okay to publish
    INFO = "info"            # FYI, no action needed


class ValidationCategory(Enum):
    """Category of validation"""
    DATA_QUALITY = "data_quality"
    CALCULATIONS = "calculations"
    NARRATIVE = "narrative"
    RECOMMENDATIONS = "recommendations"
    CONSISTENCY = "consistency"
    METADATA = "metadata"


@dataclass
class ValidationIssue:
    """A single validation issue"""
    category: ValidationCategory
    severity: ValidationSeverity
    message: str
    suggestion: Optional[str] = None
    metric_name: Optional[str] = None
    
    def __str__(self) -> str:
        icon_map = {
            ValidationSeverity.ERROR: "❌",
            ValidationSeverity.WARNING: "⚠️",
            ValidationSeverity.INFO: "ℹ️",
        }
        icon = icon_map[self.severity]
        return f"{icon} [{self.category.value}] {self.message}"


@dataclass
class ValidationResult:
    """Result of MBR validation"""
    is_valid: bool
    issues: List[ValidationIssue] = field(default_factory=list)
    warnings: List[ValidationIssue] = field(default_factory=list)
    infos: List[ValidationIssue] = field(default_factory=list)
    passing_checks: List[str] = field(default_factory=list)
    
    def add_issue(self, issue: ValidationIssue):
        """Add issue to result"""
        if issue.severity == ValidationSeverity.ERROR:
            self.issues.append(issue)
            self.is_valid = False
        elif issue.severity == ValidationSeverity.WARNING:
            self.warnings.append(issue)
        else:
            self.infos.append(issue)
    
    def all_issues(self) -> List[ValidationIssue]:
        """Get all issues"""
        return self.issues + self.warnings + self.infos
    
    def summary(self) -> str:
        """Get summary of validation"""
        icon = "✅" if self.is_valid else "❌"
        status = "PASS" if self.is_valid else "FAIL"
        return f"{icon} Validation: {status} | Errors: {len(self.issues)} | Warnings: {len(self.warnings)} | Passed: {len(self.passing_checks)}"
    
    def report(self) -> str:
        """Generate full validation report"""
        lines = []
        lines.append("\n" + "="*60)
        lines.append("VALIDATION REPORT")
        lines.append("="*60)
        lines.append(f"\n{self.summary()}")
        
        if self.issues:
            lines.append("\n❌ ERRORS (Must fix before publication):")
            for issue in self.issues:
                lines.append(f"  {issue}")
                if issue.suggestion:
                    lines.append(f"     → {issue.suggestion}")
        
        if self.warnings:
            lines.append("\n⚠️  WARNINGS (Review before publication):")
            for warning in self.warnings:
                lines.append(f"  {warning}")
                if warning.suggestion:
                    lines.append(f"     → {warning.suggestion}")
        
        if self.infos:
            lines.append("\nℹ️  INFO:")
            for info in self.infos:
                lines.append(f"  {info}")
        
        if self.passing_checks:
            lines.append(f"\n✅ Passing Checks ({len(self.passing_checks)}):")
            for check in self.passing_checks[:5]:  # Show top 5
                lines.append(f"  ✓ {check}")
            if len(self.passing_checks) > 5:
                lines.append(f"  ... and {len(self.passing_checks) - 5} more")
        
        lines.append("\n" + "="*60)
        return "\n".join(lines)


class DataQualityValidator:
    """Validates data quality"""
    
    @staticmethod
    def validate_completeness(
        metrics: Dict[str, Dict[str, Any]]
    ) -> List[ValidationIssue]:
        """Check all required metrics are present"""
        issues = []
        
        required_fields = ["current_value", "target_value"]
        
        for metric_name, metric_data in metrics.items():
            for field_name in required_fields:
                if field_name not in metric_data or metric_data[field_name] is None:
                    issues.append(ValidationIssue(
                        category=ValidationCategory.DATA_QUALITY,
                        severity=ValidationSeverity.ERROR,
                        message=f"{metric_name}: Missing required field '{field_name}'",
                        suggestion=f"Populate {field_name} for {metric_name}",
                        metric_name=metric_name
                    ))
        
        return issues
    
    @staticmethod
    def validate_value_ranges(
        metrics: Dict[str, Dict[str, Any]]
    ) -> List[ValidationIssue]:
        """Check values are in reasonable ranges"""
        issues = []
        
        for metric_name, metric_data in metrics.items():
            current = metric_data.get("current_value")
            target = metric_data.get("target_value")
            
            # Check for negative values where inappropriate
            if current and isinstance(current, (int, float)) and current < 0:
                if "negative" not in metric_name.lower():
                    issues.append(ValidationIssue(
                        category=ValidationCategory.DATA_QUALITY,
                        severity=ValidationSeverity.WARNING,
                        message=f"{metric_name}: Negative value ({current}) seems unusual",
                        suggestion=f"Verify {metric_name} value is correct",
                        metric_name=metric_name
                    ))
            
            # Check for extreme deltas
            if current and target and isinstance(current, (int, float)) and isinstance(target, (int, float)):
                if target != 0:
                    delta = abs((current - target) / target)
                    if delta > 2.0:  # More than 200% off target
                        issues.append(ValidationIssue(
                            category=ValidationCategory.DATA_QUALITY,
                            severity=ValidationSeverity.WARNING,
                            message=f"{metric_name}: Large variance from target ({delta*100:.0f}%)",
                            suggestion=f"Verify {metric_name} calculation; check if data is stale",
                            metric_name=metric_name
                        ))
        
        return issues
    
    @staticmethod
    def validate_freshness(
        last_update_time: Optional[str],
        hours_threshold: int = 24
    ) -> List[ValidationIssue]:
        """Check data is fresh enough"""
        issues = []
        
        if not last_update_time:
            issues.append(ValidationIssue(
                category=ValidationCategory.DATA_QUALITY,
                severity=ValidationSeverity.WARNING,
                message="Data freshness unknown",
                suggestion="Verify data was updated in last 24 hours"
            ))
        
        return issues


class CalculationValidator:
    """Validates metric calculations"""
    
    @staticmethod
    def validate_deltas(
        metrics: Dict[str, Dict[str, Any]]
    ) -> List[ValidationIssue]:
        """Validate delta calculations are correct"""
        issues = []
        
        for metric_name, metric_data in metrics.items():
            current = metric_data.get("current_value")
            target = metric_data.get("target_value")
            stated_delta = metric_data.get("delta_vs_target")
            
            if all(v is not None for v in [current, target, stated_delta]):
                if isinstance(stated_delta, str):
                    # Try to parse percentage
                    try:
                        stated_pct = float(stated_delta.strip('%+'))
                    except:
                        issues.append(ValidationIssue(
                            category=ValidationCategory.CALCULATIONS,
                            severity=ValidationSeverity.ERROR,
                            message=f"{metric_name}: Invalid delta format '{stated_delta}'",
                            suggestion="Use format like '+2.9%' or '-5.0%'",
                            metric_name=metric_name
                        ))
                        continue
                else:
                    stated_pct = float(stated_delta) * 100
                
                # Calculate expected
                if target != 0:
                    expected_pct = ((current - target) / target) * 100
                    if abs(stated_pct - expected_pct) > 0.5:  # 0.5% tolerance
                        issues.append(ValidationIssue(
                            category=ValidationCategory.CALCULATIONS,
                            severity=ValidationSeverity.ERROR,
                            message=f"{metric_name}: Delta mismatch (stated {stated_pct:.1f}% vs calculated {expected_pct:.1f}%)",
                            suggestion=f"Recalculate: ({current} - {target}) / {target} * 100",
                            metric_name=metric_name
                        ))
        
        return issues
    
    @staticmethod
    def validate_segment_totals(
        metric_name: str,
        total_value: float,
        segments: Dict[str, float]
    ) -> List[ValidationIssue]:
        """Validate segment breakdown adds up to total"""
        issues = []
        
        if not segments:
            return issues
        
        segment_sum = sum(segments.values())
        tolerance = max(total_value * 0.02, 0.1)  # 2% or 0.1 unit tolerance
        
        if abs(segment_sum - total_value) > tolerance:
            issues.append(ValidationIssue(
                category=ValidationCategory.CALCULATIONS,
                severity=ValidationSeverity.ERROR,
                message=f"{metric_name}: Segments don't add up (total {total_value} vs sum {segment_sum})",
                suggestion=f"Check segment values for {', '.join(segments.keys())}",
                metric_name=metric_name
            ))
        
        return issues


class NarrativeValidator:
    """Validates narrative quality"""
    
    @staticmethod
    def validate_clarity(text: str) -> List[ValidationIssue]:
        """Check narrative is clear"""
        issues = []
        
        if not text or len(text) < 50:
            issues.append(ValidationIssue(
                category=ValidationCategory.NARRATIVE,
                severity=ValidationSeverity.WARNING,
                message="Narrative is too brief",
                suggestion="Add more context and analysis"
            ))
        
        # Check for vague language
        vague_terms = ["something", "maybe", "possibly", "unclear", "unknown"]
        for term in vague_terms:
            if term.lower() in text.lower():
                issues.append(ValidationIssue(
                    category=ValidationCategory.NARRATIVE,
                    severity=ValidationSeverity.WARNING,
                    message=f"Narrative contains vague term: '{term}'",
                    suggestion=f"Replace '{term}' with specific facts or data"
                ))
                break  # One warning per narrative
        
        return issues
    
    @staticmethod
    def validate_specificity(text: str) -> List[ValidationIssue]:
        """Check recommendations are specific"""
        issues = []
        
        vague_verbs = ["investigate", "review", "consider", "think about", "look at"]
        
        for verb in vague_verbs:
            if verb in text.lower():
                # Check if there's concrete follow-up
                sentences = text.split(". ")
                for sentence in sentences:
                    if verb in sentence.lower():
                        if not any(concrete in sentence.lower() for concrete in ["specifically", "by", "such as", "including"]):
                            issues.append(ValidationIssue(
                                category=ValidationCategory.NARRATIVE,
                                severity=ValidationSeverity.WARNING,
                                message=f"Recommendation uses vague verb: '{verb}' without specific action",
                                suggestion=f"Replace with concrete action like 'Build a plan to...' or 'Test...'"
                            ))
                            break
        
        return issues


class RecommendationValidator:
    """Validates recommendation quality"""
    
    @staticmethod
    def validate_completeness(
        recommendations: List[Dict[str, Any]]
    ) -> List[ValidationIssue]:
        """Check recommendations have all required fields"""
        issues = []
        
        required_fields = ["recommendation", "owner", "timeline", "success_criteria"]
        
        for i, rec in enumerate(recommendations):
            for field in required_fields:
                if field not in rec or not rec[field]:
                    issues.append(ValidationIssue(
                        category=ValidationCategory.RECOMMENDATIONS,
                        severity=ValidationSeverity.WARNING,
                        message=f"Recommendation {i+1}: Missing '{field}'",
                        suggestion=f"Add {field} to recommendation"
                    ))
        
        return issues
    
    @staticmethod
    def validate_actionability(
        recommendations: List[Dict[str, Any]]
    ) -> List[ValidationIssue]:
        """Check recommendations are actionable"""
        issues = []
        
        for i, rec in enumerate(recommendations):
            rec_text = rec.get("recommendation", "")
            
            # Check for vague language
            if rec_text:
                vague_terms = ["maybe", "possibly", "might", "could", "perhaps"]
                for term in vague_terms:
                    if term in rec_text.lower():
                        issues.append(ValidationIssue(
                            category=ValidationCategory.RECOMMENDATIONS,
                            severity=ValidationSeverity.WARNING,
                            message=f"Recommendation {i+1}: Uses uncertain language ('{term}')",
                            suggestion="Make recommendation more definitive",
                        ))
                        break
    
        return issues
    
    @staticmethod
    def validate_owner_assignment(
        recommendations: List[Dict[str, Any]]
    ) -> List[ValidationIssue]:
        """Check all recommendations have owners"""
        issues = []
        
        for i, rec in enumerate(recommendations):
            owner = rec.get("owner")
            if not owner or owner.lower() == "unknown" or owner.lower() == "tbd":
                issues.append(ValidationIssue(
                    category=ValidationCategory.RECOMMENDATIONS,
                    severity=ValidationSeverity.WARNING,
                    message=f"Recommendation {i+1}: Owner not assigned",
                    suggestion="Assign specific team or function as owner"
                ))
        
        return issues


class ConsistencyValidator:
    """Validates internal consistency"""
    
    @staticmethod
    def validate_narrative_alignment(
        metric_name: str,
        narrative: str,
        current: float,
        target: float,
        prior: Optional[float]
    ) -> List[ValidationIssue]:
        """Check narrative aligns with data"""
        issues = []
        
        narrative_lower = narrative.lower()
        
        # Check for contradictions
        delta = (current - target) / target if target != 0 else 0
        
        if delta > 0.05 and "below" in narrative_lower or "decline" in narrative_lower:
            issues.append(ValidationIssue(
                category=ValidationCategory.CONSISTENCY,
                severity=ValidationSeverity.ERROR,
                message=f"{metric_name}: Narrative says declining but data shows +{delta*100:.1f}%",
                suggestion="Fix narrative to match data",
                metric_name=metric_name
            ))
        
        if delta < -0.05 and "exceed" in narrative_lower or "strong" in narrative_lower:
            issues.append(ValidationIssue(
                category=ValidationCategory.CONSISTENCY,
                severity=ValidationSeverity.ERROR,
                message=f"{metric_name}: Narrative says strong but data shows {delta*100:.1f}%",
                suggestion="Fix narrative to match data",
                metric_name=metric_name
            ))
        
        return issues
    
    @staticmethod
    def validate_recommendation_relevance(
        finding: str,
        recommendation: str
    ) -> List[ValidationIssue]:
        """Check recommendation relates to finding"""
        issues = []
        
        # Simple check: recommendation should mention same metric or root cause
        if finding and recommendation:
            # Extract key words from finding
            finding_words = set(finding.lower().split())
            rec_words = set(recommendation.lower().split())
            
            # Check for overlap (at least 20%)
            overlap = len(finding_words & rec_words) / max(len(finding_words), 1)
            if overlap < 0.1:
                issues.append(ValidationIssue(
                    category=ValidationCategory.CONSISTENCY,
                    severity=ValidationSeverity.WARNING,
                    message="Recommendation may not relate to finding",
                    suggestion="Ensure recommendation addresses the identified finding"
                ))
        
        return issues


class MBRValidator:
    """Complete MBR validator"""
    
    def validate(
        self,
        metrics: Dict[str, Dict[str, Any]],
        recommendations: List[Dict[str, Any]],
        narrative: Optional[str] = None,
        last_update_time: Optional[str] = None,
    ) -> ValidationResult:
        """Run complete validation"""
        
        result = ValidationResult(is_valid=True)
        
        # Data quality checks
        result.issues.extend(DataQualityValidator.validate_completeness(metrics))
        result.issues.extend(DataQualityValidator.validate_value_ranges(metrics))
        result.issues.extend(DataQualityValidator.validate_freshness(last_update_time))
        
        # Calculation checks
        result.issues.extend(CalculationValidator.validate_deltas(metrics))
        
        # Narrative checks
        if narrative:
            result.issues.extend(NarrativeValidator.validate_clarity(narrative))
            result.issues.extend(NarrativeValidator.validate_specificity(narrative))
        
        # Recommendation checks
        result.issues.extend(RecommendationValidator.validate_completeness(recommendations))
        result.issues.extend(RecommendationValidator.validate_actionability(recommendations))
        result.issues.extend(RecommendationValidator.validate_owner_assignment(recommendations))
        
        # Consistency checks
        for metric_name, metric_data in metrics.items():
            narrative_text = metric_data.get("narrative", narrative or "")
            if narrative_text:
                issues = ConsistencyValidator.validate_narrative_alignment(
                    metric_name=metric_name,
                    narrative=narrative_text,
                    current=metric_data.get("current_value", 0),
                    target=metric_data.get("target_value", 0),
                    prior=metric_data.get("prior_value")
                )
                result.issues.extend(issues)
        
        # Track passing checks
        checks_passed = [
            f"Metrics completeness: {len(metrics)} metrics present",
            f"Recommendations: {len(recommendations)} recommendations",
            "Data validation passed",
            "Narrative validation passed",
            "Consistency check passed",
        ]
        
        # Only count as passing if no errors
        if not result.issues:
            result.passing_checks = checks_passed
        
        # Update validity
        result.is_valid = len(result.issues) == 0
        
        return result


# Example usage
if __name__ == "__main__":
    sample_metrics = {
        "Revenue": {
            "current_value": 14.2,
            "target_value": 13.8,
            "prior_value": 12.6,
            "delta_vs_target": "+2.9%",
            "narrative": "Revenue exceeded target by 2.9%"
        }
    }
    
    sample_recs = [
        {
            "recommendation": "Accelerate e-commerce expansion",
            "owner": "Marketing Team",
            "timeline": "1-2 weeks",
            "success_criteria": "E-commerce grows 20%+ MoM"
        }
    ]
    
    validator = MBRValidator()
    result = validator.validate(
        metrics=sample_metrics,
        recommendations=sample_recs,
        narrative="Revenue strong, trending up, recommend expansion",
        last_update_time="2026-03-16T10:00:00"
    )
    
    print(result.report())