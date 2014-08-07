import cv2
import PIL.Image as Image
import numpy as np
import os
import sys
import matplotlib.pyplot as plt1

#import skimage.feature
#from skimage.feature import hog

#from skimage import data, color, exposure
from plot_hog import *

def newhognew(file1):

    img = cv2.imread(file1,0)

    """
    th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
        cv2.THRESH_BINARY,11,2)
    """
    th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
        cv2.THRESH_BINARY,11,2)
    contours,hierarchy = cv2.findContours(th2, 1, 2)
    i=0
    k=1
    k1=1
    #print len(contours)
    #cnt = contours[2]
    for i in range(0,len(contours)):
        cnt = contours[i]
        x,y,w,h = cv2.boundingRect(cnt)
        #print x,y,w,h
        if(h>=50 and w>=50):
            im = Image.open(file1)
            box = [x, y, x+w, y+h]
            piece=im.crop(box)
            img=Image.new('RGB', (w,h), 255)
            img.paste(piece)
            width=100
            height=100
            img=img.resize((width,height),Image.BILINEAR)
            path=os.path.join('C:\meenuneenu\project\libsvm-3.17\python\data',"IMG-%s.png" % k1)
            img.save(path)
            plothog(k1)
            path1=os.path.join('C:\meenuneenu\project\libsvm-3.17\python\preposition',"IMG-%s" % k1)
            file = open(path1, "w")
            file.write("%s " % str(box))
            file.close()
            #delpath=os.path.join('rm C:\meenuneenu\project\libsvm-3.17\python\data',"IMG-%s.png" % k1)
            #os.system(delpath)
            k1=k1+1
    file = open('C:/meenuneenu/project/libsvm-3.17/python/no', "w")
    file.write("%s " % (k1-1))
    file.close()
#delpath=os.path.join('rm C:/Python27/Lib/site-packages/temp/rectangle',"IMG-%s.png" % (k-1))
#os.system(delpath)