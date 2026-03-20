"""Tests for Phase 1 MBR Improvements

Tests all components:
- Enhanced insight engine
- Summary generators
- Validators
- Template library
- Performance tracker
- Orchestrator

Status: Production Ready
Author: Code Puppy 🐶
Date: March 16, 2026
"""

import sys
from datetime import datetime

# Import all modules
from enhanced_insight_engine import (
    EnhancedPhase2Analyzer,
    TrendAnalyzer,
    TrendDirection,
    RecommendationEngine,
    ConfidenceScorer,
)

from summary_generators import (
    SummaryGenerator,
    AudienceRole,
    generate_all_summaries,
)

from mbr_validator import (
    MBRValidator,
    DataQualityValidator,
    CalculationValidator,
)

from template_library import (
    JiraTicketTemplate,
    SurveyTemplate,
    EmailTemplate,
    TeamsMessageTemplate,
)

from performance_tracker import (
    PerformanceTracker,
    MetricPerformance,
)

from phase1_orchestrator import Phase1Orchestrator


class TestResults:
    """Track test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def add_pass(self, test_name):
        self.passed += 1
        print(f"✅ {test_name}")
    
    def add_fail(self, test_name, reason):
        self.failed += 1
        self.errors.append(f"{test_name}: {reason}")
        print(f"❌ {test_name}: {reason}")
    
    def summary(self):
        total = self.passed + self.failed
        percentage = (self.passed / total * 100) if total > 0 else 0
        return f"Results: {self.passed}/{total} passed ({percentage:.1f}%)"


def test_enhanced_insight_engine():
    """Test insight analysis"""
    print("\n" + "="*60)
    print("TEST: Enhanced Insight Engine")
    print("="*60)
    results = TestResults()
    
    analyzer = EnhancedPhase2Analyzer()
    
    # Test 1: Basic analysis
    try:
        insight = analyzer.analyze(
            metric_name="Revenue",
            current_value=14.2,
            target_value=13.8,
            prior_value=12.6,
            ly_value=13.0,
            two_periods_prior=11.2,
        )
        
        assert insight.metric_name == "Revenue", "Metric name mismatch"
        assert insight.current_value == 14.2, "Current value mismatch"
        assert len(insight.recommendations) > 0, "No recommendations generated"
        results.add_pass("Basic metric analysis")
    except Exception as e:
        results.add_fail("Basic metric analysis", str(e))
    
    # Test 2: Recommendation generation
    try:
        rec = RecommendationEngine.generate_recommendation(
            metric_name="Revenue",
            current=14.2,
            target=13.8,
            prior=12.6,
        )
        
        assert rec is not None, "No recommendation generated"
        assert rec.owner is not None, "Owner not assigned"
        assert rec.success_criteria is not None, "Success criteria missing"
        results.add_pass("Recommendation generation")
    except Exception as e:
        results.add_fail("Recommendation generation", str(e))
    
    # Test 3: Trend analysis
    try:
        trend = TrendAnalyzer.analyze(
            current=14.2,
            prior=12.6,
            two_prior=11.2,
        )
        
        assert trend.direction == TrendDirection.UP, "Trend direction wrong"
        assert trend.momentum in ["accelerating", "stable", "decelerating"], "Invalid momentum"
        results.add_pass("Trend analysis")
    except Exception as e:
        results.add_fail("Trend analysis", str(e))
    
    # Test 4: Confidence scoring
    try:
        conf = ConfidenceScorer.score_forecast([0.95, 0.92, 0.98])
        assert conf.value >= 0.85, "Confidence score too low"
        results.add_pass("Confidence scoring")
    except Exception as e:
        results.add_fail("Confidence scoring", str(e))
    
    print(f"\n{results.summary()}")
    return results


def test_summary_generators():
    """Test summary generation"""
    print("\n" + "="*60)
    print("TEST: Summary Generators")
    print("="*60)
    results = TestResults()
    
    gen = SummaryGenerator()
    
    sample_metrics = {
        "Revenue": {"current": 14.2, "target": 13.8, "delta_vs_target": "+2.9%"},
        "CAC": {"current": 42, "target": 45, "delta_vs_target": "-6.7%"},
    }
    
    sample_recs = [
        {"recommendation": "Accelerate e-commerce", "owner": "Marketing", "timeline": "1 week"},
    ]
    
    # Test 1: Short summary
    try:
        short = gen.generate_short_summary(sample_metrics, [r["recommendation"] for r in sample_recs])
        assert "QUICK SUMMARY" in short, "Short summary format wrong"
        assert len(short) < 800, "Short summary too long"
        results.add_pass("Short summary generation")
    except Exception as e:
        results.add_fail("Short summary generation", str(e))
    
    # Test 2: Full summary
    try:
        full = gen.generate_full_summary(
            title="MBR",
            key_metrics=sample_metrics,
            findings=["Revenue strong"],
            recommendations=sample_recs,
            anomalies=[],
        )
        assert "EXECUTIVE SUMMARY" in full, "Full summary format wrong"
        assert "PERFORMANCE METRICS" in full, "Metrics section missing"
        results.add_pass("Full summary generation")
    except Exception as e:
        results.add_fail("Full summary generation", str(e))
    
    # Test 3: Role-based summaries
    try:
        cfo = gen.generate_cfo_summary(sample_metrics, sample_recs)
        assert "FOR CFO" in cfo, "CFO summary header wrong"
        results.add_pass("CFO summary generation")
        
        coo = gen.generate_coo_summary(sample_metrics, sample_recs)
        assert "FOR COO" in coo, "COO summary header wrong"
        results.add_pass("COO summary generation")
        
        cto = gen.generate_cto_summary(sample_metrics, sample_recs)
        assert "FOR CTO" in cto, "CTO summary header wrong"
        results.add_pass("CTO summary generation")
        
        cmo = gen.generate_cmo_summary(sample_metrics, sample_recs)
        assert "FOR CMO" in cmo, "CMO summary header wrong"
        results.add_pass("CMO summary generation")
    except Exception as e:
        results.add_fail("Role-based summary generation", str(e))
    
    # Test 4: Summary bundle
    try:
        bundle = generate_all_summaries(
            title="Test MBR",
            key_metrics=sample_metrics,
            findings=["Finding 1"],
            recommendations=sample_recs,
        )
        assert bundle.short, "Short summary missing"
        assert bundle.full, "Full summary missing"
        assert bundle.cfo, "CFO summary missing"
        results.add_pass("Summary bundle generation")
    except Exception as e:
        results.add_fail("Summary bundle generation", str(e))
    
    print(f"\n{results.summary()}")
    return results


def test_validators():
    """Test validation"""
    print("\n" + "="*60)
    print("TEST: Validators")
    print("="*60)
    results = TestResults()
    
    validator = MBRValidator()
    
    sample_metrics = {
        "Revenue": {
            "current_value": 14.2,
            "target_value": 13.8,
            "delta_vs_target": "+2.9%",
        }
    }
    
    sample_recs = [
        {
            "recommendation": "Accelerate expansion",
            "owner": "Marketing Team",
            "timeline": "1 week",
            "success_criteria": "Growth +10%",
        }
    ]
    
    # Test 1: Complete validation
    try:
        result = validator.validate(
            metrics=sample_metrics,
            recommendations=sample_recs,
            narrative="Revenue exceeded target",
        )
        assert result is not None, "Validation returned None"
        results.add_pass("Complete validation")
    except Exception as e:
        results.add_fail("Complete validation", str(e))
    
    # Test 2: Data quality checks
    try:
        issues = DataQualityValidator.validate_completeness(sample_metrics)
        results.add_pass("Data completeness check")
    except Exception as e:
        results.add_fail("Data completeness check", str(e))
    
    # Test 3: Calculation validation
    try:
        issues = CalculationValidator.validate_deltas(sample_metrics)
        results.add_pass("Delta calculation validation")
    except Exception as e:
        results.add_fail("Delta calculation validation", str(e))
    
    # Test 4: Validation report
    try:
        result = validator.validate(
            metrics=sample_metrics,
            recommendations=sample_recs,
        )
        report = result.report()
        assert "Validation Report" in report or "VALIDATION" in report, "Report format wrong"
        results.add_pass("Validation report generation")
    except Exception as e:
        results.add_fail("Validation report generation", str(e))
    
    print(f"\n{results.summary()}")
    return results


def test_template_library():
    """Test template generation"""
    print("\n" + "="*60)
    print("TEST: Template Library")
    print("="*60)
    results = TestResults()
    
    # Test 1: Jira tickets
    try:
        ticket = JiraTicketTemplate.investigation_ticket(
            metric_name="Revenue",
            issue_description="Declining trend",
            root_cause_hypothesis="Market shift",
            owner_team="Finance",
        )
        assert ticket["issue_type"] == "Task", "Jira task type wrong"
        assert ticket["assignee"] == "Finance", "Assignee wrong"
        results.add_pass("Investigation ticket generation")
    except Exception as e:
        results.add_fail("Investigation ticket generation", str(e))
    
    try:
        ticket = JiraTicketTemplate.expansion_ticket(
            metric_name="Revenue",
            opportunity="E-commerce growth",
            current_performance="Strong momentum",
            owner_team="Marketing",
        )
        assert ticket["issue_type"] == "Epic", "Jira epic type wrong"
        results.add_pass("Expansion ticket generation")
    except Exception as e:
        results.add_fail("Expansion ticket generation", str(e))
    
    # Test 2: Surveys
    try:
        survey = SurveyTemplate.post_mbr_survey()
        assert "questions" in survey, "Survey questions missing"
        assert len(survey["questions"]) >= 5, "Survey too short"
        results.add_pass("Post-MBR survey generation")
    except Exception as e:
        results.add_fail("Post-MBR survey generation", str(e))
    
    # Test 3: Emails
    try:
        email = EmailTemplate.mbr_publication_email(
            mbr_month="March 2026",
            top_metrics=["Revenue up"],
            top_recommendations=["Expand"],
            mbr_url="http://example.com",
        )
        assert "subject" in email, "Email subject missing"
        assert "body" in email, "Email body missing"
        results.add_pass("Email template generation")
    except Exception as e:
        results.add_fail("Email template generation", str(e))
    
    # Test 4: Teams messages
    try:
        message = TeamsMessageTemplate.mbr_publication_message(
            mbr_month="March 2026",
            top_metric="Revenue up 2.9%",
            top_recommendation="Accelerate",
            mbr_url="http://example.com",
        )
        assert "attachments" in message, "Teams message format wrong"
        results.add_pass("Teams message generation")
    except Exception as e:
        results.add_fail("Teams message generation", str(e))
    
    print(f"\n{results.summary()}")
    return results


def test_performance_tracker():
    """Test performance tracking"""
    print("\n" + "="*60)
    print("TEST: Performance Tracker")
    print("="*60)
    results = TestResults()
    
    tracker = PerformanceTracker()
    
    # Test 1: Report creation
    try:
        report = tracker.create_report("March 2026")
        assert report.mbr_month == "March 2026", "Month mismatch"
        results.add_pass("Performance report creation")
    except Exception as e:
        results.add_fail("Performance report creation", str(e))
    
    # Test 2: Metric performance
    try:
        perf = MetricPerformance(
            metric_name="Revenue",
            forecast_value=13.8,
            actual_value=14.2,
            recommendations_count=3,
            recommendations_adopted=2,
        )
        perf.calculate_forecast_accuracy()
        perf.calculate_adoption_rate()
        
        assert perf.forecast_accuracy > 0.9, "Forecast accuracy low"
        assert perf.adoption_rate > 0.6, "Adoption rate low"
        results.add_pass("Metric performance calculation")
    except Exception as e:
        results.add_fail("Metric performance calculation", str(e))
    
    # Test 3: Report scoring
    try:
        report = tracker.create_report("March 2026")
        score = report.calculate_overall_score()
        assert 0 <= score <= 10, "Overall score out of range"
        results.add_pass("Report score calculation")
    except Exception as e:
        results.add_fail("Report score calculation", str(e))
    
    # Test 4: Report grading
    try:
        report = tracker.create_report("March 2026")
        grade = report.grade()
        assert grade in ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "Below C"], "Invalid grade"
        results.add_pass("Report grading")
    except Exception as e:
        results.add_fail("Report grading", str(e))
    
    print(f"\n{results.summary()}")
    return results


def test_phase1_orchestrator():
    """Test complete orchestration"""
    print("\n" + "="*60)
    print("TEST: Phase 1 Orchestrator")
    print("="*60)
    results = TestResults()
    
    orchestrator = Phase1Orchestrator()
    
    sample_metrics = {
        "Revenue": {
            "current_value": 14.2,
            "target_value": 13.8,
            "prior_value": 12.6,
            "ly_value": 13.0,
        },
        "CAC": {
            "current_value": 42,
            "target_value": 45,
            "prior_value": 48,
        },
        "Conversion": {
            "current_value": 2.1,
            "target_value": 2.3,
            "prior_value": 2.2,
        },
    }
    
    # Test 1: Complete orchestration
    try:
        result = orchestrator.run(
            mbr_month="March 2026",
            metrics_data=sample_metrics,
            optional_narrative="Strong month overall",
        )
        
        assert result.mbr_month == "March 2026", "Month mismatch"
        assert len(result.metric_insights) > 0, "No insights generated"
        assert len(result.all_recommendations) > 0, "No recommendations generated"
        results.add_pass("Complete orchestration")
    except Exception as e:
        results.add_fail("Complete orchestration", str(e))
    
    # Test 2: Summary generation
    try:
        result = orchestrator.run(
            mbr_month="March 2026",
            metrics_data=sample_metrics,
        )
        
        assert "short" in result.summaries, "Short summary missing"
        assert "full" in result.summaries, "Full summary missing"
        assert "cfo" in result.summaries, "CFO summary missing"
        results.add_pass("Summary generation in orchestrator")
    except Exception as e:
        results.add_fail("Summary generation in orchestrator", str(e))
    
    # Test 3: Template generation
    try:
        result = orchestrator.run(
            mbr_month="March 2026",
            metrics_data=sample_metrics,
        )
        
        assert len(result.jira_tickets) > 0, "No Jira tickets generated"
        assert len(result.survey_templates) > 0, "No surveys generated"
        assert len(result.email_templates) > 0, "No emails generated"
        results.add_pass("Template generation in orchestrator")
    except Exception as e:
        results.add_fail("Template generation in orchestrator", str(e))
    
    # Test 4: Performance reporting
    try:
        result = orchestrator.run(
            mbr_month="March 2026",
            metrics_data=sample_metrics,
        )
        
        assert result.performance_report is not None, "No performance report"
        assert len(result.performance_report.metric_performance) > 0, "No metric performance"
        results.add_pass("Performance reporting in orchestrator")
    except Exception as e:
        results.add_fail("Performance reporting in orchestrator", str(e))
    
    print(f"\n{results.summary()}")
    return results


def run_all_tests():
    """Run all tests"""
    print("\n" + "#"*70)
    print("# PHASE 1 COMPREHENSIVE TEST SUITE")
    print("#"*70)
    
    all_results = TestResults()
    
    # Run all test suites
    test_suites = [
        test_enhanced_insight_engine(),
        test_summary_generators(),
        test_validators(),
        test_template_library(),
        test_performance_tracker(),
        test_phase1_orchestrator(),
    ]
    
    # Aggregate results
    for suite in test_suites:
        all_results.passed += suite.passed
        all_results.failed += suite.failed
        all_results.errors.extend(suite.errors)
    
    # Final report
    print("\n" + "#"*70)
    print("# FINAL RESULTS")
    print("#"*70)
    print(f"\n{all_results.summary()}")
    
    if all_results.failed > 0:
        print("\n❌ Failures:")
        for error in all_results.errors:
            print(f"  • {error}")
    else:
        print("\n✅ ALL TESTS PASSED!")
    
    print("\n" + "#"*70)
    
    return all_results.failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)