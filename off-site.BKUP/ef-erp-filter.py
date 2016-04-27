"""
Purpose: Filter the latest file in /volume1/Backup/ef-erp.BKUP/bkup
Output: 
       target     /volume1/Backup/off-site.BKUP/script/ef-erp-inc-file
       exclude    /volume1/Backup/off-site.BKUP/script/ef-erp-exc-file
Usage: filter.py log_file
"""
from os import listdir
from os.path import isfile, join
import re, sys

search_path = [
"/volume1/Backup/ef-erp.BKUP/bkup/EFDB/EFNETDB/"                      , 
"/volume1/Backup/ef-erp.BKUP/bkup/EFDB/EFNETDBPDLOG/"                 , 
"/volume1/Backup/ef-erp.BKUP/bkup/EFDB/EFNETSYS/"                     , 
"/volume1/Backup/ef-erp.BKUP/bkup/SmartERP_DB/COMPLETION/"            ,
"/volume1/Backup/ef-erp.BKUP/bkup/SmartERP_DB/COMP_IFRS/"             ,
"/volume1/Backup/ef-erp.BKUP/bkup/SmartERP_DB/DSCRPT/"                ,
"/volume1/Backup/ef-erp.BKUP/bkup/SmartERP_DB/DSCTEST/"               ,
"/volume1/Backup/ef-erp.BKUP/bkup/SmartERP_DB/EAGLES/"                ,
"/volume1/Backup/ef-erp.BKUP/bkup/SmartERP_DB/EXCEED/"                ,
"/volume1/Backup/ef-erp.BKUP/bkup/SmartERP_DB/EXD_IFRS/"              ,
"/volume1/Backup/ef-erp.BKUP/bkup/SmartERP_DB/KUNSHAN/"               ,
"/volume1/Backup/ef-erp.BKUP/bkup/SmartERP_DB/LEADER/"                ,
"/volume1/Backup/ef-erp.BKUP/bkup/SmartERP_DB/LEAD_IFRS/"             ,
"/volume1/Backup/ef-erp.BKUP/bkup/SmartERP_DB/LINCO/"                 ,
"/volume1/Backup/ef-erp.BKUP/bkup/SmartERP_DB/LINCO2/"                ,
"/volume1/Backup/ef-erp.BKUP/bkup/SmartERP_DB/LINCO_ROC/"             ,
"/volume1/Backup/ef-erp.BKUP/bkup/SmartERP_DB/LINCT/"                 ,
"/volume1/Backup/ef-erp.BKUP/bkup/SmartERP_DB/ReportServer/"          ,
"/volume1/Backup/ef-erp.BKUP/bkup/SmartERP_DB/ReportServerTempDB/"    ,    
"/volume1/Backup/ef-erp.BKUP/bkup/SmartERP_DB/SMARTDSCSYS/"           ,
"/volume1/Backup/ef-erp.BKUP/bkup/SmartERP_DB/STD/"                   ,
"/volume1/Backup/ef-erp.BKUP/bkup/YIFEI_Backup/BIOSDB/"               ,
"/volume1/Backup/ef-erp.BKUP/bkup/YIFEI_Backup/DEMO/"                 ,
"/volume1/Backup/ef-erp.BKUP/bkup/YIFEI_Backup/DSCSYS/"               ,
"/volume1/Backup/ef-erp.BKUP/bkup/YIFEI_Backup/GCRSDB/"               ,
"/volume1/Backup/ef-erp.BKUP/bkup/YIFEI_Backup/Leader/"               ,
"/volume1/Backup/ef-erp.BKUP/bkup/YIFEI_Backup/lincotech/"            ,
"/volume1/Backup/ef-erp.BKUP/bkup/YIFEI_Backup/report/"               ]

def extract_exclude(path, f_log, f_work, f_exc):    
    files_list = [f for f in listdir(path) if isfile(join(path, f))]
    tmp_name,tmp_date = None,None
    tmp_list = []
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
                f_work.write(path+tmp_name+tmp_date+'\n')
                tmp_list.append(tmp_name+tmp_date)
                tmp_name, tmp_date = vm_name, vm_date
        else:
            f_log.write("Error: VM Back Up File in"+path+f+" dosen't contain YYYY...............Skipped\n")
        
        if f == files_list[len(files_list)-1]:    # if LAST one
            f_work.write(path+tmp_name+tmp_date+'\n')
            tmp_list.append(tmp_name+tmp_date)
    
    exclude_list = [fl for fl in files_list if fl not in tmp_list]
    for exc in exclude_list:
        f_exc.write(path+exc+'\n')

# main
#
file_log = sys.argv[1]
f_log = open(file_log, "a")
f_work = open("/volume1/Backup/off-site.BKUP/script/ef-erp-inc-file", "w")
f_exc = open("/volume1/Backup/off-site.BKUP/script/ef-erp-exc-file", "w")
f_exc.write("log/*"+"\n")   # to skip the log file

for path in search_path:
     extract_exclude(path, f_log, f_work, f_exc)

f_work.close() 
f_log.close()
f_exc.close()
