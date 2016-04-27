# This script backup \\na-1\FileServer to bk-1 
# Run this script by admin 
# FileServer mount, by DSM, point: /volume1/Backup/mount-FileServer/
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

SRC_BB=/volume1/Backup/mount-FileServer/Bulletin_board
SRC_DP=/volume1/Backup/mount-FileServer/Department
SRC_PF=/volume1/Backup/mount-FileServer/Personal_Folder
SRC_PD=/volume1/Backup/mount-FileServer/Public_disk

DST=/volume1/Backup/na-1-FileServer.BKUP/bkup/

BB_LOG=/volume1/Backup/na-1-FileServer.BKUP/log/"$now"-na-1-bkup.BB.log
DP_LOG=/volume1/Backup/na-1-FileServer.BKUP/log/"$now"-na-1-bkup.DP.log
PF_LOG=/volume1/Backup/na-1-FileServer.BKUP/log/"$now"-na-1-bkup.PF.log
PD_LOG=/volume1/Backup/na-1-FileServer.BKUP/log/"$now"-na-1-bkup.PD.log
TS=/volume1/Backup/na-1-FileServer.BKUP/log/"$now"-na-1-bkup.ts.log
EXC_FROM=/volume1/Backup/na-1-FileServer.BKUP/script/exclude_me.txt


date > $TS
echo "Bulletin Started ......" >> $TS
rsync -avhq --delete -i --log-file=$BB_LOG --exclude-from="$EXC_FROM" $SRC_BB $DST    2>$BB_LOG"-ERR"
echo "Bulletin Finished ......" >> $TS
DDD=$(grep 'deleting' $BB_LOG | wc -l)
UUU=$(grep '>f' $BB_LOG | wc -l)
echo "# of file updated in bk-1.... : " $UUU >> $TS
echo "# of file deleted in bk-1.... : " $DDD >> $TS
echo "Check log file in \\\\bk-1\\Backup\\na-1-FileServer.BKUP\\log\\"$now"-na-1-bkup.BB.log" >> $TS
echo "Check error file in \\\\bk-1\\Backup\\na-1-FileServer.BKUP\\log\\"$now"-na-1-bkup.BB.log-ERR" >> $TS
echo "   " >> $TS

date >> $TS
echo "Department Started ......" >> $TS 
rsync -avhq --delete -i --log-file=$DP_LOG --exclude-from="$EXC_FROM" $SRC_DP $DST    2>$DP_LOG"-ERR"
echo "Department Finished ......" >> $TS
DDD=$(grep 'deleting' $DP_LOG | wc -l)
UUU=$(grep '>f' $DP_LOG | wc -l)
echo "# of file updated in bk-1.... : " $UUU >> $TS
echo "# of file deleted in bk-1.... : " $DDD >> $TS
echo "Check log file in \\\\bk-1\\Backup\\na-1-FileServer.BKUP\\log\\"$now"-na-1-bkup.DP.log" >> $TS
echo "Check error file in \\\\bk-1\\Backup\\na-1-FileServer.BKUP\\log\\"$now"-na-1-bkup.DP.log-ERR" >> $TS
echo " " >> $TS


date >> $TS
echo "Personal_folder Started ......" >> $TS 
rsync -avhq --delete -i --log-file=$PF_LOG --exclude-from="$EXC_FROM" $SRC_PF $DST    2>$PF_LOG"-ERR"
echo "Personal_folder Finished ......" >> $TS
DDD=$(grep 'deleting' $PF_LOG | wc -l)
UUU=$(grep '>f' $PF_LOG | wc -l)
echo "# of file updated in bk-1.... : " $UUU >> $TS
echo "# of file deleted in bk-1.... : " $DDD >> $TS
echo "Check log file in \\\\bk-1\\Backup\\na-1-FileServer.BKUP\\log\\"$now"-na-1-bkup.PF.log" >> $TS
echo "Check error file in \\\\bk-1\\Backup\\na-1-FileServer.BKUP\\log\\"$now"-na-1-bkup.PF.log-ERR" >> $TS
echo "   " >> $TS


date >> $TS
echo "Public_disk Started ......" >> $TS
rsync -avhq --delete -i --log-file=$PD_LOG --exclude-from="$EXC_FROM" $SRC_PD $DST    2>$PD_LOG"-ERR"
echo "Public_disk Finished ......" >> $TS
date >> $TS
DDD=$(grep 'deleting' $PD_LOG | wc -l)
UUU=$(grep '>f' $PD_LOG | wc -l)
echo "# of file updated in bk-1.... : " $UUU >> $TS
echo "# of file deleted in bk-1.... : " $DDD >> $TS
echo "Check log file in \\\\bk-1\\Backup\\na-1-FileServer.BKUP\\log\\"$now"-na-1-bkup.PD.log" >> $TS
echo "Check error file in \\\\bk-1\\Backup\\na-1-FileServer.BKUP\\log\\"$now"-na-1-bkup.PD.log-ERR" >> $TS
echo " " >> $TS

# mail $TS to misbackup
/bin/python /volume1/Backup/na-1-FileServer.BKUP/script/na-1-mail.py    $TS
