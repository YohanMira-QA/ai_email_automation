def generate_response(category):
    responses = {
        "Lead": "Gracias por contactarnos, pronto te enviaremos información.",
        "Support": "Tu solicitud fue recibida, nuestro equipo la revisará.",
        "Invoice": "Factura recibida, será procesada.",
        "Spam": None
    }

    return responses.get(category)