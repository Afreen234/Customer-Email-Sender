from flask import Flask, request, jsonify, render_template
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import time
from threading import Thread
from dotenv import load_dotenv

# Load environment variables (for security)
load_dotenv()

app = Flask(__name__)

# Set the upload folder and allowed file extensions
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = {'csv'}

# Email tracking variables
email_stats = {
    'sent': 0,
    'pending': 0,
    'failed': 0
}
email_details = []  # Stores individual email details

# Ensure that the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'status': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'No selected file'}), 400

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    return jsonify({'status': 'File uploaded successfully', 'filename': file.filename})

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.get_json()
    
    recipient = data.get('recipient')
    subject = data.get('subject')
    prompt = data.get('prompt')
    send_time = data.get('sendTime')

    if not recipient or not subject or not prompt:
        return jsonify({'status': 'Missing required fields'}), 400
    
    email_entry = {
        'recipient': recipient,
        'subject': subject,
        'status': 'pending',
        'delivery_status': 'pending',
        'opened': 'No'
    }
    email_details.append(email_entry)  # Add to email details for tracking
    email_stats['pending'] += 1

    # If a send time is provided, calculate the delay
    if send_time:
        send_time = datetime.strptime(send_time, '%Y-%m-%dT%H:%M')
        delay = (send_time - datetime.now()).total_seconds()
        if delay > 0:
            time.sleep(delay)

    # Create a thread to send the email to avoid blocking
    thread = Thread(target=send_email_in_background, args=(recipient, subject, prompt, email_entry))
    thread.start()

    return jsonify({'status': 'Email sending in background'})

def send_email_in_background(recipient, subject, prompt, email_entry):
    try:
        # Get the sender's email and password from environment variables
        sender_email = os.getenv('SENDER_EMAIL')  # Set in .env file
        sender_password = os.getenv('SENDER_PASSWORD')  # Set in .env file
        
        # Create the email message
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = recipient
        message['Subject'] = subject

        # Add the body of the email
        body = MIMEText(prompt, 'plain')
        message.attach(body)

        # Connect to the Gmail SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Start TLS encryption
            server.login(sender_email, sender_password)  # Log in
            text = message.as_string()  # Convert message to string
            server.sendmail(sender_email, recipient, text)  # Send the email

        # Update email tracking
        email_entry['status'] = 'sent'
        email_entry['delivery_status'] = 'delivered'
        email_stats['sent'] += 1
        email_stats['pending'] -= 1

    except Exception as e:
        email_entry['status'] = 'failed'
        email_entry['delivery_status'] = 'failed'
        email_stats['failed'] += 1
        email_stats['pending'] -= 1
        print(f"Error sending email: {str(e)}")

@app.route('/email-stats')
def email_stats_dashboard():
    return jsonify({
        'stats': email_stats,
        'details': email_details
    })

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
