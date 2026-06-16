from src.extractor import extract_ticket

TEST_TICKETS = [
    {
        "ticket_id": "T006",
        "customer_id": "C018",
        "text": "Order QC-1012 was marked delivered yesterday but nothing is at my apartment mailroom. The carrier photo is not my building.",
    },
    {
        "ticket_id": "T007",
        "customer_id": "C014",
        "text": "I cancelled QC-1009 within ten minutes but I still got a shipping notice. Do not send it. I want my money back.",
    },
    {
        "ticket_id": "T008",
        "customer_id": "C031",
        "text": "The app keeps saying payment failed, but my card was charged 29.99. I do not have an order number.",
    },
    {
        "ticket_id": "T009",
        "customer_id": "C099",
        "text": "Someone changed my email and placed QC-1016. Lock the account and tell me what happened.",
    },
]

EXPECTED_ANALYSIS = {
    "T006": {"order_id": "QC-1012", "category": "delivery", "min_urgency": "medium"},
    "T007": {"order_id": "QC-1009", "category": "refund", "min_urgency": "medium"},
    "T008": {"order_id": None, "category": "billing", "min_urgency": "high"},
    "T009": {"order_id": "QC-1016", "category": "fraud_risk", "min_urgency": "critical"},
}

def evaluate():
    results = {}

    print("\n================ PART 2 EVALUATION ================\n")

    for ticket in TEST_TICKETS:
        out = extract_ticket(ticket)

        print(f"\n📌 Ticket: {ticket['ticket_id']}")
        print(out)

        results[ticket["ticket_id"]] = out.model_dump()

    # -----------------------------
    # METRICS
    # -----------------------------
    correct_category = 0
    correct_order_id = 0
    correct_urgency = 0
    total = len(TEST_TICKETS)

    urgency_rank = {"low": 0, "medium": 1, "high": 2, "critical": 3}

    for t in TEST_TICKETS:
        tid = t["ticket_id"]
        pred = results[tid]
        exp = EXPECTED_ANALYSIS[tid]

        # category check
        if pred["category"] == exp["category"]:
            correct_category += 1

        # order_id check
        if pred.get("order_id") == exp["order_id"]:
            correct_order_id += 1

        # urgency threshold check
        if urgency_rank[pred["urgency"]] >= urgency_rank[exp["min_urgency"]]:
            correct_urgency += 1

    print("\n================ FINAL SCORES ================\n")
    print(f"Category Accuracy: {correct_category}/{total}")
    print(f"Order ID Accuracy: {correct_order_id}/{total}")
    print(f"Min Urgency Met: {correct_urgency}/{total}")

    print("\nPASS CRITERIA:")
    print("- ≥3/4 category correct")
    print("- ≥3/4 order_id correct")
    print("- ≥3/4 urgency threshold met")


if __name__ == "__main__":
    evaluate()