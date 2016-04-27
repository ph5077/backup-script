# This script backup APP and DB of EF and ERP 
# Run this script by admin 
# mount point by DSM: 
#                   /volume1/Backup/mount-DBbackup/EFDB
#                   /volume1/Backup/mount-DBbackup/SmartERP_DB
#                   /volume1/Backup/mount-EasyFlow/
#                   /volume1/Backup/mount-SmartERP/
#                   /volume1/Backup/mount-SM82C_data/
#                   /volume1/Backup/mount-YIFEI_Backup/
#                   /volume1/Backup/mount-YIFEI_Conductor/
#
# rsync -av --delete
# -a        : archive mode; equals -rlptgoD (no -H,-A,-X)
#             r: recursive, l: copy symlink as symlink, p:preserve permissions
#             g: preserve group, o: preserve owner (super-user only), 
#             D: --devices preserve device files (super-user only)
#                --specials preserve special files
# -q        : quiet
# -h        : humand readable
# --delete  : is file not existed in source, delete it from destination
#

now=$(date +"%Y-%m%d-%H%M%S")

SRC_EF_DB=/volume1/Backup/mount-DBbackup/EFDB
SRC_ERP_DB=/volume1/Backup/mount-DBbackup/SmartERP_DB
SRC_EF_APP=/volume1/Backup/mount-EasyFlow/
SRC_ERP_APP=/volume1/Backup/mount-SmartERP/
SRC_SM82C=/volume1/Backup/mount-SM82C_data/
SRC_YF_DB=/volume1/Backup/mount-YIFEI_Backup/
SRC_YF_APP=/volume1/Backup/mount-YIFEI_Conductor/

DST_EF_DB=/volume1/Backup/ef-erp.BKUP/bkup
DST_ERP_DB=/volume1/Backup/ef-erp.BKUP/bkup
DST_EF_APP=/volume1/Backup/ef-erp.BKUP/bkup/EF_APP
DST_ERP_APP=/volume1/Backup/ef-erp.BKUP/bkup/ERP_APP
DST_SM82C=/volume1/Backup/ef-erp.BKUP/bkup/SM82C
DST_YF_DB=/volume1/Backup/ef-erp.BKUP/bkup/YIFEI_Backup
DST_YF_APP=/volume1/Backup/ef-erp.BKUP/bkup/YIFEI_Conductor

LOG_EF_DB=/volume1/Backup/ef-erp.BKUP/log/"$now"-EF_DB.log
LOG_ERP_DB=/volume1/Backup/ef-erp.BKUP/log/"$now"-ERP_DB.log
LOG_EF_APP=/volume1/Backup/ef-erp.BKUP/log/"$now"-EF_APP.log
LOG_ERP_APP=/volume1/Backup/ef-erp.BKUP/log/"$now"-ERP_APP.log
LOG_SM82C=/volume1/Backup/ef-erp.BKUP/log/"$now"-SM82C.log
LOG_YF_DB=/volume1/Backup/ef-erp.BKUP/log/"$now"-YF_DB.log
LOG_YF_APP=/volume1/Backup/ef-erp.BKUP/log/"$now"-YF_APP.log

ERR_EF_DB=/volume1/Backup/ef-erp.BKUP/log/"$now"-EF_DB.ERR.log
ERR_ERP_DB=/volume1/Backup/ef-erp.BKUP/log/"$now"-ERP_DB.ERR.log
ERR_EF_APP=/volume1/Backup/ef-erp.BKUP/log/"$now"-EF_APP.ERR.log
ERR_ERP_APP=/volume1/Backup/ef-erp.BKUP/log/"$now"-ERP_APP.ERR.log
ERR_SM82C=/volume1/Backup/ef-erp.BKUP/log/"$now"-SM82C.ERR.log
ERR_YF_DB=/volume1/Backup/ef-erp.BKUP/log/"$now"-YF_DB.ERR.log
ERR_YF_APP=/volume1/Backup/ef-erp.BKUP/log/"$now"-YF_APP.ERR.log

TS=/volume1/Backup/ef-erp.BKUP/log/"$now"-ef-erp-ts.log

EXC_FROM=/volume1/Backup/ef-erp.BKUP/script/exclude_me.txt

date > $TS

# rsync -avhq --delete -i --log-file=$BB_LOG --exclude-from="$EXC_FROM" $SRC_BB $DST    2>$BB_LOG"-ERR"
# Arguments
#   #1 : SRC
#   #2 : DST
#   #3 : LOG
#   #4 : ERR
#
function sync(){ 
    src_name=(${1})
    date >> $TS
    echo $src_name " ......Backup Started ......" >> $TS
    rsync -avhq --delete -i --log-file=$3  --exclude-from="$EXC_FROM" $1 $2    2>$4
    echo $src_name " ......Backup Finished ......" >> $TS
    
    DDD=$(grep 'deleting' $3 | wc -l)
    UUU=$(grep '>f' $3 | wc -l)
    echo "# of file updated in " $src_name " .... : " $UUU >> $TS
    echo "# of file deleted in " $src_name " .... : " $DDD >> $TS
    echo "Check log file in $3 " >> $TS 
    echo "Check error file in $4" >> $TS 
    echo "   " >> $TS
}

# EF_APP, ERP_APP, YF_APP Archive
# Remove archive older than 2 weeks
#
BK=/volume1/Backup/ef-erp.BKUP/bkup/
cd /volume1/Backup/ef-erp.BKUP/bkup/tar.app

# Remove archive older than 2 weeks, only dir starting with 20**
find . -maxdepth 1 -name "20*" -type d  -mtime +14 \
    -exec sh -c "echo removing dir > 2 weeks ... {} >$TS; rm -fr {}" \;

apps="EF_APP ERP_APP SM82C YIFEI_Conductor"
for app in $apps
do    
    echo mkdir $now\_$app " .... Dir Created"   >> $TS
    mkdir $now\_$app                                    # new a dir
    echo cp -r $BK$app $now\_$app >> $TS
    cp -r $BK$app $now\_$app                            # copy data of previous day
done

echo " Archieve APP dir finished..... " >> $TS
echo " " >> $TS

# rsync
# 
sync $SRC_EF_DB     $DST_EF_DB      $LOG_EF_DB      $ERR_EF_DB 
sync $SRC_ERP_DB    $DST_ERP_DB     $LOG_ERP_DB     $ERR_ERP_DB 
sync $SRC_EF_APP    $DST_EF_APP     $LOG_EF_APP     $ERR_EF_APP 
sync $SRC_SM82C     $DST_SM82C      $LOG_SM82C      $ERR_SM82C 
sync $SRC_YF_DB     $DST_YF_DB      $LOG_YF_DB      $ERR_YF_DB 
sync $SRC_YF_APP    $DST_YF_APP     $LOG_YF_APP     $ERR_YF_APP 

# mail $TS to misbackup
/bin/python /volume1/Backup/ef-erp.BKUP/script/mail.py    $TS

exit
