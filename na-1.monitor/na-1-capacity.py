"""
Check NA-1 Storage Used Level
if > 80%, send an email to misbackup
"""
import paramiko
import smtplib
import email.utils
from email.mime.text import MIMEText
import time

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def one_command(cmd):
    ssh.connect('na-1.masterad.lincotech.com.tw', username='root', password='admin123')
    stdin, stdout, stderr = ssh.exec_command(cmd)
    return stdin, stdout, stderr

# log file
#
t_now = time.strftime("%Y%m%d-%H%M%S")
log_file_name = "/volume1/Backup/na-1.monitor/log/na-1.monitoring.log-"+t_now
log = open(log_file_name, "w")
#
# issue one command and get the result
stdin, stdout, stderr = one_command("df")

rsp = stdout.readlines()

for r in rsp:
    log.write(str(r))

b=[x for x in rsp \
  if ('FileServer' in x) and \
     ('snapshot' not in x)]

c=b[0]
i=c.index('%')  # locate %

# used = int(c[i-2:i])  # check the number

msg = MIMEText(' '.join(rsp))   # attachment 
msg['To'] = email.utils.formataddr(('MIS', 'misbackup@lincotech.com.tw'))
msg['From'] = email.utils.formataddr(('Fax', 'fax@lincotech.com.tw'))

pre = '[NA-1]'
p = c[i-2:i]        # % value of FileServer   
if int(p) >= 80:    # Warnning  
    msg['Subject'] = pre + '  !!! Warnning FileServer >= ' + p + '%' + ' !!!' 
else:
    msg['Subject'] = pre + '  !!! INFO FileServer Used = ' + p + '%' + ' !!!'  

s = smtplib.SMTP('mail.lincotech.com.tw',25) 	# create an SMTP object
s.ehlo()
s.sendmail('fax@lincotech.com.tw', ['misbackup@lincotech.com.tw'], msg.as_string())
s.close()

log.close()
