#!/usr/bin/python

#
# cronjob that automatically checks,
# if there are any pictures in your camera folder
# and downloads them into your local Pictures folder 
#
# Requires root priviledges and ssh/sftp server (on the phone)
#

from subprocess import Popen,PIPE
from shlex import split
from os.path import exists,join

phonehostip = 'galaxy'
camerapath = '/sdcard/DCIM/Camera'
localpath = '/home/user/Pictures'

def listfiles(path):
    cmd = 'ssh root@'+phonehostip+' ls '+path
    print cmd
    return Popen(split(cmd), stdout=PIPE, stderr=PIPE).communicate()[0].split('\n')

def download(filename):
    local = join(localpath,filename)
    if not exists(local):
        remote = join(camerapath,filename)
        #cmd = 'adb pull "'+remote+'" "'+localpath+'/"'
        #cmd = 'scp "root@'+phonehostip+':'+remote+'" "'+localpath+'/"'
        cmd = 'ssh root@'+phonehostip+' "dd if='+remote.replace(' ','\ ')+'"'
        print cmd
        data = Popen(split(cmd), stdout=PIPE, stderr=PIPE).communicate()[0]
        open(local, 'w').write(data)
        return True
    else:
        print 'Aborted: Local file "'+local+'" exists, not overwriting'
        return False 

count = 0

for file in listfiles(camerapath):
    if len(file.strip()) > 0 and file[-4:].lower() == '.jpg':
        if download(file):
            count += 1

print str(count)+" file(s) downloaded"
