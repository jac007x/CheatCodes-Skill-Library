"""Template Library - Ready-to-Use Templates for Jira, Surveys, Emails

Provides templates for:
- Jira tickets (by recommendation type)
- Feedback surveys
- Email notifications
- Teams messages
- Market context

Status: Production Ready
Author: Code Puppy 🐶
Date: March 16, 2026
"""

from typing import Dict, List
from datetime import datetime, timedelta


class JiraTicketTemplate:
    """Templates for Jira tickets"""
    
    @staticmethod
    def investigation_ticket(
        metric_name: str,
        issue_description: str,
        root_cause_hypothesis: str,
        owner_team: str,
        priority: str = "High",
        due_days: int = 7,
    ) -> Dict:
        """Template for investigation recommendation"""
        
        due_date = (datetime.now() + timedelta(days=due_days)).strftime("%Y-%m-%d")
        
        return {
            "project": "MBR",
            "issue_type": "Task",
            "summary": f"[MBR] Investigate {metric_name} {issue_description}",
            "description": f"""From MBR Analysis:

Metric: {metric_name}
Issue: {issue_description}
Hypothesis: {root_cause_hypothesis}

Needed:
1. Root cause analysis
2. Impact assessment
3. Remediation recommendation

Target Completion: {due_days} days

Success Criteria:
- Root cause identified
- Impact documented
- Next steps recommended
""",
            "assignee": owner_team,
            "priority": priority,
            "due_date": due_date,
            "labels": ["mbr-action", "investigation", f"metric-{metric_name.lower()}"],
            "components": ["MBR"],
            "custom_fields": {
                "mbr_month": datetime.now().strftime("%B %Y"),
                "metric_type": metric_name,
            }
        }
    
    @staticmethod
    def expansion_ticket(
        metric_name: str,
        opportunity: str,
        current_performance: str,
        owner_team: str,
        budget_impact: str = "TBD",
        priority: str = "High",
        due_days: int = 14,
    ) -> Dict:
        """Template for expansion recommendation"""
        
        due_date = (datetime.now() + timedelta(days=due_days)).strftime("%Y-%m-%d")
        
        return {
            "project": "MBR",
            "issue_type": "Epic",
            "summary": f"[MBR] Expand {metric_name}: {opportunity}",
            "description": f"""From MBR Analysis:

Metric: {metric_name}
Opportunity: {opportunity}
Current Performance: {current_performance}
Budget Impact: {budget_impact}

Proposal:
1. Increase resources/budget
2. Expand successful initiatives
3. Track growth vs. forecast

Success Criteria:
- Strategy approved
- Resources allocated
- Growth targets set
- Progress tracked weekly
""",
            "assignee": owner_team,
            "priority": priority,
            "due_date": due_date,
            "labels": ["mbr-action", "expansion", f"metric-{metric_name.lower()}"],
            "components": ["MBR"],
        }
    
    @staticmethod
    def recovery_ticket(
        metric_name: str,
        decline_description: str,
        owner_team: str,
        priority: str = "Critical",
        due_days: int = 14,
    ) -> Dict:
        """Template for recovery/turnaround recommendation"""
        
        due_date = (datetime.now() + timedelta(days=due_days)).strftime("%Y-%m-%d")
        
        return {
            "project": "MBR",
            "issue_type": "Epic",
            "summary": f"[MBR] Recover {metric_name}: {decline_description}",
            "description": f"""From MBR Analysis:

Metric: {metric_name}
Trend: {decline_description}
Priority: CRITICAL - Declining metric requires recovery plan

Recovery Plan Requirements:
1. Root cause analysis
2. Strategic turnaround initiatives
3. Target recovery metrics
4. Weekly progress tracking
5. Executive check-ins

Success Criteria:
- Plan developed and approved
- Initiatives deployed
- Metric stabilizes within {due_days} days
- Growth resumes within 30 days
""",
            "assignee": owner_team,
            "priority": priority,
            "due_date": due_date,
            "labels": ["mbr-action", "critical", "recovery", f"metric-{metric_name.lower()}"],
            "components": ["MBR"],
        }
    
    @staticmethod
    def monitoring_ticket(
        metric_name: str,
        item_to_monitor: str,
        owner_team: str,
        check_frequency: str = "Daily",
        priority: str = "Medium",
    ) -> Dict:
        """Template for monitoring recommendation"""
        
        return {
            "project": "MBR",
            "issue_type": "Story",
            "summary": f"[MBR] Monitor {metric_name}: {item_to_monitor}",
            "description": f"""From MBR Analysis:

Metric: {metric_name}
Monitor: {item_to_monitor}
Frequency: {check_frequency}
Duration: Ongoing (next 90 days)

Action Items:
1. Set up monitoring dashboard/alerts
2. Define alert thresholds
3. Assign monitoring owner
4. Schedule weekly reviews

Success Criteria:
- Monitoring in place
- Dashboard live
- Alerts configured
- Weekly reports sent
- Early warnings caught

{metric_name} should be monitored to catch any
adverse trends before they become critical.
""",
            "assignee": owner_team,
            "priority": priority,
            "labels": ["mbr-action", "monitoring", f"metric-{metric_name.lower()}"],
            "components": ["MBR"],
        }


