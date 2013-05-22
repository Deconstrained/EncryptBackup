# encryptBackup.py #
Script for maintaining partial, incremental data backups on multiple encrypted drives.

## Usage ##
This script is for the following scenario:
* You use Linux
* You have a few spare hard drives of medium-large size that you would like to use for back ups
* You have a decent hard drive dock for mounting and transferring data to the hard drives (I recommend Rosewill; there are a few models in the $20-30 range that work well enough)
* You don't feel like sparing the money and/or time to turn said drives into some sort of fancy array to use all of their storage capacity and use them collectively as one device
* You want your backups to be encrypted, for whatever reason
If all of the above apply to you, this script might be useful. What it does is (once configured) reduces the effort of maintaining encrypted, partial, incremental backups (private, copies a part of your data, copies only what changed since the last backup). It does this by detecting which hard drive you've inserted, unlocking/decrypting it, and then backing up the specific directories of your data that you intend to store on that particular disk. When it's done, it unmounts/locks the device so that you can quickly take it out and swap in another. The full procedure is as follows:
1. Insert the drive
2. Run the script (no command line options necessary; if you insist, see -h for options)
3. When the script finishes, remove the drive.
That's about it.

## Disclaimer ##
I highly recommend that you use two LUKS key slots on your encrypted drives: both the key file that this script will use, and a secure encryption passphrase you use for some other equally-secure purpose, and often enough to remember (perhaps even the encryption passphrase of your own computer's hard drive) or have written down somewhere. A backup is utterly useless if you cannot access the data in it.
