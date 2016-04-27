# Purpose: tar BKUP dir and script to external USB DRIVE for off-site storage
#          7z password, $RANDOM, protected
#          mail log and $RANDOM to misbackup 
# Source: /volume1/Backup
#           README
#
#           /volume1/Backup/mount-VaultBackup
#           /volume1/Backup/mount-Veeam
#
#           bk-1-etc       
#           env-ctrl.BKUP
#           network_equipment
#           na-1.monitor
#
#           ef-erp.BKUP         (Yifei included) 
#
#           na-1-FileServer.BKUP
#           
# TBD:
#           Mail
#
# Note: Execution Timing must avoid conflict data changing in mount-Veeam
#       which is daily backuped
#
# Target: $DST

now=$(date +"%Y-%m%d-%H%M%S")
OFF_SITE_LOG=/volume1/Backup/off-site.BKUP/log/$now-off-site-bkup.log
# DST=/volumeUSB2/usbshare
# DST=/volume1/Backup/off-site.BKUP/bkup
USB1=/volumeUSB1/usbshare
USB2=/volumeUSB2/usbshare

# =================================
# 0.0 Detect external USB Drive
#     Remove existing contents in USB DRIVE
#     Generate a random number as password   
# =================================
if [ -d "$USB1" ]; then
    DST=$USB1
    echo "Found USB Drive....." $USB1 > $OFF_SITE_LOG
elif [ -d "$USB2" ]; then
    DST=$USB2
    echo "Found USB Drive....." $USB2 > $OFF_SITE_LOG
else
    echo "NO USB DRIVE Available......Exit" > $OFF_SITE_LOG
    exit
fi

#
cd $DST
cwd=$(pwd)
if [ "$DST" == "$cwd" ]; then
    rm -fr *                ## Delete file check, Be careful
else
    echo "Error: can't cd to USB drive.......Exit" >> $OFF_SITE_LOG
    exit
fi    


PPP=$RANDOM
date >> $OFF_SITE_LOG
echo '7z Compression Password : ' $PPP  >> $OFF_SITE_LOG

# =================================
# 1.0 Vault DB BKUP 
#     tar 7z
# =================================
cd /volume1/Backup/mount-VaultBackup  
f_list=$(find . -maxdepth 1 -ctime -1)  # get one file and one dir, updated in one day 
vault_list=${f_list:1}                  # remove the 1st "."

echo "$(date +"%Y-%m%d-%H%M%S") tar Start..... : VaultBackup "  >>  $OFF_SITE_LOG

tar -cf -  $vault_list  2>>$OFF_SITE_LOG   |  7z a -mx0 -p$PPP -si $DST/$now.VaultBackup.tar.7z


# =================================
# 2.0 Filter Veeam file list to workfile
#     Copy Veeam file
# =================================
/bin/python  /volume1/Backup/off-site.BKUP/script/veeam-filter.py $OFF_SITE_LOG

echo "$(date +"%Y-%m%d-%H%M%S") Veeam Copy Start..... : "  >>  $OFF_SITE_LOG
file_list="`cat /volume1/Backup/off-site.BKUP/script/workfile`"

for f in $file_list
do
    cp  $f $DST
    echo "$(date +"%Y-%m%d-%H%M%S") $f Copy End..... : "  >>  $OFF_SITE_LOG
done

echo "$(date +"%Y-%m%d-%H%M%S") veeam Copy End..... : " >>  $OFF_SITE_LOG
echo "Check log file at \\\\bk-1\\Backup\\\off-site.BKUP\\log\\"$now"-off-site-bkup.log">> $OFF_SITE_LOG
rm -f /volume1/Backup/off-site.BKUP/script/workfile

# =================================
# 3.0 tar 7z each dir in dirs
# =================================
EXC='--exclude 'System.Volume.Information/*'  --exclude 'System.Volume.Information' --exclude '.RECYCLE.BIN/*' --exclude '.RECYCLE.BIN' --exclude 'log/*' --exclude 'log' --exclude 'tmp/*' --exclude 'tmp' '

cd /volume1/Backup

dirs="bk-1-etc  env-ctrl.BKUP  network_equipment na-1.monitor"

for ddd in $dirs
do
    echo "$(date +"%Y-%m%d-%H%M%S") tar Start..... : " $ddd >>  $OFF_SITE_LOG 
# if using 7z  
    tar -cf -  $EXC  $ddd  2>>$OFF_SITE_LOG   |  7z a -mx0 -p$PPP -si $DST/$now.$ddd.tar.7z 
#   tar -c $EXC -f $DST/$now.$ddd.tar $ddd 2>> $OFF_SITE_LOG  
done

echo "$(date +"%Y-%m%d-%H%M%S") tar End..... : " >>  $OFF_SITE_LOG 

# =================================
# 4.0 ef erp db app
#   avoid whole dir 
#   only tar the latest file
# =================================
cd /volume1/Backup
/bin/python  /volume1/Backup/off-site.BKUP/script/ef-erp-filter.py $OFF_SITE_LOG
echo "$(date +"%Y-%m%d-%H%M%S") tar Start..... : ef erp  "  >>  $OFF_SITE_LOG 
tar -cf -  -X /volume1/Backup/off-site.BKUP/script/ef-erp-exc-file   ef-erp.BKUP  2>>$OFF_SITE_LOG  \
    |  7z a -mx0 -p$PPP -si $DST/$now.ef-erp.BKUP.tar.7z 

# =================================
# 5.0 na-1 file folders
# =================================
cd /volume1/Backup/na-1-FileServer.BKUP
ddd=script
echo "$(date +"%Y-%m%d-%H%M%S") tar 7z Start..... : $ddd" >>  $OFF_SITE_LOG 
tar -cf -  $EXC  $ddd 2>>$OFF_SITE_LOG   |  7z a -mx0 -p$PPP  -si $DST/$now.$ddd.tar.7z 

cd /volume1/Backup/na-1-FileServer.BKUP/bkup
dirs="  Bulletin_board \
        Department  \
        Personal_Folder  \
        Public_disk"

for ddd in $dirs
do
    echo "$(date +"%Y-%m%d-%H%M%S") tar 7z Start..... : " $ddd >>  $OFF_SITE_LOG 
    tar -cf -  $EXC  $ddd    |  7z a -mx0 -p$PPP  -si $DST/$now.$ddd.tar.7z 
done


echo "$(date +"%Y-%m%d-%H%M%S") tar End..... : " >>  $OFF_SITE_LOG 



# =================================
# last: Mail logfile to misbackup
# =================================
echo "Check log file at \\\\bk-1\\Backup\\\off-site.BKUP\\log\\"$OFF_SITE_LOG" ">> $OFF_SITE_LOG
/bin/python  /volume1/Backup/off-site.BKUP/script/mail.py $OFF_SITE_LOG '[OFF-SITE BKUP] Backup Message' 
