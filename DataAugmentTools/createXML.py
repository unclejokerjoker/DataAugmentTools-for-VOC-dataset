import xml.etree.ElementTree as ET
import os
from lxml import etree
from lxml.etree import Element,SubElement,ElementTree, tostring
from xml.dom.minidom import parseString
import numpy as np
import math

class createXML():
    def __init__(self,srcXML):
        #tree = ET.parse(srcXML)
        tree = etree.parse(srcXML)
        self.root = tree.getroot()
        owner = self.root.find('owner')
        owner.find('name').text = 'zhanghan'
    def crop(self,pointX,pointY,nW,nH,dst):
        size = self.root.find('size')
        size.find('width').text = str(nW)
        size.find('height').text = str(nH)
        for obj in self.root.iter('object'):
            print(obj.find('name').text)
            box = obj.find('bndbox')
            rect = []
            rect.append(int(box.find('xmin').text))
            rect.append(int(box.find('ymin').text))
            rect.append(int(box.find('xmax').text))
            rect.append(int(box.find('ymax').text))
            newRect = self.computeCropBox(rect,pointX,pointY,nW,nH)
            print(rect)
            print(newRect)
            box.find('xmin').text = str(newRect[0])
            box.find('ymin').text = str(newRect[1])
            box.find('xmax').text = str(newRect[2])
            box.find('ymax').text = str(newRect[3])

            newTree = ElementTree(self.root)
            newTree.write(dst,pretty_print=True,xml_declaration=False)
    
    def flip(self,dst):
        #Horizontal flip
        size = self.root.find('size')
        W = int(size.find('width').text)
        for obj in self.root.iter('object'):
            print(obj.find('name').text)
            box = obj.find('bndbox')
            rect = []
            rect.append(int(box.find('xmin').text))
            rect.append(int(box.find('ymin').text))
            rect.append(int(box.find('xmax').text))
            rect.append(int(box.find('ymax').text))

            #y' = y
            #x' = w - x
            tmp = rect[2]
            rect[2] = W - rect[0]
            rect[0] = W - tmp
            box.find('xmin').text = str(rect[0])
            box.find('ymin').text = str(rect[1])
            box.find('xmax').text = str(rect[2])
            box.find('ymax').text = str(rect[3])

            newTree = ElementTree(self.root)
            newTree.write(dst,pretty_print=True,xml_declaration=False)
    

    def rotate(self,dst,xr,yr,angle=15,offset=0.05):
        for obj in self.root.iter('object'):
            print(obj.find('name').text)
            box = obj.find('bndbox')
            rect = []
            rect.append(int(box.find('xmin').text))
            rect.append(int(box.find('ymin').text))
            rect.append(int(box.find('xmax').text))
            rect.append(int(box.find('ymax').text))
            newRect = self.computeRotateBox(rect,xr,yr,angle,offset)
            print(rect)
            print(newRect)

            box.find('xmin').text = str(newRect[0])
            box.find('ymin').text = str(newRect[1])
            box.find('xmax').text = str(newRect[2])
            box.find('ymax').text = str(newRect[3])

            newTree = ElementTree(self.root)
            newTree.write(dst,pretty_print=True,xml_declaration=False)

    
    def translate(self,dst,mat):
        for obj in self.root.iter('object'):
            print(obj.find('name').text)
            box = obj.find('bndbox')
            rect = []
            rect.append(int(box.find('xmin').text))
            rect.append(int(box.find('ymin').text))
            rect.append(int(box.find('xmax').text))
            rect.append(int(box.find('ymax').text))
            newRect = self.computeTranslateBox(rect,mat)
            print(rect)
            print(newRect)

            box.find('xmin').text = str(newRect[0])
            box.find('ymin').text = str(newRect[1])
            box.find('xmax').text = str(newRect[2])
            box.find('ymax').text = str(newRect[3])

            newTree = ElementTree(self.root)
            newTree.write(dst,pretty_print=True,xml_declaration=False)


    def computeCropBox(self,rect,pointX,pointY,nW,nH):
        newXmin = min(max(0,rect[0] - pointX),nW)
        newYmin = min(max(0,rect[1] - pointY),nH)
        newXmax = min(max(0,rect[2] - pointX),nW)
        newYmax = min(max(0,rect[3] - pointY),nH)
        newRect = [newXmin,newYmin,newXmax,newYmax]
        return newRect
        
    def computeRotateBox(self,rect,xr,yr,angle=15,offset=0.05):
        #nx   cos,-sin,xr(1-cos)+yrsin    x
        #ny = sin,cos, yr(1-cos)-xrsin  * y
        #1     0 , 0 ,        1           1

        ptl = np.array([rect[0],rect[1],1])
        ptr = np.array([rect[2],rect[1],1])
        pbl = np.array([rect[0],rect[3],1])
        pbr = np.array([rect[2],rect[3],1])
        Angle = -(angle/180 * math.pi)#注意opencv中的坐标轴方向，此处需加一个负号
        T = np.array([[math.cos(Angle),-math.sin(Angle),xr * (1 - math.cos(Angle)) + yr * math.sin(Angle)],
                        [math.sin(Angle),math.cos(Angle),yr * (1 - math.cos(Angle)) - xr * math.sin(Angle)],
                        [0,0,1]])
        #print(T)
        newptl = np.dot(ptl,T.T)
        newptr = np.dot(ptr,T.T)
        newpbl = np.dot(pbl,T.T)
        newpbr = np.dot(pbr,T.T)#transpose
        #print("p1:",newptl)
        #print("p2:",newptr)
        #print("p3:",newpbl)
        #print("p4:",newpbr)
        size = self.root.find('size')
        W = int(size.find('width').text)
        H = int(size.find('height').text)
        newXmin = min(newptl[0],min(newptr[0],min(newpbl[0],newpbr[0])))
        newYmin = min(newptl[1],min(newptr[1],min(newpbl[1],newpbr[1])))
        newXmax = max(newptl[0],max(newptr[0],max(newpbl[0],newpbr[0])))
        newYmax = max(newptl[1],max(newptr[1],max(newpbl[1],newpbr[1])))

        #print("coord1:",newXmin)
        #print("coord2:",newYmin)
        #print("coord3:",newXmax)
        #print("coord4:",newYmax)
        boxW = newXmax - newXmin
        boxH = newYmax - newYmin
        #scale the bbox by offset param
        newXmin = min(max(0,newXmin + offset * boxW),W)
        newYmin = min(max(0,newYmin + 0.4 * offset * boxH),H)
        #newYmin = min(max(0,newYmin),H)
        newXmax = min(max(0,newXmax - offset * boxW),W)
        newYmax = min(max(0,newYmax - 0.4 * offset * boxH),H)
        #newYmax = min(max(0,newYmax),H)
        newRect = [int(newXmin),int(newYmin),int(newXmax),int(newYmax)]
        return newRect

    def computeTranslateBox(self,rect,mat):
        ptl = np.array([rect[0],rect[1],1])
        pbr = np.array([rect[2],rect[3],1])
        T = np.row_stack((mat,[0,0,1]))
        print(T)
        newptl = np.dot(ptl,T.T)
        newpbr = np.dot(pbr,T.T)

        size = self.root.find('size')
        W = int(size.find('width').text)
        H = int(size.find('height').text)
        newXmin = min(max(0,newptl[0]),W)
        newYmin = min(max(0,newptl[1]),H)
        newXmax = min(max(0,newpbr[0]),W)
        newYmax = min(max(0,newpbr[1]),H)
        newRect = [int(newXmin),int(newYmin),int(newXmax),int(newYmax)]
        return newRect



