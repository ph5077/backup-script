"""
This script backup ASCENLINK 5050 config
Note:
1.	The HTTP sequence below were captured from browser.
"""
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import time
import smtplib
import email.utils
from email.mime.text import MIMEText

apply_login = {
"Language": "0",
"AccountAlias": "Administrator",
"Password": "1q2w#E$R",
"AdminCheck": "yes",
"SubmitBar": "+Login",
"Action": ""
	}

apply_admin = {
"no_submit": "yes",
"AdministratorAlias":"Add+New",
"AdministratorAliasAdd":"",
"AdministratorPassword":"",
"AdministratorCheck":"",
"MonitorAlias":"Add+New",
"MonitorAliasAdd":"",
"MonitorPassword":"",
"MonitorCheck":"",
"Setserverenable":"0",
"RadiusChoice":"Radius",
"Setserverip":"",
"Setserverport":"",
"Setserversecret":"",
"Setnasip":"",
"Setnasport":"",
"Setapacheport":"8000",
"AuthenticationString":"",
"UserCommand":"SaveConfiguration",
"UserAction":""
	}

t_now = time.strftime("%Y%m%d-%H%M%S")
cfg_path = "/volume1/Backup/network_equipment/ascenlink/"
cfg_file_name = cfg_path + "ascenlink.cfg-" + t_now
log_path = "/volume1/Backup/network_equipment/log/"
log_file_name = log_path + "ascenlink-bkup.log-" + t_now
log = open(log_file_name, "w")
cfg = open(cfg_file_name, "w")
Failed = 0

url = "https://192.168.168.1:8000"
login_url = url + "/script/login.php"
admin_url = url + "/script/system/administration.php"
save_url = url + "/AscenLink.cfg"

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

# Download cfg
#
    r = s.get(admin_url, data=apply_admin, verify=False)
    r = s.post(save_url, verify=False)
    if r.status_code != 200:
        log.write("Download Aruba StartUp Config Failed at " + r.url + str(r.status_code) + "\n")
        Failed += 1
    else:
        log.write("Download ASCENLINK Config OK at " + r.url + "\n")
        log.write("     File ==> "+ cfg_path+"ascenlink.cfg-"+t_now + "\n")
        cfg.write(r.content)

#       
# Logout    
#
    r = s.get(url, verify=False)
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
    
msg['Subject'] = pre + '  ASCENLINK 5050 Back Up Messege'

s = smtplib.SMTP('mail.lincotech.com.tw',25) 	# create an SMTP object
s.ehlo()
s.sendmail('fax@lincotech.com.tw', ['misbackup@lincotech.com.tw'], msg.as_string())
s.close()
log.close()
