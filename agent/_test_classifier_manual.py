import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure root directory is in sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

# Load .env file
load_dotenv(dotenv_path=root_dir / ".env")

from agent.classifier import classify_email


def run_manual_test():
    print("=== Testing classify_email() ===")

    # Sample 1: Obvious Task Request
    task_email = {
        "sender": "sarah.connor@cyberdyne-tech.com",
        "subject": "Urgent: Review Q3 Security Audit and Sign Off by Friday",
        "date": "2026-08-22 10:30 AM",
        "body": (
            "Hi Team,\n\n"
            "Please review the attached Q3 security audit report and complete the sign-off "
            "by Friday 5 PM. We need the vulnerability remediation items addressed before our "
            "board meeting on Monday.\n\n"
            "Thanks,\nSarah"
        ),
    }

    print("\n--- Test 1: Actionable Task Email ---")
    print(f"Subject: {task_email['subject']}")
    res1 = classify_email(**task_email)
    print(f"Result: is_actionable={res1.is_actionable}, confidence={res1.confidence}")
    print(f"Raw Output: {res1.model_dump_json(indent=2)}")

    # Sample 2: Obvious Newsletter / Notification
    newsletter_email = {
        "sender": "digest@techweekly.com",
        "subject": "Tech Weekly #412: The Rise of AI Agents in 2026",
        "date": "2026-08-22 08:00 AM",
        "body": (
            "Welcome to this week's edition of Tech Weekly!\n\n"
            "In this issue, we cover the latest breakthroughs in autonomous coding agents, "
            "open source LLM benchmarks, and upcoming tech conferences.\n\n"
            "Click here to read full articles online. "
            "Unsubscribe here if you no longer wish to receive these emails."
        ),
    }

    print("\n--- Test 2: Non-Actionable Newsletter ---")
    print(f"Subject: {newsletter_email['subject']}")
    res2 = classify_email(**newsletter_email)
    print(f"Result: is_actionable={res2.is_actionable}, confidence={res2.confidence}")
    print(f"Raw Output: {res2.model_dump_json(indent=2)}")

    print("\n=== Test Finished Successfully ===")


if __name__ == "__main__":
    run_manual_test()
