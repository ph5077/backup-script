"""
This script backup fg200d config
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
t_now = time.strftime("%Y%m%d-%H%M%S")
cmd0 ='scp -q  admin@192.168.168.2:sys_config '
cmd1 =' /volume1/Backup/network_equipment/fg200d/'
cmd2 = 'sys_config-'+t_now
scp_cmd  = cmd0 + cmd1 + cmd2

log_path = "/volume1/Backup/network_equipment/log/"
log_file_name = log_path + "fg200d-bkup.log-" + t_now
log = open(log_file_name, "w")

#
#
#
os.system(scp_cmd)

log.write('FG200D cfg Backup File ==> /volume1/Backup/network_equipment/fg200d/sys_config-'+t_now)


log.close()
#
# mail
#
log = open(log_file_name, "r")
msg = MIMEText(log.read())
msg['To'] = email.utils.formataddr(('MIS', 'misbackup@lincotech.com.tw'))
msg['From'] = email.utils.formataddr(('Fax', 'fax@lincotech.com.tw'))

pre = '[OK]'
    
msg['Subject'] = pre + '  FG200D Backup Message'

s = smtplib.SMTP('mail.lincotech.com.tw',25) 	# create an SMTP object
s.ehlo()
s.sendmail('fax@lincotech.com.tw', ['misbackup@lincotech.com.tw'], msg.as_string())
s.close()
log.close()
