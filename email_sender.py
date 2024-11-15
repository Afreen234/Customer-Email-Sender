import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, jsonify

app = Flask(_name_)

@app.route('/send-email/', methods=['POST'])
def send_email():
    recipient_email = request.form['recipient']
    subject = request.form['subject']
    prompt = request.form['prompt']
    send_time = request.form['sendTime']

    sender_email = "affu26@gmail.com"  # Your Gmail address
    sender_password = "yxfg ihen ofxa fjrx"  # Or your Gmail password if using less secure apps

    try:
        # Set up the SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Login to Gmail using your email and password
        server.login(sender_email, sender_password)

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(prompt, 'plain'))

        # Send the email
        server.sendmail(sender_email, recipient_email, msg.as_string())

        # Close the server connection
        server.quit()

        return jsonify({'status': 'Email sent successfully!'}), 200

    except Exception as e:
        print(f"Error sending email: {e}")
        return jsonify({'status': 'Error sending email', 'error': str(e)}), 500

if _name_ == '_main_':
    app.run(debug=True, port=8000)