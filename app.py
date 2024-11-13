from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure the Flask-Mail extension
app.config['MAIL_SERVER'] = os.getenv('EMAIL_HOST')
app.config['MAIL_PORT'] = int(os.getenv('EMAIL_PORT'))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_SENDER')

# Initialize Mail object
mail = Mail(app)

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        # Retrieve JSON data from the request
        data = request.get_json()
        message_body = data.get('message')
        recipient_email = data.get('email')

        if not message_body or not recipient_email:
            return jsonify({'error': 'Missing message or email'}), 400

        # Compose the email message
        msg = Message(subject="Message from Flask App",
                      recipients=[recipient_email],
                      body=message_body)

        # Send the email
        mail.send(msg)

        return jsonify({'success': True, 'message': 'Email sent successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)