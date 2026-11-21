from http.server import BaseHTTPRequestHandler
import json
import os
import smtplib
from email.message import EmailMessage

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body.decode('utf-8'))

        msg = EmailMessage()
        msg['Subject'] = f"Portfolio Lead: {data.get('subject', 'New Inquiry')}"
        msg['From'] = "Engineer Ouko <jw5141576@gmail.com>"
        msg['To'] = "jw5141576@gmail.com"
        msg['Reply-To'] = data.get('email', '')
        msg.set_content(
            f"Name: {data.get('name')}\n"
            f"Email: {data.get('email')}\n\n"
            f"Message:\n{data.get('message')}"
        )

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(os.environ['GMAIL_USER'], os.environ['GMAIL_APP_PASSWORD'])
                smtp.send_message(msg)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode())
