# This script backup env ctrl PC project file 
# Run this script by admin 
# FileServer mount, by DSM, point: 
#                       /volume1/Backup/mount-env-ctrl_Lincotech
#                       /volume1/Backup/mount-env-ctrl_GT-531                      
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

SRC_Lincotech=/volume1/Backup/mount-env-ctrl_Lincotech/
SRC_GT531=/volume1/Backup/mount-env-ctrl_GT-531/


DST_Lincotech=/volume1/Backup/env-ctrl.BKUP/bkup/Lincotech
DST_GT531=/volume1/Backup/env-ctrl.BKUP/bkup/GT531

Lincotech_LOG=/volume1/Backup/env-ctrl.BKUP/log/"$now"-Lincotech.log
Lincotech_ERR=/volume1/Backup/env-ctrl.BKUP/log/"$now"-Lincotech.ERR.log

GT531_LOG=/volume1/Backup/env-ctrl.BKUP/log/"$now"-GT531.log
GT531_ERR=/volume1/Backup/env-ctrl.BKUP/log/"$now"-GT531.ERR.log

TS=/volume1/Backup/env-ctrl.BKUP/log/"$now"-env-ctrl-ts.log


date > $TS
echo "env-ctrl PC Lincotech Backup Started ......" >> $TS
rsync -avhq --delete -i --log-file=$Lincotech_LOG  $SRC_Lincotech $DST_Lincotech 2>$Lincotech_ERR
echo "env-ctrl PC Lincotech Backup Finished ......" >> $TS
DDD=$(grep 'deleting' $Lincotech_LOG | wc -l)
UUU=$(grep '>f' $Lincotech_LOG | wc -l)
echo "# of file updated in bk-1.... : " $UUU >> $TS
echo "# of file deleted in bk-1.... : " $DDD >> $TS
echo "Check log file in \\\\bk-1\\Backup\\env-ctrl.BKUP\\log\\"$now"-Lincotech.log >> $TS
echo "Check error file in \\\\bk-1\\Backup\\env-ctrl.BKUP\\log\\"$now"-Lincotech.ERR.log >> $TS
echo "   " >> $TS


date >> $TS
echo "env-ctrl PC GT531 Backup Started ......" >> $TS 
rsync -avhq --delete -i --log-file=$GT531_LOG  $SRC_GT531 $DST_GT531    2>$GT531_ERR
echo "env-ctrl PC GT531 Backup Finished ......" >> $TS
DDD=$(grep 'deleting' $GT531_LOG | wc -l)
UUU=$(grep '>f' $GT531_LOG | wc -l)
echo "# of file updated in bk-1.... : " $UUU >> $TS
echo "# of file deleted in bk-1.... : " $DDD >> $TS
echo "Check log file in \\\\bk-1\\Backup\\env-ctrl.BKUP\\log\\"$now"-GT531.log" >> $TS
echo "Check error file in \\\\bk-1\\Backup\\env-ctrl.BKUP\\log\\"$now"-GT531.ERR.log" >> $TS
echo "  " >> $TS



# mail $TS to misbackup
/bin/python /volume1/Backup/env-ctrl.BKUP/script/mail.py    $TS
