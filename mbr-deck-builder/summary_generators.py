"""Summary Generators - Multiple Narrative Styles for MBR

Generates:
- Short 2-minute summary
- Full 30-minute summary
- Role-based summaries (CFO, COO, CTO, CMO)
- Audience-specific narratives

Status: Production Ready
Author: Code Puppy 🐶
Date: March 16, 2026
"""

from dataclasses import dataclass
from typing import List, Dict, Optional

# Import canonical enums from central source
from enums import (
    NarrativeStyle,
    AudienceRole,
)


@dataclass
class Summary:
    """A generated summary"""
    title: str
    audience: str
    length: str  # "short", "medium", "full"
    executive_summary: str  # 1-2 paragraphs
    key_metrics: List[str]  # Top 3-5 metrics
    key_findings: List[str]  # Main insights
    recommendations: List[str]  # Top actions
    warnings: List[str]  # Things to watch
    style: NarrativeStyle


class SummaryGenerator:
    """Generates narratives in multiple styles"""
    
    @staticmethod
    def generate_short_summary(
        metrics: Dict[str, Dict],
        top_recommendations: List[str],
    ) -> str:
        """Generate 2-minute summary (~400 words)"""
        
        lines = []
        lines.append("📊 MBR QUICK SUMMARY (2 Minutes)\n")
        lines.append("═" * 50)
        
        # Top 3 metrics
        lines.append("\n📈 KEY METRICS:")
        for metric_name, metric_data in list(metrics.items())[:3]:
            delta = metric_data.get("delta_vs_target", "N/A")
            lines.append(f"  • {metric_name}: {delta}")
        
        # Top 3 recommendations
        lines.append("\n🎯 TOP ACTIONS:")
        for i, rec in enumerate(top_recommendations[:3], 1):
            lines.append(f"  {i}. {rec}")
        
        lines.append("\n" + "═" * 50)
        lines.append("Read full MBR for details →")
        
        return "\n".join(lines)
    
    @staticmethod
    def generate_full_summary(
        title: str,
        key_metrics: Dict[str, Dict],
        findings: List[str],
        recommendations: List[Dict],
        anomalies: List[Dict],
    ) -> str:
        """Generate full 30-minute summary"""
        
        lines = []
        lines.append(f"\n📊 {title}\n")
        lines.append("═" * 70)
        
        # Executive Summary
        lines.append("\n📋 EXECUTIVE SUMMARY")
        lines.append("-" * 70)
        
        if findings:
            lines.append(f"\nTop insight: {findings[0]}")
            for finding in findings[1:3]:
                lines.append(f"Also: {finding}")
        
        # Metrics
        lines.append("\n\n📈 PERFORMANCE METRICS")
        lines.append("-" * 70)
        
        for metric_name, metric_data in key_metrics.items():
            current = metric_data.get("current", "N/A")
            target = metric_data.get("target", "N/A")
            delta = metric_data.get("delta_vs_target", "N/A")
            trend = metric_data.get("trend", {})
            
            lines.append(f"\n{metric_name}:")
            lines.append(f"  Current: {current} | Target: {target} | vs Target: {delta}")
            if trend:
                lines.append(f"  Trend: {trend.get('direction', 'N/A')} ({trend.get('momentum', 'N/A')})")
        
        # Anomalies
        if anomalies:
            lines.append("\n\n⚠️  ANOMALIES DETECTED")
            lines.append("-" * 70)
            for anomaly in anomalies:
                severity = anomaly.get("severity", "Medium")
                desc = anomaly.get("description", "Unknown")
                lines.append(f"\n[{severity}] {desc}")
        
        # Recommendations
        lines.append("\n\n🎯 RECOMMENDATIONS")
        lines.append("-" * 70)
        
        for i, rec in enumerate(recommendations, 1):
            owner = rec.get("owner", "TBD")
            action = rec.get("recommendation", "Unknown")
            timeline = rec.get("timeline", "TBD")
            lines.append(f"\n{i}. {action}")
            lines.append(f"   Owner: {owner}")
            lines.append(f"   Timeline: {timeline}")
        
        lines.append("\n" + "═" * 70)
        return "\n".join(lines)
    
    @staticmethod
    def generate_cfo_summary(
        metrics: Dict[str, Dict],
        recommendations: List[Dict],
    ) -> str:
        """Generate summary for CFO (revenue, margin, profitability focused)"""
        
        lines = []
        lines.append("\n💰 MBR FOR CFO")
        lines.append("═" * 50)
        
        # Financial metrics
        lines.append("\n💵 FINANCIAL PERFORMANCE:")
        for metric_name in ["Revenue", "Margin", "Profitability", "CAC"]:
            if metric_name in metrics:
                data = metrics[metric_name]
                delta = data.get("delta_vs_target", "N/A")
                lines.append(f"  ✓ {metric_name}: {delta}")
        
        # Financial implications
        lines.append("\n📊 FINANCIAL IMPLICATIONS:")
        lines.append("  • Revenue trending: [positive/negative/flat]")
        lines.append("  • Profitability: [improving/stable/declining]")
        lines.append("  • Cash flow impact: [positive/neutral/negative]")
        
        # Financial recommendations
        lines.append("\n💳 FINANCIAL ACTIONS:")
        for rec in recommendations:
            if any(x in rec.get("owner", "").lower() for x in ["finance", "revenue"]):
                lines.append(f"  → {rec.get('recommendation', 'Action')}")
        
        lines.append("\n" + "═" * 50)
        return "\n".join(lines)
    
    @staticmethod
    def generate_coo_summary(
        metrics: Dict[str, Dict],
        recommendations: List[Dict],
    ) -> str:
        """Generate summary for COO (operations, efficiency focused)"""
        
        lines = []
        lines.append("\n⚙️ MBR FOR COO")
        lines.append("═" * 50)
        
        # Operational metrics
        lines.append("\n🏭 OPERATIONAL PERFORMANCE:")
        for metric_name in ["Uptime", "Efficiency", "Cost", "Conversion"]:
            if metric_name in metrics:
                data = metrics[metric_name]
                delta = data.get("delta_vs_target", "N/A")
                lines.append(f"  • {metric_name}: {delta}")
        
        # Operational risks
        lines.append("\n⚠️  OPERATIONAL RISKS:")
        lines.append("  • In-store performance: [declining/stable/improving]")
        lines.append("  • System reliability: [excellent/good/needs attention]")
        lines.append("  • Efficiency gaps: [none/minor/significant]")
        
        # Operational actions
        lines.append("\n✅ OPERATIONAL ACTIONS:")
        for rec in recommendations:
            if any(x in rec.get("owner", "").lower() for x in ["operations", "in-store", "efficiency"]):
                lines.append(f"  → {rec.get('recommendation', 'Action')}")
        
        lines.append("\n" + "═" * 50)
        return "\n".join(lines)
    
    @staticmethod
    def generate_cto_summary(
        metrics: Dict[str, Dict],
        recommendations: List[Dict],
    ) -> str:
        """Generate summary for CTO (technical, performance focused)"""
        
        lines = []
        lines.append("\n🔧 MBR FOR CTO")
        lines.append("═" * 50)
        
        # Technical metrics
        lines.append("\n💻 TECHNICAL PERFORMANCE:")
        for metric_name in ["Uptime", "Performance", "Error Rate", "Security"]:
            if metric_name in metrics:
                data = metrics[metric_name]
                delta = data.get("delta_vs_target", "N/A")
                lines.append(f"  ✓ {metric_name}: {delta}")
        
        # Technical insights
        lines.append("\n🔍 TECHNICAL INSIGHTS:")
        lines.append("  • Infrastructure: [healthy/monitored/alerts]")
        lines.append("  • Performance: [optimal/acceptable/degraded]")
        lines.append("  • Security posture: [strong/compliant/needs review]")
        
        # Technical actions
        lines.append("\n🛠️ TECHNICAL ACTIONS:")
        for rec in recommendations:
            if any(x in rec.get("owner", "").lower() for x in ["engineering", "technical", "platform"]):
                lines.append(f"  → {rec.get('recommendation', 'Action')}")
        
        lines.append("\n" + "═" * 50)
        return "\n".join(lines)
    
    @staticmethod
    def generate_cmo_summary(
        metrics: Dict[str, Dict],
        recommendations: List[Dict],
    ) -> str:
        """Generate summary for CMO (marketing, growth focused)"""
        
        lines = []
        lines.append("\n📢 MBR FOR CMO")
        lines.append("═" * 50)
        
        # Marketing metrics
        lines.append("\n📊 MARKETING PERFORMANCE:")
        for metric_name in ["CAC", "Conversion", "NPS", "Segment Performance"]:
            if metric_name in metrics:
                data = metrics[metric_name]
                delta = data.get("delta_vs_target", "N/A")
                lines.append(f"  • {metric_name}: {delta}")
        
        # Customer insights
        lines.append("\n👥 CUSTOMER INSIGHTS:")
        lines.append("  • Customer acquisition: [efficient/expensive/optimal]")
        lines.append("  • Channel performance: [strong/diverse/concentrated]")
        lines.append("  • Brand sentiment: [improving/stable/declining]")
        
        # Marketing actions
        lines.append("\n🎯 MARKETING ACTIONS:")
        for rec in recommendations:
            if any(x in rec.get("owner", "").lower() for x in ["marketing", "customer", "growth"]):
                lines.append(f"  → {rec.get('recommendation', 'Action')}")
        
        lines.append("\n" + "═" * 50)
        return "\n".join(lines)


