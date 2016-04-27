"""
This script send email with attached log
Note:
/usr/bin/python etc-bk.py log_file_name
"""
import smtplib
import email.utils
from email.mime.text import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email import Encoders
import sys


log_file_name = sys.argv[1]
#
# mail
#


msg = MIMEMultipart()

msg['Subject'] = '  Synology NAS System /etc Back Up Done'
msg['To'] = email.utils.formataddr(('MIS', 'misbackup@lincotech.com.tw'))
msg['From'] = email.utils.formataddr(('Fax', 'fax@lincotech.com.tw'))
    
part = MIMEBase('application', "octet-stream")
part.set_payload(open(log_file_name, "rb").read())
Encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment', filename=log_file_name)

msg.attach(part)

s = smtplib.SMTP('mail.lincotech.com.tw',25) 	# create an SMTP object
s.ehlo()
s.sendmail('fax@lincotech.com.tw', ['misbackup@lincotech.com.tw'], msg.as_string())
s.close()
#log.close()
