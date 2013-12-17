#!/usr/bin/python

#
# Compares images of a BML and an STL partition,
# (that gets mounted out of this BML partition)
# and draws a picture to visualize,
# in which blocks differences are occuring
# Goal is, to learn more about how the sector remapping
# is working in STL
#
# Commands to read images from your (root+busybox'ed) phone:
# for i in {1..15}; do dd if=/dev/bml$i of=/sdcard/bml$i count=10; done;
# for i in {0..15}; do dd if=/dev/stl$i of=/sdcard/stl$i; done;
# Your SD card must be bigger than 512MB for these to work.
#

blocksize = 512000

from sys import argv
from os.path import getsize
from PIL import Image

width = 50
height = getsize(argv[1])/(blocksize*width)+5
img = Image.new('RGB', (width,height), (255,255,255))

f1 = open(argv[1])
f2 = open(argv[2])
x = 0
y = 0
maxX = width-1
while True:
    sector1 = f1.read(blocksize)
    sector2 = f2.read(blocksize)
    if sector1 == sector2:
        img.putpixel((x,y), (0,136,68))
    else:
        img.putpixel((x,y), (255,21,21))
    x += 1
    if x > maxX:
        x = 0
        y += 1
        print y
        print f1.tell()
    if sector1+sector2 == '':
        break

img.save('test.png', 'PNG')
img.show()
