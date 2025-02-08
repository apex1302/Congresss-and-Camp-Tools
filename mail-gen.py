import csv
import json
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Konfiguration
csv_file = 'email_list.csv'
json_file = 'error_descriptions.json'
smtp_server = 'smtp.example.com'
smtp_port = 587
smtp_username = 'your_username'
smtp_password = 'your_password'

# Lade E-Mail-Adressen aus der CSV-Datei
def load_emails(csv_file):
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        return [row[0] for row in reader]

# Lade Fehlerbeschreibungen aus der JSON-Datei
def load_error_descriptions(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)

# Generiere eine zufällige Absender-E-Mail-Adresse
def generate_random_email():
    domains = ['example.com', 'mail.com', 'test.com']
    local_part = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz1234567890', k=10))
    domain = random.choice(domains)
    return f"{local_part}@{domain}"

# Erstelle eine E-Mail-Nachricht
def create_email(sender, recipient, error_description):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = "Serviceterminanfrage für Tesla Model 3"

    body = f"""
    Sehr geehrtes Tesla-Service-Team,

    ich benötige einen Servicetermin für mein Tesla Model 3. Das Problem ist folgendes:

    {error_description}

    Bitte teilen Sie mir mögliche Termine mit.

    Mit freundlichen Grüßen,
    {sender}
    """
    msg.attach(MIMEText(body, 'plain'))
    return msg

# Sende E-Mails
def send_emails(emails, error_descriptions):
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        for email in emails:
            for _ in range(20):  # Sende 20 E-Mails pro E-Mail-Adresse
                error_description = random.choice(error_descriptions)
                sender = generate_random_email()
                msg = create_email(sender, email, error_description)
                server.sendmail(sender, email, msg.as_string())
                print(f"E-Mail an {email} von {sender} gesendet.")

# Hauptfunktion
def main():
    emails = load_emails(csv_file)
    error_descriptions = load_error_descriptions(json_file)
    send_emails(emails, error_descriptions)

if __name__ == "__main__":
    main()
