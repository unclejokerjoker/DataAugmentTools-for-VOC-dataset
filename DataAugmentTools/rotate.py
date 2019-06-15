from utils import *
from createXML import createXML

import os
import cv2
import random

angle = 15#anti-clock 15°,if == -15,clock direction
thresh = 0.5

def rotateImg_old(img,angle,scale=1):
    center = (img.shape[1]//2,img.shape[0]//2)
    print(center)
    print(img.shape[:2])
    mat = cv2.getRotationMatrix2D(center,angle,scale)
    rand1 = random.random()
    rand2 = random.random()
    rand3 = random.random()
    resultImg = cv2.warpAffine(img,mat,(img.shape[1],img.shape[0]),borderValue=(int(rand1*255),int(rand2*255),int(rand3*255)))
    cv2.imwrite('rotatedimg.jpg',resultImg)

def rotateImg(srcImg,srcXml,dstImgPath,dstXmlPath,angle=15,offset=0.05):
    name = srcImg.split('/')[-1]
    fname,pf = name.split('.')
    newFname = dstImgPath + fname + '_' + str(angle) + '_rotate.jpg'
    newXMLname = dstXmlPath + fname + '_' + str(angle) + '_rotate.xml'
    
    img = cv2.imread(srcImg)
    center = (img.shape[1]//2,img.shape[0]//2)
    scale = 1
    color = [0,0,0]
    if(random.random() < 0.5):
        angle = -angle
    mat = cv2.getRotationMatrix2D(center,angle,scale)
    rand = random.random()
    if(rand < 0.33):
        color = [128,128,128]
    elif(rand > 0.66):
        color = [255,255,255]

    print("angle:",angle)
    resultImg = cv2.warpAffine(img,mat,(img.shape[1],img.shape[0]),borderValue=(color[0],color[1],color[2]))
    cv2.imwrite(newFname,resultImg)

    newXML = createXML(srcXml)
    newXML.rotate(newXMLname,center[0],center[1],angle,offset)

def main():
    #srcImgPath = '/home/zhanghan/person/data0612/labeladd0524/rename0524/'
    #srcXmlPath = '/home/zhanghan/person/data0612/labeladd0524/addxml0524/'
    srcImgPath = '/home/zhanghan/person/data0524/labelimg0524/rename/'
    srcXmlPath = '/home/zhanghan/person/data0524/labelimg0524/xml/'
    dstImgPath = '/home/zhanghan/person/data0614/aug0524/rotimg/'
    dstXmlPath = '/home/zhanghan/person/data0614/aug0524/rotxml/'
    
    files = os.listdir(srcImgPath)
    for f in files:
        if(random.random() < thresh):
            fname,pf = f.split('.')
            angle = round(5 + 10 * random.random())
            rotateImg(srcImgPath + f,srcXmlPath + fname + '.xml',dstImgPath,dstXmlPath,angle,0.05)
    print("done.")


if __name__ == '__main__':
    main()

