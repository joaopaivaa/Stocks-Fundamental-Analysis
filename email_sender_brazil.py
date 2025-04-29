from datetime import datetime

today = datetime.now()

if today.day == 10:
    
    import time

    start = time.time()

    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders
    import os

    import pdf_creator_brazil

    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email = "joaopaiva.raspberrypi@gmail.com"
    password = os.getenv("RASPBERRY_PASSWORD")

    recipient = "joaovmarcotti@hotmail.com"
    assunto = "Brazil Stocks List"

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = recipient
    msg['Subject'] = assunto

    with open('top10_brazil_stocks.pdf', "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())

    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename={'top10_brazil_stocks.pdf'}",
    )
    msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, recipient, msg.as_string())
        print("E-mail sent!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.quit()

    end = time.time()

    print(f"Execution time: {end - start:.2f} seconds")

else:
    print("Today is not the 10th of the month. No email will be sent.")