class SurveyTemplate:
    """Templates for feedback surveys"""
    
    @staticmethod
    def post_mbr_survey() -> Dict:
        """Survey sent 3-5 days after MBR publication"""
        
        return {
            "title": "MBR Quality Feedback",
            "description": "Help us improve future MBRs",
            "time_limit_minutes": 5,
            "questions": [
                {
                    "question": "How useful was this MBR?",
                    "type": "scale",
                    "scale": 5,
                    "required": True,
                    "scale_labels": {
                        1: "Not useful",
                        2: "Somewhat useful",
                        3: "Useful",
                        4: "Very useful",
                        5: "Exceeded expectations"
                    }
                },
                {
                    "question": "Will you act on the recommendations?",
                    "type": "choice",
                    "options": ["Yes, already started", "Yes, will start soon", "Maybe", "No"],
                    "required": True
                },
                {
                    "question": "Which recommendation will you prioritize?",
                    "type": "text",
                    "required": False
                },
                {
                    "question": "What information was missing?",
                    "type": "text",
                    "required": False
                },
                {
                    "question": "What surprised you (good or bad)?",
                    "type": "text",
                    "required": False
                },
                {
                    "question": "Would you recommend the MBR format to other teams?",
                    "type": "choice",
                    "options": ["Yes", "No", "With improvements"],
                    "required": True
                },
                {
                    "question": "Net Promoter Score: How likely to recommend MBR? (0-10)",
                    "type": "scale",
                    "scale": 10,
                    "required": True
                }
            ]
        }
    
    @staticmethod
    def recommendation_outcome_survey() -> Dict:
        """Survey sent 30 days after MBR to track outcomes"""
        
        return {
            "title": "MBR Recommendation Outcomes",
            "description": "How did the MBR recommendations work out?",
            "time_limit_minutes": 10,
            "questions": [
                {
                    "question": "How many MBR recommendations did you act on?",
                    "type": "choice",
                    "options": ["All", "Most (75%+)", "Some (50-74%)", "Few (25-49%)", "None"],
                    "required": True
                },
                {
                    "question": "Which recommendation had the biggest impact?",
                    "type": "text",
                    "required": False
                },
                {
                    "question": "Did any recommendation NOT work as expected?",
                    "type": "text",
                    "required": False
                },
                {
                    "question": "What was the business impact? (e.g. revenue, efficiency, customer satisfaction)",
                    "type": "text",
                    "required": False
                },
                {
                    "question": "If you didn't act on some recommendations, why?",
                    "type": "text",
                    "required": False
                },
                {
                    "question": "Estimate ROI of following MBR recommendations",
                    "type": "choice",
                    "options": ["Very high (10x+)", "High (5-10x)", "Medium (2-5x)", "Low (1-2x)", "Negative"],
                    "required": False
                }
            ]
        }


