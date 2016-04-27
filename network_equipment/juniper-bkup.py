"""
This script backup Juniper config
Check if new files in /volume1/homes/juniper
if yes, move them to /volume/Backup/network_equipment/juniper
if no, skip
"""
import time
import smtplib
import email.utils
from email.mime.text import MIMEText
import os
import shutil 
#
#
#
log_path = "/volume1/Backup/network_equipment/log/"
t_now = time.strftime("%Y%m%d-%H%M%S")
log_file_name = log_path + "juniper-bkup.log-" + t_now
log = open(log_file_name, "w")

src = '/volume1/homes/juniper'
dst = '/volume/Backup/network_equipment/juniper'

new_f = os.listdir(src)
if new_f:
    for f in new_f:
        shutil.move(src+'/'+f, dst+'/'+f)
        log.write('New cfg File ' + f + ' moved from ' + src + ' To ' + dst +'\n')
else:
    log.write('No new cfg files found in ' + src + '\n')

log.close()
#
# mail
#
log = open(log_file_name, "r")
msg = MIMEText(log.read())
msg['To'] = email.utils.formataddr(('MIS', 'misbackup@lincotech.com.tw'))
msg['From'] = email.utils.formataddr(('Fax', 'fax@lincotech.com.tw'))

pre = '[OK]'
    
msg['Subject'] = pre + '  Juniper Switch Backup Message'

s = smtplib.SMTP('mail.lincotech.com.tw',25) 	# create an SMTP object
s.ehlo()
s.sendmail('fax@lincotech.com.tw', ['misbackup@lincotech.com.tw'], msg.as_string())
s.close()
log.close()
