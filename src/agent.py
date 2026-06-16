import json

from src.llm_client import client, MODEL
from src.tools import (
    lookup_order,
    lookup_policy,
    create_support_case,
    approve_refund,
    lock_account,
    TOOL_LOG
)

from src.tool_schemas import TOOLS


SYSTEM_PROMPT = """
You are QuickCart's support triage agent.

CRITICAL RULES (must follow exactly):

1. ALWAYS check for fraud or account takeover FIRST.
   - If fraud is suspected → NEVER approve refund.
   - Instead immediately call lock_account + create_support_case.

2. Use lookup_order whenever an order_id exists.

3. Use lookup_policy before any refund decision.

4. Refunds are ONLY allowed if:
   - fraud_review = passed
   - no fraud suspicion

5. Every ticket MUST create a support case LAST.

6. Final answer must be short and calm.

7. FRAUD_RISK CATEGORY RULE:
Fraud_risk MUST be used when:
- Unauthorized orders are placed
- Email or password is changed without user intent
- Account takeover is suspected
- User explicitly asks to lock account due to suspicious activity involving orders

If any fraud indicator exists → category MUST be "fraud_risk" (NOT "account")

If category = fraud_risk → urgency MUST be "critical" (never high or medium)

If fraud_risk is detected:
- urgency = critical (mandatory override)

TOOL ORDER PRIORITY:
fraud → order lookup → policy → action → case creation
"""


def execute_tool(name: str, arguments: dict, tool_log: list):
    """Map tool name → Python function + log results"""

    if name == "lookup_order":
        result = lookup_order(**arguments)

    elif name == "lookup_policy":
        result = lookup_policy(**arguments)

    elif name == "create_support_case":
        result = create_support_case(**arguments)

    elif name == "approve_refund":
        result = approve_refund(**arguments)

    elif name == "lock_account":
        result = lock_account(**arguments)

    else:
        result = {"error": f"Unknown tool: {name}"}

    tool_log.append({
        "tool": name,
        "arguments": arguments,
        "result": result
    })

    return result


def run_support_agent(ticket: dict, max_steps: int = 6) -> dict:

    tool_log = []

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"""
Ticket Information:
{json.dumps(ticket, indent=2)}
"""}
    ]

    step_count = 0

    while step_count < max_steps:

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.2,
        )

        msg = response.choices[0].message

        # 1. TOOL CALL CASE
        if getattr(msg, "tool_calls", None):

            messages.append(msg)

            for tool_call in msg.tool_calls:

                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                print(f"🔧 Tool: {tool_name} | Args: {args}")

                result = execute_tool(tool_name, args, tool_log)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

            step_count += 1
            continue

        # 2. FINAL ANSWER CASE
        final_answer = msg.content or ""

        return {
            "ticket_id": ticket["ticket_id"],
            "final_answer": final_answer,
            "tool_log": tool_log,
            "step_count": step_count
        }

    return {
        "ticket_id": ticket["ticket_id"],
        "final_answer": "Max steps reached without final answer.",
        "tool_log": tool_log,
        "step_count": step_count
    }