from utils import *
from createXML import createXML

import os
import cv2
import random
import numpy as np

thresh = 0.5
boundX = -40
boundY = -30

def translateImg(srcImg,srcXml,dstImgPath,dstXmlPath,mat):
    color = [0,0,0]
    rand = random.random()
    if(rand < 0.33):
        color = [128,128,128]
    elif(rand > 0.66):
        color = [255,255,255]
    
    name = srcImg.split('/')[-1]
    fname,pf = name.split('.')
    transX = int(mat[0][2])
    transY = int(mat[1][2])
    newFname = dstImgPath + fname + '_' + str(transX) + '_' + str(transY) + '_translate.jpg'
    newXMLname = dstXmlPath + fname + '_' + str(transX) + '_' + str(transY) + '_translate.xml'
    
    img = cv2.imread(srcImg)
    resultImg = cv2.warpAffine(img,mat,(img.shape[1],img.shape[0]),borderValue=(color[0],color[1],color[2]))
    cv2.imwrite(newFname,resultImg)

    newXML = createXML(srcXml)
    newXML.translate(newXMLname,mat)


def main():
    srcImgPath = '/home/zhanghan/person/data0612/labeladd0524/rename0524/'
    srcXmlPath = '/home/zhanghan/person/data0612/labeladd0524/addxml0524/'
    dstImgPath = '/home/zhanghan/person/data0614/aug0524/img/'
    dstXmlPath = '/home/zhanghan/person/data0614/aug0524/xml/'
    
    files = os.listdir(srcImgPath)
    for f in files:
        if(random.random() < thresh):
            fname,pf = f.split('.')
            transX = boundX + 2 * (0 - boundX) * random.random()
            transY = boundY + 2 * (0 - boundY) * random.random()
            mat = np.array([[1,0,round(transX)],[0,1,round(transY)]],np.float32)
            translateImg(srcImgPath + f,srcXmlPath + fname + '.xml',dstImgPath,dstXmlPath,mat)
    print("done.")


if __name__ == '__main__':
    main()

