import xml.etree.ElementTree as ET
import os
from lxml import etree
from lxml.etree import Element,SubElement,ElementTree, tostring
from xml.dom.minidom import parseString
import numpy as np
import cv2

def label(srcImgPath,srcXmlPath,dstImgPath):
    name = srcImgPath.split('/')[-1]
    fname,pf = name.split('.')
    newFname = dstImgPath + fname + '_label.jpg'

    img = cv2.imread(srcImgPath)
    tree = etree.parse(srcXmlPath)
    root = tree.getroot()
    for obj in root.iter('object'):
        print(obj.find('name').text)
        box = obj.find('bndbox')
        rect = []
        rect.append(int(box.find('xmin').text))
        rect.append(int(box.find('ymin').text))
        rect.append(int(box.find('xmax').text))
        rect.append(int(box.find('ymax').text))
        cv2.rectangle(img,(rect[0],rect[1]),(rect[2],rect[3]),(255,0,0),1)
    cv2.imwrite(newFname,img)

def main():
    srcImgPath = '/home/zhanghan/person/data0614/aug0524/img/'
    srcXmlPath = '/home/zhanghan/person/data0614/aug0524/xml/'
    dstImgPath = '/home/zhanghan/person/data0614/aug0524/labeledimg/'

    files = os.listdir(srcImgPath)
    for f in files:
        fname,pf = f.split('.')
        label(srcImgPath + f,srcXmlPath + fname + '.xml',dstImgPath)
    print("done.")

if __name__ == '__main__':
    main()
