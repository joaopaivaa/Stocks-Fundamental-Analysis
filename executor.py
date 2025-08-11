import subprocess
import time

subprocess.run(['python', 'brazil_info_collect.py'])
print('Brazil info collected successfully.')
time.sleep(5)

subprocess.run(['python', 'brazil_query.py'])
print('Brazil query executed successfully.')
time.sleep(5)

subprocess.run(['python', 'brazil_analysis.py'])
print('Brazil analysis executed successfully.')
time.sleep(5)

subprocess.run(['python', 'brazil_pdf_creator.py'])
print('Brazil PDF created successfully.')
time.sleep(5)

subprocess.run(['python', 'brazil_email_sender.py'])
print('Brazil email sent successfully.')
time.sleep(5)