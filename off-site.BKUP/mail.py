"""
Mail to misbackup
Usgage: mail.py log_file str_subject
"""
import smtplib, sys
import email.utils
from email.mime.text import MIMEText

log_file_name = sys.argv[1]
str_subject = sys.argv[2]
#
#
log = open(log_file_name, "r")
msg = MIMEText(log.read())
msg['To'] = email.utils.formataddr(('MIS', 'misbackup@lincotech.com.tw'))
msg['From'] = email.utils.formataddr(('Fax', 'fax@lincotech.com.tw'))
    
msg['Subject'] = str_subject

s = smtplib.SMTP('mail.lincotech.com.tw',25) 	# create an SMTP object
s.ehlo()
s.sendmail('fax@lincotech.com.tw', ['misbackup@lincotech.com.tw'], msg.as_string())
s.close()
log.close()
