from flask import Flask, request, jsonify
import smtplib
import random

app = Flask(__name__)

# This dictionary will store email-OTP pairs
otp_storage = {}

# Email configuration
EMAIL_ADDRESS = ''
EMAIL_PASSWORD = ''


def send_email(receiver_email, otp):
    subject = 'Your One-Time Password (OTP)'
    body = f'Your OTP is: {otp}'

    message = f'Subject: {subject}\n\n{body}'

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, receiver_email, message)


@app.route('/send_otp', methods=['POST'])
def send_otp():
    data = request.get_json()
    email = data.get('email')

    if email:
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # Generate a 6-digit OTP
        otp_storage[email] = otp  # Store the OTP in the dictionary
        send_email(email, otp)  # Send the OTP to the provided email
        return jsonify({'message': 'OTP sent successfully'}), 200
    else:
        return jsonify({'error': 'Email is required'}), 400


@app.route('/validate_otp', methods=['POST'])
def validate_otp():
    data = request.get_json()
    email = data.get('email')
    otp_entered = data.get('otp')

    if email and otp_entered:
        stored_otp = otp_storage.get(email)

        if stored_otp == otp_entered:
            # del otp_storage [email]  # Remove the OTP from storage after successful validation
            return jsonify({'message': 'OTP is valid'}), 200
        else:
            return jsonify({'error': 'Invalid OTP'}), 400
    else:
        return jsonify({'error': 'Email and OTP are required'}), 400


if __name__ == '__main__':
    app.run(debug=True,port=6059)
