TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "lookup_order",
            "description": "Look up an order by order ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "Order ID such as QC-1008"
                    }
                },
                "required": ["order_id"],
                "additionalProperties": False
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "lookup_policy",
            "description": "Look up company policies",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "enum": [
                            "refund",
                            "shipping",
                            "account",
                            "delivery"
                        ]
                    }
                },
                "required": ["topic"],
                "additionalProperties": False
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "create_support_case",
            "description": "Create a support case for a customer",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticket_id": {"type": "string"},
                    "customer_id": {"type": "string"},
                    "category": {"type": "string"},
                    "urgency": {"type": "string"},
                    "summary": {"type": "string"}
                },
                "required": [
                    "ticket_id",
                    "customer_id",
                    "category",
                    "urgency",
                    "summary"
                ],
                "additionalProperties": False
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "approve_refund",
            "description": "Approve a refund for an order",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "string"},
                    "amount": {"type": "number"},
                    "reason": {"type": "string"}
                },
                "required": [
                    "order_id",
                    "amount",
                    "reason"
                ],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lock_account",
            "description": "Lock a customer account for suspected fraud",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string"
                    },
                    "reason": {
                        "type": "string"
                    }
                },
                "required": [
                    "customer_id",
                    "reason"
                ],
                "additionalProperties": False
            }
        }
    }
]