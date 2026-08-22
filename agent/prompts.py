"""Prompt templates for email classification and task extraction."""

CLASSIFICATION_PROMPT = """You are an intelligent email triage assistant for InboxPilot.
Your task is to analyze an incoming email and determine whether it requires direct human action or follow-up.

### Input Email:
- Sender: {sender}
- Subject: {subject}
- Date/Time: {date}
- Content:
{body}

### Classification Rules:
1. Actionable (`is_actionable = True`):
   - Direct requests for action, deliverables, task completion, or review.
   - Meeting requests, scheduling, or invitations requiring RSVP/coordination.
   - Questions requiring a response or decision.
   - Escalations, support requests, or operational issues assigned to a person.

2. Non-Actionable (`is_actionable = False`):
   - Newsletters, marketing emails, product updates, and promotional material.
   - Automated system alerts, notifications (e.g., GitHub, Jira, CI/CD, social media).
   - Receipts, invoices, order confirmations, and transaction summaries without pending action.
   - Informational "FYI" or status updates that do not ask for any response or work.
   - Spam or irrelevant automated broadcasts.

### Output Requirements:
- `is_actionable`: Boolean (true/false) indicating if the email warrants action.
- `confidence`: Float between 0.0 and 1.0 reflecting your certainty in this classification. High confidence (0.85-1.0) for clear-cut cases; lower confidence (0.5-0.8) for ambiguous or mixed emails.
"""

EXTRACTION_PROMPT = """You are an intelligent task extraction assistant for InboxPilot.
Your task is to analyze an actionable email and extract structured task details for task trackers and notification systems.

### Input Email:
- Sender: {sender}
- Subject: {subject}
- Date/Time: {date}
- Content:
{body}

### Extraction Guidelines:
1. `task_title` (str):
   - Create a clear, concise, and imperative action item (e.g., "Review Q3 financial report", "Fix OAuth redirect bug").
   - Summarize the primary request rather than copying raw sentences.

2. `deadline` (Optional[str]):
   - Extract the specific due date, time, or relative deadline if mentioned (e.g., "2026-08-25", "by Friday 5 PM EST", "End of Day").
   - If no deadline is stated or implied, set this to null / None.

3. `priority` (Literal['low', 'medium', 'high']):
   - 'high': Urgent tasks, critical bugs, immediate deadlines (< 24-48 hours), leadership requests, or severe blockers.
   - 'medium': Standard business requests with normal deadlines, regular review tasks, or non-urgent client questions.
   - 'low': Nice-to-have items, low-urgency background tasks, or flexible long-term assignments.

4. `sender_context` (str):
   - Provide a concise summary of who the sender is (name, company/team, role if discernible) and relevant context/relationship regarding why they are reaching out.
"""
