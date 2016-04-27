"""
Purpose: Filter the latest file in /volume1/Backup/mount-Veeam
Output: /volume1/Backup/off-site.BKUP/script/workfile
Usage: filter.py log_file
"""
from os import listdir
from os.path import isfile, join
import re, sys

veeam_path='/volume1/Backup/mount-Veeam'
file_log = sys.argv[1]
f_log = open(file_log, "a")
f_work = open("/volume1/Backup/off-site.BKUP/script/workfile", "w")

files_list = [f for f in listdir(veeam_path) if isfile(join(veeam_path, f))]
tmp_list = []
tmp_name,tmp_date = None,None

for f in files_list:
    YYYY = re.search("\d{4}", f)            # match Year like 2016
    if YYYY:                                # if matched
        Yr = YYYY.start()
        vm_name = f[0:Yr]                   # VM name
        vm_date = f[Yr:]                    # VM date

        if not tmp_name:
            tmp_name, tmp_date = vm_name, vm_date
        elif (vm_name == tmp_name) and (vm_date > tmp_date):
            tmp_name, tmp_date = vm_name, vm_date
        elif (vm_name != tmp_name):
            f_work.write("/volume1/Backup/mount-Veeam/"+tmp_name+tmp_date+'\n')
            tmp_name, tmp_date = vm_name, vm_date
    else:
        f_log.write("Error: VM Back Up File Name dosen't contain YYYY...............Skipped\n")
        
    if f == files_list[len(files_list)-1]:    # if LAST one
        f_work.write("/volume1/Backup/mount-Veeam/"+tmp_name+tmp_date+'\n')


f_work.close() 
f_log.close()
