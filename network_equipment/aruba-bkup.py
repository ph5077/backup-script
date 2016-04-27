"""
This script backup Aruba 7010 config
Note:
1.	The HTTP sequence below were captured from browser.
2. 	FTP download to /volume1/homes/juniper/
3.	Move to /volume1/Backup/network_equipment/juniper 
"""
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time
import smtplib
import email.utils
from email.mime.text import MIMEText
import shutil

apply_login = {
"opcode": "login",
"url": "/screens/wms/wms.login",
"needxml": "0",
"uid": "admin",
"passwd": "aruba123",
	}

apply_startup = {
"args": "put,no,logs,192.168.168.179,juniper,juniper123,.,/flash/config/Aruba7010-config,aruba-startup.cfg,ftp,known_host",
"method": "ftp",
"UIDARUBA": "" 
	}

t_now = time.strftime("%Y%m%d-%H%M%S")
cfg_path = "/volume1/Backup/network_equipment/aruba/"
log_path = "/volume1/Backup/network_equipment/log/"
log_file_name = log_path + "aruba-bkup.log-" + t_now
log = open(log_file_name, "w")
Failed = 0

url = "https://192.168.168.3"
login_url = url + ":4343/screens/wms/wms.login"
logout_url = url + ":4343/logout.html"
startup_url = url + ":4343/screens/cmnutil/ncftp.html"
cmd = 'copy running-config ftp 192.168.168.179 juniper juniper123 aruba-running.cfg . &UIDARUBA='
running_url = url + ':4343/screens/cmnutil/execFPCliCommand.xml?'+cmd

# Disable Security Warnning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Use 'with' to ensure the session context is closed after use.
with requests.Session() as s:
# Login
    r = s.get(url, verify=False)
    r = s.post(login_url, data=apply_login, verify=False)
    if r.status_code != 200:
        log.write("Login Failed at " + r.url + "\n")
        Failed += 1
    else:
        log.write("Login Ok at " + r.url + "\n")

# Download startup_cfg, move it to ./aruba
#
    session = r.headers['set-cookie'][8:44]
    apply_startup['UIDARUBA'] = session
    r = s.post(startup_url, data=apply_startup)
    if r.status_code != 200:
        log.write("Download Aruba StartUp Config Failed at " + r.url + str(r.status_code) + "\n")
        Failed += 1
    else:
        log.write("Download Aruba StartUp Config OK at " + r.url + "\n")
        shutil.move("/volume1/homes/juniper/aruba-startup.cfg", cfg_path+"aruba-startup.cfg-"+t_now) 
        log.write("     File ==> "+ cfg_path+"aruba-startup.cfg-"+t_now + "\n")

# Download running_cfg, move it to ./aruba
#
    r = s.get(running_url+session, verify=False) 
    if r.status_code != 200:
        log.write("Download Aruba Running Config Failed at " + r.url + str(r.status_code) + "\n")
        Failed += 1
    else:
        log.write("Download Aruba Running Config OK at " + r.url + "\n")
        shutil.move("/volume1/homes/juniper/aruba-running.cfg", cfg_path+"aruba-running.cfg-"+t_now) 
        log.write("     File ==> " + cfg_path+"aruba-running.cfg-"+t_now + "\n")
#       
# Logout    
#
    r = s.get(logout_url, verify=False)
    log.write("Logout Ok at " + r.url + "\n")
    log.write("     File ==> " + log_file_name + "\n")

    
log.close()
#
# mail
#
log = open(log_file_name, "r")
msg = MIMEText(log.read())
msg['To'] = email.utils.formataddr(('MIS', 'misbackup@lincotech.com.tw'))
msg['From'] = email.utils.formataddr(('Fax', 'fax@lincotech.com.tw'))
if Failed == 0:
    pre = '[OK]'
else:
    pre = '[Failed]'
    
msg['Subject'] = pre + '  Aruba7010 WI-FI Controller Back Up Messege'

s = smtplib.SMTP('mail.lincotech.com.tw',25) 	# create an SMTP object
s.ehlo()
s.sendmail('fax@lincotech.com.tw', ['misbackup@lincotech.com.tw'], msg.as_string())
s.close()
log.close()
