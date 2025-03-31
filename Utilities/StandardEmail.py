import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def SendGmail(message="Message not passed to SendGmail function",
              subject="Subject not passed to SendGmail function",
              **Kwargs):
    try:
        # Initialize Dictionary Values
        emailFrom = Kwargs.get("emailFrom")
        emailTo = Kwargs.get("emailTo")
        smtpServer = Kwargs.get("smtpServer")
        emailPassword = Kwargs.get("emailPassword")

        # Create Email Message
        msg = MIMEMultipart()
        msg["From"] = emailFrom
        msg["To"] = emailTo
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        # Send Email
    
        server = smtplib.SMTP_SSL(smtpServer, 465) 
        server.login(emailFrom, emailPassword)
        server.send_message(msg)
        server.quit()
        return True
    
    
    #In instances where an email can not be sent, the host machine will leave the error up on the terminal
    except Exception as e:
        print(f"Error: {e}")
        input("Press enter key to continue")
        return False