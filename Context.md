# InboxPilot — Project Context

## Project

InboxPilot is an AI-powered email-to-action automation system being built
for the Razorpay AI Builder internship.

The goal is to automatically read incoming emails, determine whether they
contain actionable work, extract the relevant task information, and route
the result to a task tracker and Slack.

---

## Core Architecture

Gmail
  ↓
n8n Gmail Trigger
  ↓
LangChain Agent
  ↓
Classification
  ↓
Structured Extraction
  ↓
n8n
  ├── Actionable → Notion/Google Sheets → Slack
  └── Informational → Daily Digest

---

## Responsibilities

### n8n

n8n is responsible for:

- Gmail trigger
- Workflow orchestration
- Routing and branching
- Calling the LangChain/FastAPI service
- Notion or Google Sheets integration
- Slack notifications
- Duplicate/processed-email checks where appropriate

### LangChain / FastAPI

The Python service is responsible for:

- Email classification
- Actionability detection
- Structured task extraction
- Deadline extraction
- Priority extraction
- Sender/context extraction
- Returning validated structured JSON
- Handling LLM-related errors

---

## Tech Stack

### Agent / Backend

- Python
- LangChain
- FastAPI
- LLM API
- Pydantic
- python-dotenv

### Automation

- n8n Cloud

### Integrations

- Gmail
- Notion or Google Sheets
- Slack

### Development

- Antigravity IDE
- Git
- GitHub

### Cloud / Existing Knowledge

The developer has experience with:

- LangChain
- n8n
- FastAPI
- AWS
- Python
- Git/GitHub

---

## Architecture Principles

1. Keep n8n responsible for orchestration and integrations.
2. Keep Python/LangChain responsible for AI logic.
3. Return structured JSON from the AI service.
4. Keep the Python code modular and easy to understand.
5. Prefer simple implementations over unnecessary abstractions.
6. Every important AI decision should be explainable.
7. Validate LLM outputs before they are sent to downstream systems.
8. Never hardcode API keys or credentials.
9. Use environment variables for local secrets.
10. Use n8n's credential system for external service credentials whenever appropriate.

---

## Scope Restrictions

Do NOT introduce:

- Docker
- Kubernetes
- Microservice infrastructure
- Redis
- Kafka
- Celery
- Complex databases
- Unnecessary cloud infrastructure
- Complex frontend frameworks

The project should remain simple enough to build, demo, debug, and
explain during an internship interview.

Do not replace n8n with another orchestration framework.

Do not replace LangChain with another agent framework unless explicitly
requested.

Do not introduce technologies merely because they are popular.

---

## Development Rules

Before making major architectural changes:

1. Explain why the change is necessary.
2. Check whether the existing architecture already solves the problem.
3. Prefer the simplest solution.
4. Do not modify unrelated files.
5. Do not generate large amounts of code without explaining what is being built.
6. Keep functions and modules focused on one responsibility.
7. Add error handling around external APIs and LLM calls.
8. Never expose secrets in source code or logs.

---

## Expected Project Structure

The project will eventually follow approximately this structure:

InboxPilot/
│
├── agent/
│   ├── main.py
│   ├── classifier.py
│   ├── extractor.py
│   ├── models.py
│   └── prompts.py
│
├── n8n/
│   └── inboxpilot-workflow.json
│
├── .env
├── .gitignore
├── requirements.txt
├── CONTEXT.md
└── README.md

This structure may be changed if there is a clear technical reason.

---

## Important Agent Instruction

Do not start implementing the project just because this context file exists.

Wait for explicit instructions from the developer before creating
application code or changing the architecture.

When implementation begins, build the project incrementally and explain
each major step before proceeding.