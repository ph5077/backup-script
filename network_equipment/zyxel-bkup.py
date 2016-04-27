"""
This script backup ZyXel Switch startup config
Note:
1.	The HTTP sequence below were captured from browser.
2.	Whenever you upate the config through web, 
	remember click "save" on the top right corner before logout,
	to save the "running config" to "startup config"  
"""
import requests
import time
import smtplib
import email.utils
from email.mime.text import MIMEText

login = {
"login": "1",
"username": "admin",
"password": "1234",
'dummy' : int(time.time()*1000)
	}

apply = {
"upmethod": "1", 		# HTTP
"type": "2",			# Startup configuration
"cmd": "5902",			# cmd
"sysSubmit": "Apply"	# Apply
	}

zyxel_sw = {
    "192.168.3.240": "Zyxel-HA-poe1",
    "192.168.3.241": "Zyxel-HA-poe2",
    "192.168.3.242": "Zyxel-HB-poe1",
    "192.168.3.243": "Zyxel-HC-poe1",
    "192.168.3.244": "Zyxel-HC-poe2",
    "192.168.3.245": "Zyxel-HD-poe1"
    }


t_now = time.strftime("%Y%m%d-%H%M%S")
cfg_path = "/volume1/Backup/network_equipment/zyxel/"
log_path = "/volume1/Backup/network_equipment/log/"
log_file_name = log_path + "zyxel-bkup.log-" + t_now
log = open(log_file_name, "w")
Failed = 0

for ip in zyxel_sw.keys():

    login_url = "http://"+ip+"/cgi-bin/dispatcher.cgi"
    startup_config_url = "http://"+ip+"/tmp/startup-config.cfg"
    save_url = "http://"+ip+"/cgi-bin/dispatcher.cgi?cmd=4"
    logout_url = "http://"+ip+"/cgi-bin/dispatcher.cgi?cmd=3"

    # Use 'with' to ensure the session context is closed after use.
    with requests.Session() as s:
        # login
        r = s.post(login_url, data=login)
        if r.status_code != 200:
            log.write("Login Failed at " + r.url + "\n")
            Failed += 1
            continue
        else:
            log.write("Login Ok at " + r.url + "\n")
	

        # Click "save" to save the running to startup config on the home page
        # To aviod in case user forgets to do this
	r = s.get(save_url)
	# print "Click Save.....", r.status_code
	if r.status_code != 200:
	    log.write("Click Save Failed at ", r.url + "\n")
	    Failed += 1	        
	    continue
	else:
	    log.write("Click Save Ok at " + r.url + "\n")

        # Post to apply HTTP Download 
	r = s.post(login_url, data=apply)
	# print "POST.....", r.status_code
	if r.status_code != 200:
	    log.write("POST Failed at ", r.url + "\n")
	    Failed += 1	        
	    continue
        else:
	    log.write("POST Ok at " + r.url + "\n")

        # Download the startup config file 
        d = s.get(startup_config_url)
        # print "Download.....", d.status_code
        if d.status_code != 200:
            log.write("Download Failed at ", d.url + "\n")
            Failed += 1	        
            continue
	else:
            log.write("Download Ok at " + d.url + "\n")
    
        # Logout
        r = s.get(logout_url)
        # print "Logout.....", r.status_code
	if r.status_code != 200:
	    log.write("Logout Failed at ", r.url + "\n")
	    Failed += 1	        
            continue
        else:
	    log.write("Logout Ok at " + r.url + "\n")
    
    cfg_file_name = cfg_path+"startup_config"+".cfg-"+zyxel_sw[ip]+"-"+t_now
    with open(cfg_file_name, "w") as cfg:
        cfg.write(d.content)
        cfg.close()

    log.write("\n")

log.close()

# mail
log = open(log_file_name, "r")
msg = MIMEText(log.read())
msg['To'] = email.utils.formataddr(('MIS', 'misbackup@lincotech.com.tw'))
msg['From'] = email.utils.formataddr(('Fax', 'fax@lincotech.com.tw'))
if Failed == 0:
    pre = '[OK]'
else:
    pre = '[Failed]'
    
msg['Subject'] = pre + '  ZyXel Switch Back Up Messege'


s = smtplib.SMTP('mail.lincotech.com.tw',25) 	# create an SMTP object
s.ehlo()
s.sendmail('fax@lincotech.com.tw', ['misbackup@lincotech.com.tw'], msg.as_string())
s.close()