class NarrativeSelector:
    """Selects best narrative style for audience"""
    
    @staticmethod
    def select_style(audience: AudienceRole) -> NarrativeStyle:
        """Select narrative style based on audience role"""
        
        style_map = {
            AudienceRole.CFO: NarrativeStyle.EXECUTIVE,
            AudienceRole.COO: NarrativeStyle.EXECUTIVE,
            AudienceRole.CTO: NarrativeStyle.TECHNICAL,
            AudienceRole.CMO: NarrativeStyle.EXECUTIVE,
            AudienceRole.CEO: NarrativeStyle.BOARD,
            AudienceRole.BOARD: NarrativeStyle.BOARD,
        }
        
        return style_map.get(audience, NarrativeStyle.EXECUTIVE)
    
    @staticmethod
    def generate_for_role(
        role: AudienceRole,
        metrics: Dict[str, Dict],
        recommendations: List[Dict],
    ) -> str:
        """Generate summary for specific role"""
        
        generator = SummaryGenerator()
        
        if role == AudienceRole.CFO:
            return generator.generate_cfo_summary(metrics, recommendations)
        elif role == AudienceRole.COO:
            return generator.generate_coo_summary(metrics, recommendations)
        elif role == AudienceRole.CTO:
            return generator.generate_cto_summary(metrics, recommendations)
        elif role == AudienceRole.CMO:
            return generator.generate_cmo_summary(metrics, recommendations)
        else:
            return generator.generate_full_summary(
                title="MBR",
                key_metrics=metrics,
                findings=[],
                recommendations=recommendations,
                anomalies=[]
            )


