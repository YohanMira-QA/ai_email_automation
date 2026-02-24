from email_loader import load_emails
from ai_classifier import classify_email
from auto_responder import generate_response
from exporter import export_results

def main():
    df = load_emails("sample_emails.csv")
    
    categories = []
    responses = []

    for content in df["email_body"]:
        category = classify_email(content)
        response = generate_response(category)
        
        categories.append(category)
        responses.append(response)

    df["category"] = categories
    df["auto_response"] = responses

    export_results(df)
    print("Proceso completado.")

if __name__ == "__main__":
    main()