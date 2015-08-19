#!/bin/sh
####################################
#
# Backup to NFS mount script.
#
####################################

# What to backup. 
backup_files="/Users/mdb/Developer/git/recordpeeker/recordpeeker/data /Users/mdb/Developer/git/recordpeeker/recordpeeker/data_dump /Users/mdb/Developer/git/recordpeeker/recordpeeker/enemy_data /Users/mdb/Developer/git/recordpeeker/recordpeeker/debug"

# Where to backup to.
dest="/Users/mdb/Developer/git/recordpeeker/backups"
# dest="/backups/"

# Create archive filename.
# day=$(date +%A)
date=$(date +"%Y-%m-%d")
#+%m-%d-%Y_%H-%M)
# hostname=$(hostname -s)
# archive_file="$hostname-$day.tgz"
# archive_file="$recordpeeker_data-$day.tgz"
archive_file="recordpeeker_data-$date.tgz"
# archive_file="/Users/mdb/Developer/git/recordpeeker/backups/recordpeeker_data-$date.tgz"

# Print start status message.
echo "Backing up $backup_files to $dest/$archive_file"
date
echo

# Backup the files using tar.
tar czf $dest/$archive_file $backup_files

# Print end status message.
echo
echo "Backup finished"
date
pwd

# Long listing of files in $dest to check file sizes.
ls -lh $dest