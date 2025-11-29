# src/auto_reply.py
from typing import Dict, Optional

# Define professional auto-reply templates based on expected intents
INTENT_TEMPLATES = {
    'sales_inquiry': "Hello {name},\n\nThank you for your interest! Our sales team will reach out within 2 hours to discuss pricing and options.\n\nBest regards,\nSales Team",
    'support_issue': "Hi {name},\n\nWe apologize for the issue. Your request has been escalated to our technical support team ({issue_id}). We will update you shortly.\n\nThank you,\nSupport Desk",
    'billing_issue': "Dear {name},\n\nPlease provide your invoice or order number, and our accounts team will resolve the billing query immediately.\n\nSincerely,\nAccounts Team",
    'partnership': "Hello {name},\n\nThanks for reaching out about a partnership! We will review your proposal and contact you this week.\n\nKind regards,\nPartnerships",
    'cancellation': "Hi {name},\n\nYour cancellation request has been received and processed. We're sorry to see you go.\n\nThanks,\nTeam",
    'other': "Hi {name},\n\nThank you for your message. A member of our team will review your query and respond within 24 hours.\n\nRegards,\nTeam"
}

def generate_reply(intent: str, name: Optional[str] = None, issue_id: Optional[str] = None) -> str:
    """
    Selects a template based on the predicted intent and formats the reply.
    """
    name = name or "Customer"  # Default name if none is provided
    
    # Select template, falling back to 'other' if intent is unrecognized
    template = INTENT_TEMPLATES.get(intent, INTENT_TEMPLATES['other'])
    
    # Context variables for template formatting
    context = {"name": name, "issue_id": issue_id or "N/A"}
    
    return template.format(**context)