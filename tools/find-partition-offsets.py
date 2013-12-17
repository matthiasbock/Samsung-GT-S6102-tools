#!/usr/bin/python

#
# This program attempts to find the offset of BML partition within a complete image
#
# It assumes images of all BML partitions to be present
# in the current directory, where bml0 contains the complete NAND content
# and bml1-x respectively contain at least the first couple of sectors
# of the corresponding BML partitions.
#
# Images could be obtained like this:
# dd if=/dev/bml0 of=/sdcard/bml0;
# for i in {1..15}; do dd if=/dev/bml$i of=/sdcard/bml$i count=10; done;
#

from sys import exit

block_size = 4096

partitions = []

f = open('bml0')

previous_start = -1
def print_size():
    global start, previous_start, partitions
    if previous_start > -1:
        size = start-previous_start
        partitions[len(partitions)-1]['size'] = size
        size = size/1024 # K
        print str(size)+'K',
        if size > 1024:
            print '('+str(size/1024)+'M)'
        else:
            print
    previous_start = start

for i in range(1,16):
    partition_head = open('bml'+str(i)).read(block_size)
    sector = ''
    while sector != partition_head:
        sector = f.read(block_size)
        if sector == '':
            print 'EOF'
            break
        if sector == partition_head:
            start = f.tell()-block_size
            print_size()
            partitions.append({'offset':start})
            h = hex(start)
            if h[len(h)-1] == 'L':
                h = h[:-1]
            offset = str(start/1024)
            print 'bml'+str(i)+': offset '+h+' = '+offset+'K, size',
print_size()

f.close()

#
# Using the findings from above
# create a losetup script, that allows accessing the partitions
# within the complete image
#

i = 1
for partition in partitions:
    print 'losetup /dev/loop'+str(i)+' bml0 --offset '+str(partition['offset'])+' --sizelimit '+str(partition['size'])
    i += 1
