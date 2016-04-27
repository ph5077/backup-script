#!/bin/sh
# This script must be run as root
# -z  ：透過 gzip  的支援進行壓縮/解壓縮
# -p(小寫) ：保留備份資料的原本權限與屬性
# -c  ：建立打包檔案
#
t_now=$(date +"%Y%m%d-%H%M%S")

tar -zpcv -f /volume1/Backup/bk-1-etc/tar.etc-bkup/etc.tar.gz.$t_now /etc  > \
   /volume1/Backup/bk-1-etc/log/etc-bkup.log.$t_now 2>&1
#
# find files older than 365 DAYS, then delete it
#
find /volume1/Backup/bk-1-etc/tar.etc-bkup/ -mtime +365 -exec rm {} \; >> \
	/volume1/Backup/bk-1-etc/log/etc-bkup.log.$t_now 2>&1

find /volume1/Backup/bk-1-etc/log/ -mtime +365 -exec rm {} \; >> \
	/volume1/Backup/bk-1-etc/log/etc-bkup.log.$t_now 2>&1

/usr/bin/python /volume1/Backup/bk-1-etc/etc-mail.py /volume1/Backup/bk-1-etc/log/etc-bkup.log.$t_now
