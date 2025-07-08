


recipient = "dassubho202004@gmail.com"


subject = "Appointment Cancelled"
body = f"Your appointment with has been cancelled."

message = MIMEMultipart()
message["From"] = SENDER_EMAIL
message["To"] = recipient
message["Subject"] = subject
message.attach(MIMEText(body, "plain"))

try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(message)
    print("Email Send")
except Exception as e:
    print("Error occurred")