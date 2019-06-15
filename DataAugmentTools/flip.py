from utils import *
from createXML import createXML

import os
import cv2
import random

thresh = 0.4
def flipImg(img,xml,imgPath,xmlPath):
    
    dstImg = cv2.flip(cv2.imread(img),1)
    newXML = createXML(xml)
    
    name = img.split('/')[-1]
    fname,pf = name.split('.')
    newFname = imgPath + fname + '_flip.jpg'
    newXMLname = xmlPath + fname + '_flip.xml'
    cv2.imwrite(newFname,dstImg)
    newXML.flip(newXMLname)

def main():
    srcImgPath = '/home/zhanghan/person/data0612/labeladd0524/rename0524/'
    srcXmlPath = '/home/zhanghan/person/data0612/labeladd0524/addxml0524/'
    dstImgPath = '/home/zhanghan/person/data0614/aug0524/img/'
    dstXmlPath = '/home/zhanghan/person/data0614/aug0524/xml/'
    files = os.listdir(srcImgPath)
    for f in files:
        if(random.random() < thresh):
            fname,pf = f.split('.')
            flipImg(srcImgPath + f,srcXmlPath + fname + '.xml',dstImgPath,dstXmlPath)
    print("done.")

if __name__ == '__main__':
    main()





