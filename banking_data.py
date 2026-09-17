"""
Mock Banking Data for Demonstration Purposes.

WARNING: This is dummy data. This application does not connect to any
real banking backend or store real customer credentials.
"""

MOCK_CUSTOMER_DATA = {
    "customer_id": "CUST-987654321",
    "name": "Demo User",
    "accounts": [
        {
            "account_id": "XXXX1234",
            "type": "Savings",
            "balance": "₹75,000",
            "status": "Active"
        },
        {
            "account_id": "XXXX5678",
            "type": "Current",
            "balance": "₹1,20,000",
            "status": "Active"
        }
    ],
    "cards": [
        {
            "card_id": "XXXX-XXXX-XXXX-4321",
            "type": "Debit Card",
            "status": "Active"
        }
    ],
    "recent_transactions": [
        {"date": "2023-10-25", "amount": "-₹2,000", "description": "ATM Withdrawal"},
        {"date": "2023-10-24", "amount": "+₹15,000", "description": "Salary Credit"}
    ]
}

def get_customer_summary() -> str:
    """Returns a string representation of the mock customer data."""
    summary = f"Customer Name: {MOCK_CUSTOMER_DATA['name']}\n"
    for acc in MOCK_CUSTOMER_DATA["accounts"]:
        summary += f"- {acc['type']} Account ({acc['account_id']}): Balance {acc['balance']} [{acc['status']}]\n"
    for card in MOCK_CUSTOMER_DATA["cards"]:
        summary += f"- {card['type']} ({card['card_id']}): Status [{card['status']}]\n"
    return summary
