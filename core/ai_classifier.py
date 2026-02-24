
def classify_email(content):
    content = content.lower()

    if "factura" in content:
        return "Invoice"
    elif "soporte" in content:
        return "Support"
    elif "información" in content or "cotización" in content:
        return "Lead"
    else:
        return "Spam"