import smtplib
from email.message import EmailMessage

EMAIL_SENDER = "chirudeep80@gmail.com"
EMAIL_PASSWORD = "glucnhcemivgfelw"
EMAIL_RECEIVER = "medisettiaditya57@gmail.com"

try:
    msg = EmailMessage()
    msg['Subject'] = "✅ Test Email Successful"
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg.set_content("If you received this, your email setup is working perfectly!")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)

    print("✅ EMAIL SENT SUCCESSFULLY!")

except Exception as e:
    print("❌ EMAIL FAILED:")
    print(e)
