import time

start = time.time()

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from analysis_us import df_evaluated as df_evaluated_us

smtp_server = "smtp.gmail.com"
smtp_port = 587
email = "joaopaiva.raspberrypi@gmail.com"
password = os.getenv("RASPBERRY_PASSWORD")

destinatario = "joaovmarcotti@hotmail.com"
assunto = "US Stocks List"
mensagem = f"US Stocks List\n{df_evaluated_us[['ticker', 'name', 'Portfolio %', 'Portfolio Value']].to_string(index=False)}"

msg = MIMEMultipart()
msg['From'] = email
msg['To'] = destinatario
msg['Subject'] = assunto
msg.attach(MIMEText(mensagem, 'plain'))

try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(email, password)
    server.sendmail(email, destinatario, msg.as_string())
    print("E-mail sent!")
except Exception as e:
    print(f"Error: {e}")
finally:
    server.quit()

end = time.time()

print(f"Execution time: {end - start:.2f} seconds")