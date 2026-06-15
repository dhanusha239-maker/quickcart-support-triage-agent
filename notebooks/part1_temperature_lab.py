import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.llm_client import chat

ticket = {
    "ticket_id": "T003",
    "customer_id": "C014",
    "text": "Why did you charge me twice for QC-1008? My bank shows two 89.99 charges."
}
prompt_1 = "Classify this customer support ticket and suggest next action."

prompt_2 = """
You are a careful support triage analyst.
Classify the ticket, identify order ID, urgency, and next action.
Be concise.
"""

prompt_3 = """
You are a support agent writing for an upset customer.
Explain what you will do next.
Do NOT promise refunds unless confirmed.
"""
def run_test(prompt, temp):
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": ticket["text"]}
    ]
    
    return chat(messages, temperature=temp)
temps = [0, 0.7, 1.3]

for prompt in [prompt_1, prompt_2, prompt_3]:
    print("\n====================")
    print("PROMPT TEST")
    
    for t in temps:
        print("\nTEMP:", t)
        print(run_test(prompt, t))