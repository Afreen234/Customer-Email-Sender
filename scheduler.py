from apscheduler.schedulers.background import BackgroundScheduler
from email_service import send_email

scheduler = BackgroundScheduler()

# Example of scheduling an email to be sent at a specific date and time
def schedule_email(recipient: str, subject: str, content: str, run_date: str):
    scheduler.add_job(send_email, 'date', run_date=run_date, args=[recipient, subject, content])
    scheduler.start()