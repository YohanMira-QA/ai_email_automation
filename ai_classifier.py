"""from openai import OpenAI
from config import OPENAI_API_KEY, MODEL

# Crear cliente usando la API key
client = OpenAI(api_key=OPENAI_API_KEY)
"""
def classify_email(content):
    prompt = f"""
    Clasifica el siguiente email en una de estas categorías:
    - Lead
    - Support
    - Invoice
    - Spam

    Email:
    {content}
    """
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()
"""
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