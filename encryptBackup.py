#!/usr/bin/env python
import os,subprocess,sys
from optparse import OptionParser

# CONFIGURATION

# Define your aliases here. Keys = aliases, values = description of each device.
defs = {
}

# Define your encrypted hard drives here. Keys = disk UUID; value = drive alias.
cryptPartitions = {
}

# Define your rsync starting paths here as key = alias, value = path
path = {
}

# Define your destination paths here, i.e. subdirectory of mount point /mt/mount, key = alias
dest = {
}

# Define excluded paths here as key = alias, value = list of paths to exclude in rsync
excludePaths = {
}

# Where the key file to unlock the encrypted backups is stored
keyFile = ''

# Encrypted device's name
encryptDevName = 'backup'

# Mount point
mountPoint = '/mnt/backup'

# END CONFIGURATION

usage_text = '%prog [options]'
info_text = 'If called with no options, it will: (1) Unlock/mount; (2) Backup, and (3) dismount. Performing '
parser = OptionParser(usage=usage_text)
parser.add_option('-m','--mount',action='store_true',default=False,help='Unlock/mount the current volume if not mounted already.')
parser.add_option('-c','--cont',action='store_true',default=False,help='Assume the backup volume is already unlocked/mounted and continue an existing backup.')
parser.add_option('-u','--umount',action='store_true',default=False,help='Unmount the current volume, if any, and exit.')
opts = parser.parse_args()[0]

default = not (opts.mount or opts.cont or opts.umount)

def sudoCall(popenArgs):
	sudoComm = ['sudo','-u','root']
	sudoComm.extend(popenArgs)
	subprocess.call(sudoComm)

def unlockEncryptedBackup(uuid):
	global keyFile
	sudoCall(['cryptsetup','luksOpen','-d',os.path.expanduser(keyFile),'/dev/disk/by-uuid/'+uuid,'backup'])

def lockEncryptedBackup():
	global encryptDevName
	sudoCall(['cryptsetup','luksClose',encryptDevName])

def mountEncryptedBackup():
	global encryptDevName,mountPoint
	sudoCall(['mount','/dev/mapper/'+encryptDevName,mountPoint])

def umountEncryptedBackup():
	global encryptDevName
	sudoCall(['umount','/dev/mapper/'+encryptDevName])

getDevs = subprocess.Popen(['ls','-1','/dev/disk/by-uuid'],stdout=subprocess.PIPE)

# Find a drive to perform backup on;
# Pick the first UUID that matches an encrypted backup device:
uuid = ''
for line in getDevs.stdout:
	lTrim = line.strip()
	if lTrim in cryptPartitions:
		uuid = lTrim

if uuid == '':
	print 'No backup drive present.'
	sys.exit(1)

# Set the short three-letter key for the drive:
alias = cryptPartitions[uuid]

# Mount:
if opts.mount or default:
	unlockEncryptedBackup(uuid)
	mountEncryptedBackup()

# Run rsync:
if opts.cont or default:
	# Compose rsync command:
	rsync = ['rsync','-a','--delete']

	# Excludes:
	rsync.extend(['--exclude='+epath for epath in excludePaths[alias]])

	# Source and target:
	rsync.extend([os.path.expanduser(path[alias]),os.path.expanduser(dest[alias])])

	# Run rsync:
	subprocess.call(rsync)

# Dismount:
if opts.umount or default:
	umountEncryptedBackup()
	lockEncryptedBackup()
