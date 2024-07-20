from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message

app = Flask(__name__)

# Configurations for email
app.config['MAIL_SERVER'] = 'smtp.example.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'your_email@example.com'
app.config['MAIL_PASSWORD'] = 'your_password'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form['email']
    send_verification_email(email)
    return jsonify({'message': 'Subscription successful, verification email sent!'})

def send_verification_email(email):
    msg = Message('Verify your email', sender='your_email@example.com', recipients=[email])
    msg.body = 'Please verify your email by clicking the link.'
    mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True)