class EmailTemplate:
    """Templates for email notifications"""
    
    @staticmethod
    def mbr_publication_email(
        mbr_month: str,
        top_metrics: List[str],
        top_recommendations: List[str],
        mbr_url: str,
    ) -> Dict:
        """Email sent when MBR published"""
        
        return {
            "from": "mbr-engine@company.com",
            "to_roles": ["executives", "functional_leaders"],
            "subject": f"MBR Ready: {mbr_month} - Revenue Beat Target by 2.9%",
            "body": f"""Hi team,

The {mbr_month} MBR is ready for review.

📊 KEY HIGHLIGHTS:
{chr(10).join('• ' + m for m in top_metrics[:3])}

🎯 TOP RECOMMENDATIONS:
{chr(10).join(f'{i}. {r}' for i, r in enumerate(top_recommendations[:3], 1))}

📖 VIEW FULL MBR:
{mbr_url}

💬 QUICK SURVEY (2 minutes):
[SURVEY_LINK]

📅 REVIEW MEETINGS:
• Wed 2:00 PM - Highlights & Q&A
• Fri 10:00 AM - Deep Dive: [Topic]
• Mon 9:00 AM - Strategy Alignment

💡 Questions? Ask the MBR team.

Best,
MBR Engine
""",
            "template_variables": {
                "mbr_month": mbr_month,
                "metrics_count": len(top_metrics),
                "recommendations_count": len(top_recommendations),
                "url": mbr_url
            }
        }
    
    @staticmethod
    def jira_ticket_reminder_email(
        owner_team: str,
        ticket_count: int,
        due_days: int,
    ) -> Dict:
        """Email reminder for pending Jira tickets"""
        
        return {
            "from": "mbr-engine@company.com",
            "to": owner_team,
            "subject": f"Reminder: {ticket_count} MBR Action Items Due in {due_days} Days",
            "body": f"""Hi {owner_team},

You have {ticket_count} action items from the latest MBR due in {due_days} days.

🎯 ACTION ITEMS:
• [Ticket 1: Brief description]
• [Ticket 2: Brief description]
• [Ticket 3: Brief description]
[View all tickets →]

📅 Due Date: [DATE]
✅ Success Criteria: [CRITERIA]

Please provide a status update by [DATE].

Questions? Ask the MBR team.

Best,
MBR Engine
""",
            "template_variables": {
                "owner_team": owner_team,
                "ticket_count": ticket_count,
                "due_days": due_days
            }
        }
    
    @staticmethod
    def feedback_request_email(
        mbr_month: str,
        survey_url: str,
    ) -> Dict:
        """Email requesting feedback on MBR"""
        
        return {
            "from": "mbr-engine@company.com",
            "to_roles": ["executives"],
            "subject": f"Quick Feedback: {mbr_month} MBR Quality (2 minutes)",
            "body": f"""Hi,

We'd love to hear your feedback on this month's MBR.

📋 Quick Survey (2 minutes):
{survey_url}

Questions covered:
• How useful was the MBR?
• Will you act on the recommendations?
• What was missing?
• Net Promoter Score

Your feedback helps us improve future MBRs.

Thank you!
MBR Engine
""",
            "template_variables": {
                "mbr_month": mbr_month,
                "survey_url": survey_url
            }
        }


class TeamsMessageTemplate:
    """Templates for Teams notifications"""
    
    @staticmethod
    def mbr_publication_message(
        mbr_month: str,
        top_metric: str,
        top_recommendation: str,
        mbr_url: str,
    ) -> Dict:
        """Teams adaptive card for MBR publication"""
        
        return {
            "type": "message",
            "attachments": [
                {
                    "contentType": "application/vnd.microsoft.card.adaptive",
                    "contentUrl": None,
                    "content": {
                        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                        "type": "AdaptiveCard",
                        "version": "1.4",
                        "body": [
                            {
                                "type": "TextBlock",
                                "text": f"📊 {mbr_month} MBR Published",
                                "weight": "bolder",
                                "size": "large"
                            },
                            {
                                "type": "TextBlock",
                                "text": f"✅ {top_metric}",
                                "wrap": True
                            },
                            {
                                "type": "TextBlock",
                                "text": f"🎯 {top_recommendation}",
                                "wrap": True
                            }
                        ],
                        "actions": [
                            {
                                "type": "Action.OpenUrl",
                                "title": "View Full MBR",
                                "url": mbr_url
                            },
                            {
                                "type": "Action.OpenUrl",
                                "title": "Quick Feedback",
                                "url": "[SURVEY_URL]"
                            }
                        ]
                    }
                }
            ]
        }


class MarketContextTemplate:
    """Templates for market context sections"""
    
    @staticmethod
    def market_context_section() -> str:
        """Market context section for MBR narrative"""
        
        return """🌍 MARKET CONTEXT

INDUSTRY TRENDS:
• Sector growth: +X% YoY
• Our growth: +Y% YoY
• Market penetration: Z%
• Position vs market: [Leading/Competitive/Trailing]

COMPETITIVE LANDSCAPE:
• Competitor A: [Status]
• Competitor B: [Status]
• Market consolidation: [Trend]
• New entrants: [Risk/Opportunity]

EXTERNAL EVENTS:
• Regulatory changes: [Impact]
• Economic factors: [Impact]
• Technology shifts: [Impact]
• Seasonal factors: [Impact]

IMPLICATIONS FOR OUR METRICS:
• Revenue: [Headwind/Tailwind]
• Market share: [Risk/Opportunity]
• Growth sustainability: [Assessment]
"""