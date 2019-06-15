from utils import *
from createXML import createXML

import os
import cv2
import random

thresh = 0.4
def cropImg_old(img):
    h,w,c = img.shape
    nh,nw = 300,400
    offsetH = h - nh
    offsetW = w - nw
    newTopLeftY = max(int(random.random() * offsetH),int(0.3 * offsetH))
    newTopLeftX = max(int(random.random() * offsetW),int(0.3 * offsetW))
    dstImg = img[newTopLeftY:newTopLeftY + nh,newTopLeftX:newTopLeftX + nw]
    cv2.imwrite("cropimg.jpg",dstImg)


def cropImg(img,nW,nH):
    h,w,c = img.shape
    nh,nw = nH,nW
    offsetH = h - nh
    offsetW = w - nw
    newTopLeftY = max(int(random.random() * offsetH),int(0.3 * offsetH))
    newTopLeftX = max(int(random.random() * offsetW),int(0.3 * offsetW))
    dstImg = img[newTopLeftY:newTopLeftY + nh,newTopLeftX:newTopLeftX + nw]
    #cv2.imwrite("cropimg.jpg",dstImg)
    return newTopLeftX,newTopLeftY,dstImg


def main():
    srcImgPath = '/home/zhanghan/person/data0612/labeladd0524/rename0524/'
    srcXmlPath = '/home/zhanghan/person/data0612/labeladd0524/addxml0524/'
    dstImgPath = '/home/zhanghan/person/data0614/aug0524/img/'
    dstXmlPath = '/home/zhanghan/person/data0614/aug0524/xml/'
    N = 2
    nW,nH = 400,300
    files = os.listdir(srcImgPath)
    for f in files:
        if(random.random() < thresh):
            img = cv2.imread(srcImgPath + f)
            fname,pf = f.split('.')
            for i in range(N):
                pointX,pointY,dstImg = cropImg(img,nW,nH)
                newFname = dstImgPath + fname + '_' + str(pointX) + '_' + str(pointY) + '_crop.jpg'
                newXMLname = dstXmlPath + fname + '_' + str(pointX) + '_' + str(pointY) + '_crop.xml'
                cv2.imwrite(newFname,dstImg)
                newXML = createXML(srcXmlPath + fname + '.xml')
                newXML.crop(pointX,pointY,nW,nH,newXMLname)
            
if __name__ == '__main__':
    main()
