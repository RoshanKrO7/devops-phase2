#! /bin/bash
DISK_THRESHOLD=80
DISK=0
check_disk() {
    DISK=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
    echo -e "\nChecking Disk Space: $DISK%"
    if [ $DISK -gt $DISK_THRESHOLD ]; then
        echo -e "NOT OK"
    else
        echo -e "OK"
    fi
}

if [ -z "$1" ]; then
echo usage: ./backup.sh [file location]
else
TIMESTAMP=$(date +%y-%m-%d-%H-%M)
echo "Starting backup of " $1
check_disk
if [ $DISK -lt $DISK_THRESHOLD ] ; then
	tar -czf backup-$TIMESTAMP.tar.gz $1
	echo -e Backup created : backup-$TIMESTAMP.tar.gz
	echo "size: $(du -sh backup-$TIMESTAMP.tar.gz)"
	echo "Backup successful! - $TIMESTAMP" >> ~/backup.log
else
	echo "ERROR: Disk usage too high! Backup aborted."
    	echo "Backup failed! - $TIMESTAMP - Disk full" >> ~/backup.log
fi
fi
