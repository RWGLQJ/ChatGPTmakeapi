import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
from flask import Flask, request, jsonify
#http://localhost:5000/send_email?receiver_email=1939418698@qq.com&sender_name=%E6%B5%8B%E8%AF%95%E5%90%8D%E7%A7%B0&subject=%E6%B5%8B%E8%AF%95%E6%A0%87%E9%A2%98&message=%E6%B5%8B%E8%AF%95%E5%86%85%E5%AE%B9

app = Flask(__name__)

SMTP_SERVER = 'smtp.qq.com'
SMTP_PORT = 587
SENDER_EMAIL = 'yhtmailapi@qq.com'
#SENDER_PASSWORD = 'msahqpilzybodeed'
SENDER_PASSWORD = 'psbhsxoyulcxdehg'
# 设置日志记录
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s - %(message)s')

def create_message(receiver_email, sender_name, subject, message):
    msg = MIMEMultipart()
    msg['From'] = formataddr((str(Header(sender_name, 'utf-8')), SENDER_EMAIL))
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    return msg

@app.route('/send_email', methods=['GET'])
def send_email():
    try:
        receiver_email = request.args.get('receiver_email')
        sender_name = request.args.get('sender_name')
        subject = request.args.get('subject')
        message = request.args.get('message')

        msg = create_message(receiver_email, sender_name, subject, message)

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        # 记录日志
        log_message = f"Email sent. IP: {request.remote_addr}, " \
                      f"Receiver: {receiver_email}, " \
                      f"Sender Name: {sender_name}, " \
                      f"Subject: {subject}, " \
                      f"Message: {message}"
        logging.info(log_message)

        # 构建正确的JSON响应
        response = {
            'status': 'success',
            'data': {
                'receiver_email': receiver_email,
                'sender_name': sender_name,
                'subject': subject,
                'message_content': message
            },
            'message': 'Email sent successfully'
        }
        return jsonify(response)
    except Exception as e:
        # 记录错误日志
        error_message = f"Error sending email. IP: {request.remote_addr}, " \
                        f"Error: {str(e)}"
        logging.error(error_message)
        
        # 返回错误消息的JSON响应
        response = {
            'status': 'error',
            'message': str(e)
        }
        return jsonify(response)

if __name__ == '__main__':
    app.run()
