
from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USERNAME = ''
SMTP_PASSWORD = ''
EMAIL_FROM = ''

app = Flask(__name__)

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    data = request.json
    email = data.get('email')

    # Generate forgot password link
    forgot_password_link = 'http://127.0.0.1:8081/change-password/'  # Replace with your reset password page URL

    # Send email with forgot password link
    send_forgot_password_email(email, forgot_password_link)

    return jsonify({'message': 'Forgot password link sent successfully'})

def send_forgot_password_email(email, link):
    subject = 'Forgot Password'
    body = f'Click the following link to reset your password: {link}'

    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(EMAIL_FROM, email, msg.as_string())
            print("Forgot password email sent successfully")
    except Exception as e:
        print("Error sending email:", e)



@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.json
    email = data.get('email')
    new_password = data.get('new_password')

    # Reset the password (you should update it in your database)
    # Here, we're just printing it for demonstration purposes
    print(f"Password for {email} has been reset to: {new_password}")

    # Send email notification
    send_password_reset_notification(email)

    return jsonify({'message': 'Password reset successfully'})
  
  
def send_password_reset_notification(email):
    subject = 'Password Reset Successful'
    body = 'Your password has been successfully reset.'

    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(EMAIL_FROM, email, msg.as_string())
            print("Password reset notification email sent successfully")
    except Exception as e:
        print("Error sending email:", e)

if __name__=='__main__':
    app.run(debug=True,port=8860)
