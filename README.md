QuickCart Support Triage Agent:
An LLM-powered support automation system that classifies customer tickets, extracts structured information, and executes internal tools such as order lookup, policy checks, refunds, and account security actions.
Project Overview


This system processes customer support tickets using:
Structured LLM extraction (Pydantic + JSON schema)
Tool calling (OpenAI function calling)
Rule-based agent orchestration
Safety guardrails for fraud detection
It is divided into:
Part 2: Structured Ticket Extraction
Part 3: Internal Tools
Part 4: Support Agent Loop (Tool-using LLM agent)
Evaluation Scripts

Project Structure:
quickcart-support-triage-agent/
│
├── src/
│   ├── llm_client.py
│   ├── tools.py
│   ├── tool_schemas.py
│   ├── agent.py
│
├── test_part2.py
├── test_part2_eval.py
├── test_part4.py
│
├── README.md
├── REPORT.md
└── requirements.txt

Setup Instructions:
1. Create Virtual Environment: 
python -m venv .venv
.\.venv\Scripts\activate
2. Install Dependencies
pip install -r requirements.txt


Part2:
Structured Extraction:
Key Rules:
No hallucinated order IDs
Fraud-related tickets must be high/critical urgency
Output must pass schema validation

Part3:
Internal Tools:
1. lookup_order(order_id)
Fetch order details.
2. lookup_policy(topic)
Returns policy for:
refund
shipping
account
delivery
3. create_support_case(...)
Creates support ticket in backend system.
4. approve_refund(...)
Validates and processes refunds with fraud checks.
5. lock_account(customer_id, reason)
Locks account for fraud/security issues.


Part 4:
 Support Agent Loop
The agent works in a loop:

Send ticket to LLM
Model selects tools
Execute tools in Python
Append results to conversation
Repeat until final answer
System Rules:
Fraud must be checked FIRST
Fraud → lock_account + create_support_case
Refund only if fraud_review = passed
Every ticket must create a support case
Final response must be short and clear

Run Part 2 evaluation::python test_part2_eval.py
Run Part 4 agent tests:python test_part4.py

Evaluation Metrics:
Part 2 Evaluation:
Category Accuracy
Order ID Accuracy
Minimum Urgency Satisfaction
Part 4 Evaluation:
Tool execution correctness
Fraud handling safety
Support case creation consistency

Final results Summary:
| Metric                | Result |
| --------------------- | ------ |
| Category Accuracy     | 4/4    |
| Order ID Accuracy     | 4/4    |
| Urgency Compliance    | 3/4    |
| Support Case Creation | 100%   |
| Fraud Safety          | Passed |


Safety Guardrails:
Fraud-risk tickets are escalated immediately
Refunds blocked for suspicious accounts
Account takeover → automatic lock

Key Learnings:
Structured outputs improve reliability
Tool calling enables real-world agent behavior
Guardrails are essential for production safety
LLMs need strict rules for fraud detection

Git command to push:
git add .
git commit -m "Final QuickCart agent submission"
git push origin main
