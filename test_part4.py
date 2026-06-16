from src.agent import run_support_agent

# -----------------------------
# Test Ticket 1 (Billing issue)
# -----------------------------
ticket_1 = {
    "ticket_id": "T003",
    "customer_id": "C014",
    "order_id": "QC-1008",
    "message": "I was charged twice for my order QC-1008. Please fix this.",
    "priority_hint": "high"
}

# -----------------------------
# Test Ticket 2 (Account/Fraud risk)
# -----------------------------
ticket_2 = {
    "ticket_id": "T004",
    "customer_id": "C022",
    "order_id": "QC-1007",
    "message": "Someone may have accessed my account and placed an order I did not make.",
    "priority_hint": "critical"
}


def run_test(ticket, label):
    print("\n" + "=" * 60)
    print(f"RUNNING TEST: {label}")
    print("=" * 60)

    result = run_support_agent(ticket)

    print("\n📌 Ticket ID:", result["ticket_id"])

    print("\n🧠 Final Answer:\n")
    print(result["final_answer"])

    print("\n🔧 Step Count:", result["step_count"])

    print("\n🧾 TOOL TRACE:")
    for i, log in enumerate(result["tool_log"], 1):
        print(f"\nStep {i}:")
        print("Tool:", log["tool"])
        print("Args:", log["arguments"])
        print("Result:", log["result"])


if __name__ == "__main__":
    run_test(ticket_1, "Billing - Duplicate Charge")
    run_test(ticket_2, "Fraud / Account Risk")