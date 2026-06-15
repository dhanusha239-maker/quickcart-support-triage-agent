import json
from src.llm_client import client, MODEL
from src.schemas import TicketAnalysis

def normalize(data: dict):
    # fix casing issues
    if "category" in data and data["category"]:
        data["category"] = data["category"].lower()

    if "urgency" in data and data["urgency"]:
        data["urgency"] = data["urgency"].lower()

    if "sentiment" in data and data["sentiment"]:
        data["sentiment"] = data["sentiment"].lower()

    return data

def extract_ticket(ticket: dict):
    system_prompt = """
You are a strict JSON generator.

You MUST return ONLY valid JSON.

You must copy and fill this structure EXACTLY:

{
  "ticket_id": null,
  "customer_id": null,
  "category": null,
  "urgency": null,
  "sentiment": null,
  "order_id": null,
  "requested_action": null,
  "confidence": null,
  "rationale": null
}

RULES:
1. Do NOT remove any keys.
2. Do NOT add extra keys.
3. Replace null with extracted values when available.
4. Use ONLY allowed labels:

CATEGORY:
- delivery, refund, billing, technical, account, fraud_risk, other

URGENCY:
- low, medium, high, critical

SENTIMENT:
- calm, confused, frustrated, angry

5. Output ONLY JSON.
"""


    response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": str(ticket)}
    ],
    temperature=0.2,

    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "ticket_analysis",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "ticket_id": {"type": "string"},
                    "customer_id": {"type": "string"},
                    "category": {
                        "type": "string",
                        "enum": [
                            "delivery",
                            "refund",
                            "billing",
                            "technical",
                            "account",
                            "fraud_risk",
                            "other"
                        ]
                    },
                    "urgency": {
                        "type": "string",
                        "enum": ["low", "medium", "high", "critical"]
                    },
                    "sentiment": {
                        "type": "string",
                        "enum": ["calm", "confused", "frustrated", "angry"]
                    },
                    "order_id": {
                        "type": ["string", "null"]
                    },
                    "requested_action": {"type": "string"},
                    "confidence": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1
                    },
                    "rationale": {"type": "string"}
                },
                "required": [
                    "ticket_id",
                    "customer_id",
                    "category",
                    "urgency",
                    "sentiment",
                    "order_id",
                    "requested_action",
                    "confidence",
                    "rationale"
                ],
                "additionalProperties": False
            }
        }
    }
)

    data = response.choices[0].message.content

    parsed = json.loads(data)

    parsed = normalize(parsed)

    return TicketAnalysis.model_validate(parsed)