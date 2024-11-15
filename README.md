# Customer-Email-Sender
Custom Email Sender with Flask

This project is a customized email sender application built with Flask. The application allows users to log in using their email ID and password, and then send emails using their own accounts. After sending emails, the application tracks the status of sent, pending, and failed emails and displays this data on a dashboard.

Features
Login Page: Users can log in with their email and password.
Email Sending Page: Users can send emails from their own email account.
Dashboard: A dashboard to display the status of emails (Sent, Pending, Failed).
File Upload: Option to upload CSV files (if required for email recipient lists or other purposes).
Technologies Used
Python
Flask
HTML/CSS for front-end
SMTP (Gmail) for sending emails
Jinja2 for templating
Session handling
Required Packages
Flask
Flask-Session
smtplib
email
datetime
os
time
Installation
Follow these steps to get the application running on your local machine:

Step 1: Clone the repository
Clone the repository to your local machine.

bash
Copy code
git clone <repository-url>
cd <repository-folder>
Step 2: Set up the virtual environment
If you don't have a virtual environment set up yet, you can create one using the following commands:

For Linux/macOS:

bash
Copy code
python3 -m venv venv
source venv/bin/activate
For Windows:

bash
Copy code
python -m venv venv
.\venv\Scripts\activate
Step 3: Install dependencies
Install the required Python packages using pip.

bash
Copy code
pip install -r requirements.txt
requirements.txt content:

makefile
Copy code
Flask==2.1.2
Flask-Session==0.4.0
smtplib
email
If the requirements.txt does not exist, you can manually install the packages using:

bash
Copy code
pip install Flask Flask-Session smtplib
Step 4: Setup Configuration
App Secret Key:

Main App: The Flask app requires a secret key to handle sessions. You can generate one using the following code:

python
Copy code
import os
print(os.urandom(24))
Use the output of this code as your secret_key in main.py for session handling.

Email Credentials:

In app.py, use your Gmail email ID and the corresponding Gmail App Password (not your regular Gmail password, as Gmail blocks sign-ins from less secure apps). You can set up an App Password here: App Passwords.

Example:

python
Copy code
sender_email = "your-email@example.com"
sender_password = "your-app-password"
Ensure that you set these values in app.py to use the correct email credentials for sending emails.

Step 5: Running the Application
Running main.py (Login Page)
Run main.py to start the login page:

bash
Copy code
python main.py
Visit the login page at http://127.0.0.1:8000/login.

Login using your email ID and password. After successful login, you will be redirected to the app.py email sender page.

Running app.py (Email Sender Page)
Once logged in through main.py, run app.py:

Run app.py:

bash
Copy code
python app.py
The app will open at http://127.0.0.1:5000 (or the port specified).

You’ll be taken to the index.html page, where you can input the recipient, subject, and content of the email.

After sending the email, navigate to /dashboard to see the stats (sent, pending, failed).

Folder Structure
bash
Copy code
/project-folder
│
├── /templates
│   ├── login.html
│   ├── index.html
│   ├── dashboard.html
│
├── main.py          # Contains the login page and session management
├── app.py           # Email sender logic
├── requirements.txt # Required Python packages
└── /uploads         # Folder for storing uploaded files (if needed)
Detailed Functionality
Login (main.py):
The login page (login.html) asks users for their email and password.
After successful login, the user’s session is created, and they are redirected to the email sender page (app.py).
Email Sender (app.py):
Users enter the recipient, subject, and body of the email on the index.html page.
The email is sent using the Gmail SMTP server after successful authentication (using the credentials provided in app.py).
Dashboard (app.py):
The /dashboard page displays the status of sent, pending, and failed emails.
Users can view their email statistics and the status of each email they sent.
Notes
Make sure to enable Less Secure Apps in your Gmail settings if using a regular Gmail account, or use App Passwords (recommended).
The app uses Flask Sessions to track logged-in users. The session data is not persistent across different machines, so ensure you handle the login flow accordingly.
The email sending process uses the Gmail SMTP server (smtp.gmail.com), but this can be modified to use other services if needed.
Security Warning
Do not expose your Gmail credentials publicly. Always use environment variables or secure methods to store sensitive information like email IDs and passwords.
