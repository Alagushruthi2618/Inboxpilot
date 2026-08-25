import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure root directory is in sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

# Load .env file
load_dotenv(dotenv_path=root_dir / ".env")

from agent.extractor import extract_task


def run_manual_test():
    print("=== Testing extract_task() ===")

    # Sample 1: Explicit hard deadline & high urgency
    urgent_email = {
        "sender": "alex.morgan@payment-gateway.io",
        "subject": "CRITICAL: Fix production webhook signature mismatch by 2:00 PM EST today",
        "date": "2026-08-25 09:15 AM",
        "body": (
            "Hi Team,\n\n"
            "We are seeing a high volume of failed webhooks in production due to a signature verification "
            "mismatch after the morning release. We need a hotfix deployed and an incident RCA submitted "
            "by 2:00 PM EST today. Please treat this as top priority.\n\n"
            "Best,\n"
            "Alex Morgan (Head of Core Engineering)"
        ),
    }

    print("\n--- Test 1: High Urgency & Hard Deadline ---")
    print(f"Subject: {urgent_email['subject']}")
    res1 = extract_task(**urgent_email)
    print(f"Task Title: {res1.task_title}")
    print(f"Deadline: {res1.deadline}")
    print(f"Priority: {res1.priority}")
    print(f"Sender Context: {res1.sender_context}")
    print(f"\nFull JSON Output:\n{res1.model_dump_json(indent=2)}")

    # Sample 2: Vague / relative deadline & lower urgency
    casual_email = {
        "sender": "priya.sharma@designguild.org",
        "subject": "Ideas for Q4 design system icon library refresh",
        "date": "2026-08-25 10:00 AM",
        "body": (
            "Hey everyone,\n\n"
            "Whenever you get some downtime, could you take a look at the proposed icon set updates for Q4? "
            "No rush on this at all — just drop your thoughts or feedback in the shared Figma file sometime next week.\n\n"
            "Cheers,\n"
            "Priya (Product Design Lead)"
        ),
    }

    print("\n--- Test 2: Low Urgency & Relative Deadline ---")
    print(f"Subject: {casual_email['subject']}")
    res2 = extract_task(**casual_email)
    print(f"Task Title: {res2.task_title}")
    print(f"Deadline: {res2.deadline}")
    print(f"Priority: {res2.priority}")
    print(f"Sender Context: {res2.sender_context}")
    print(f"\nFull JSON Output:\n{res2.model_dump_json(indent=2)}")

    print("\n=== Test Finished Successfully ===")


if __name__ == "__main__":
    run_manual_test()