class SummaryBundle:
    """Complete set of summaries for all audiences"""
    
    def __init__(
        self,
        short_summary: str,
        full_summary: str,
        cfo_summary: str,
        coo_summary: str,
        cto_summary: str,
        cmo_summary: str,
    ):
        self.short = short_summary
        self.full = full_summary
        self.cfo = cfo_summary
        self.coo = coo_summary
        self.cto = cto_summary
        self.cmo = cmo_summary
        self.all_summaries = {
            "short": short_summary,
            "full": full_summary,
            "cfo": cfo_summary,
            "coo": coo_summary,
            "cto": cto_summary,
            "cmo": cmo_summary,
        }
    
    def get(self, summary_type: str) -> str:
        """Get summary by type"""
        return self.all_summaries.get(summary_type, self.short)
    
    def get_for_role(self, role: AudienceRole) -> str:
        """Get summary for specific role"""
        role_map = {
            AudienceRole.CFO: "cfo",
            AudienceRole.COO: "coo",
            AudienceRole.CTO: "cto",
            AudienceRole.CMO: "cmo",
            AudienceRole.CEO: "full",
            AudienceRole.BOARD: "full",
        }
        summary_key = role_map.get(role, "short")
        return self.all_summaries[summary_key]


def generate_all_summaries(
    title: str,
    key_metrics: Dict[str, Dict],
    findings: List[str],
    recommendations: List[Dict],
    anomalies: List[Dict] = None,
) -> SummaryBundle:
    """Generate complete summary bundle"""
    
    if anomalies is None:
        anomalies = []
    
    gen = SummaryGenerator()
    
    short = gen.generate_short_summary(key_metrics, [r.get("recommendation", "") for r in recommendations])
    full = gen.generate_full_summary(title, key_metrics, findings, recommendations, anomalies)
    cfo = gen.generate_cfo_summary(key_metrics, recommendations)
    coo = gen.generate_coo_summary(key_metrics, recommendations)
    cto = gen.generate_cto_summary(key_metrics, recommendations)
    cmo = gen.generate_cmo_summary(key_metrics, recommendations)
    
    return SummaryBundle(
        short_summary=short,
        full_summary=full,
        cfo_summary=cfo,
        coo_summary=coo,
        cto_summary=cto,
        cmo_summary=cmo,
    )


# Example usage
if __name__ == "__main__":
    sample_metrics = {
        "Revenue": {"current": 14.2, "target": 13.8, "delta_vs_target": "+2.9%"},
        "CAC": {"current": 42, "target": 45, "delta_vs_target": "-6.7%"},
        "Conversion": {"current": 2.1, "target": 2.3, "delta_vs_target": "-8.7%"},
    }
    
    sample_recs = [
        {"recommendation": "Accelerate e-commerce", "owner": "Marketing", "timeline": "1 week"},
        {"recommendation": "Investigate conversion dip", "owner": "Product", "timeline": "1 week"},
    ]
    
    gen = SummaryGenerator()
    
    print("\n" + "="*60)
    print("SHORT SUMMARY")
    print("="*60)
    print(gen.generate_short_summary(sample_metrics, [r["recommendation"] for r in sample_recs]))
    
    print("\n" + "="*60)
    print("CFO SUMMARY")
    print("="*60)
    print(gen.generate_cfo_summary(sample_metrics, sample_recs))
    
    print("\n" + "="*60)
    print("COO SUMMARY")
    print("="*60)
    print(gen.generate_coo_summary(sample_metrics, sample_recs))