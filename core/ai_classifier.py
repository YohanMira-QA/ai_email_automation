def classify_email(content):

    if not isinstance(content, str):
        return "Unknown"

    content = content.lower()

    # Lead keywords
    lead_keywords = ["information", "services", "pricing", "quote", "interested"]

    # Support keywords
    support_keywords = ["support", "help", "issue", "problem", "error"]

    # Invoice keywords
    invoice_keywords = ["invoice", "billing", "payment", "receipt"]

    if any(word in content for word in lead_keywords):
        return "Lead"
    elif any(word in content for word in support_keywords):
        return "Support"
    elif any(word in content for word in invoice_keywords):
        return "Invoice"
    else:
        return "Spam"