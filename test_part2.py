from src.extractor import extract_ticket

ticket = {
    "ticket_id": "T003",
    "customer_id": "C014",
    "text": "Why did you charge me twice for QC-1008? My bank shows two 89.99 charges."
}

result = extract_ticket(ticket)

print(result.model_dump())