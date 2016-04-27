#!/bin/sh
date > /volume1/homes/admin/copy.log

cp -r /volume1/Backup/FileServer/Department/A007*/###*/ /volume1/Backup/tar.backup/na-1.ServerBackup/ >> \
	/volume1/homes/admin/copy.log

date >> /volume1/homes/admin/copy.log
