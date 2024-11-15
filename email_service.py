import sendgrid
from sendgrid.helpers.mail import Mail
from database import log_email_status

SENDGRID_API_KEY = "your_sendgrid_api_key"

def send_email(recipient: str, subject: str, content: str):
    try:
        sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)
        from_email = "affu26@example.com"
        to_email = recipient
        mail = Mail(from_email, subject, to_email, content)
        response = sg.send(mail)
        log_email_status(recipient, subject, "sent")
        return response
    except Exception as e:
        log_email_status(recipient, subject, "failed")
        raise e

def handle_sendgrid_webhook(request):
    # Process the event data from SendGrid webhook
    event_data = request.json()  # Assuming the request is a FastAPI request object
    for event in event_data:
        # Process each event like delivered, opened, bounced, etc.
        pass