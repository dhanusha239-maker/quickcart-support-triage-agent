# src/tools.py

TOOL_LOG = []

# -----------------------------
# Mock Data
# -----------------------------

ORDERS = {
    "QC-1008": {
        "order_id": "QC-1008",
        "total": 89.99,
        "status": "delivered",
        "fraud_review": "passed"
    },
    "QC-1007": {
        "order_id": "QC-1007",
        "total": 149.50,
        "status": "shipped",
        "fraud_review": "not_started"
    }
}

POLICIES = {
    "refund": "Refunds are allowed within 30 days of purchase if item is unused.",
    "shipping": "Standard shipping takes 5-7 business days.",
    "account": "Account issues require identity verification before changes.",
    "delivery": "Delivery delays may occur due to carrier issues or weather."
}

# -----------------------------
# TOOL 1: lookup_order
# -----------------------------
def lookup_order(order_id: str) -> dict:
    result = ORDERS.get(order_id, {"error": f"Order {order_id} was not found"})

    TOOL_LOG.append({
        "tool": "lookup_order",
        "arguments": {"order_id": order_id},
        "result": result
    })

    return result


# -----------------------------
# TOOL 2: lookup_policy
# -----------------------------
def lookup_policy(topic: str) -> dict:
    # STRICT VALIDATION (required by assignment)
    allowed_topics = {"refund", "shipping", "account", "delivery"}

    if topic not in allowed_topics:
        result = {"error": f"Invalid topic '{topic}'. Must be one of {list(allowed_topics)}"}
    else:
        result = {
            "topic": topic,
            "policy": POLICIES.get(topic)
        }

    TOOL_LOG.append({
        "tool": "lookup_policy",
        "arguments": {"topic": topic},
        "result": result
    })

    return result


# -----------------------------
# TOOL 3: create_support_case
# -----------------------------
def create_support_case(
    ticket_id: str,
    customer_id: str,
    category: str,
    urgency: str,
    summary: str
) -> dict:

    # required field safety check
    if not all([ticket_id, customer_id, category, urgency, summary]):
        return {"error": "Missing required fields for support case"}

    result = {
        "case_id": f"CASE-{ticket_id}",
        "status": "created",
        "ticket_id": ticket_id,
        "customer_id": customer_id,
        "category": category,
        "urgency": urgency,
        "summary": summary
    }

    TOOL_LOG.append({
        "tool": "create_support_case",
        "arguments": {
            "ticket_id": ticket_id,
            "customer_id": customer_id,
            "category": category,
            "urgency": urgency,
            "summary": summary
        },
        "result": result
    })

    return result


# -----------------------------
# TOOL 4: approve_refund
# -----------------------------
def approve_refund(order_id: str, amount: float, reason: str) -> dict:
    order = ORDERS.get(order_id)

    if order is None:
        result = {"approved": False, "error": f"Order {order_id} was not found"}

    elif order.get("fraud_review") == "not_started":
        result = {
            "approved": False,
            "error": "Fraud-related refunds require manual review"
        }

    elif amount > float(order["total"]):
        result = {
            "approved": False,
            "error": "Refund amount exceeds order total"
        }

    else:
        result = {
            "approved": True,
            "order_id": order_id,
            "amount": amount,
            "reason": reason
        }

    TOOL_LOG.append({
        "tool": "approve_refund",
        "arguments": {
            "order_id": order_id,
            "amount": amount,
            "reason": reason
        },
        "result": result
    })

    return result


# -----------------------------
# TOOL 5 (OPTIONAL): lock_account
# -----------------------------
def lock_account(customer_id: str, reason: str) -> dict:
    result = {
        "locked": True,
        "customer_id": customer_id,
        "reason": reason
    }

    TOOL_LOG.append({
        "tool": "lock_account",
        "arguments": {
            "customer_id": customer_id,
            "reason": reason
        },
        "result": result
    })

    return result