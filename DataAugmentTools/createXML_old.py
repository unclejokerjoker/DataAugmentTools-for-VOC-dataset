import xml.etree.ElementTree as ET
import os
from lxml.etree import Element,SubElement,ElementTree, tostring
from xml.dom.minidom import parseString

def readtxt(fname):
    with open(fname,'r') as f:
        lines = f.readlines()
        items = []
        for l in lines:
            item = l.split()
            if int(item[-1]) > 360:
                item[-1] = '360'
            if int(item[-2]) > 640:
                item[-2] = '640'
            if int(item[-3]) < 0:
                item[-3] = '0'
            if int(item[-4]) < 0:
                item[-4] = '0'
            items.append(item)
    return items


#fname: .txt
def writexml(fname,objects,savepath):
    name,posetfix = fname.split('.')

    node_root = Element('annotation')

    node_folder = SubElement(node_root,'folder')
    node_folder.text = 'VOC2007'

    node_filename = SubElement(node_root,'filename')
    #node_filename.text = '010001.jpg'
    node_filename.text = name + '.jpg'

    node_source = SubElement(node_root,'source')

    node_database = SubElement(node_source,'database')
    node_database.text = 'ISLAB'
    node_anno = SubElement(node_source,'annotation')
    node_anno.text = 'VOC2007'
    node_image = SubElement(node_source,'image')
    node_image.text = 'flickr'
    node_fli = SubElement(node_source,'flickrid')
    node_fli.text = 'NULL'

    node_owner = SubElement(node_root,'owner')
    node_fli2 = SubElement(node_owner,'flickrid')
    node_fli2.text = 'NULL'
    node_name = SubElement(node_owner,'name')
    node_name.text = 'zhanghan'

    node_size = SubElement(node_root,'size')

    node_width = SubElement(node_size,'width')
    node_height = SubElement(node_size,'height')
    node_depth = SubElement(node_size,'depth')
    node_width.text = '640'
    node_height.text = '360'
    node_depth.text = '3'

    node_object = SubElement(node_root,'object')

    for i in range(len(objects)):
        node_name = SubElement(node_object,'name')
        node_name.text = 'person'

        node_pose = SubElement(node_object,'pose')
        node_pose.text = 'Unspecified'

        node_truncated = SubElement(node_object,'truncated')
        node_truncated.text = '0'

        node_diff = SubElement(node_object,'difficult')
        node_diff.text = '0'

        node_bbox = SubElement(node_object,'bndbox')

        node_xmin = SubElement(node_bbox,'xmin')
        node_ymin = SubElement(node_bbox,'ymin')
        node_xmax = SubElement(node_bbox,'xmax')
        node_ymax = SubElement(node_bbox,'ymax')

        node_xmin.text = objects[i][3]
        node_ymin.text = objects[i][4]
        node_xmax.text = objects[i][5]
        node_ymax.text = objects[i][6]

    tree = ElementTree(node_root)
    #tree.write('010001.xml',pretty_print=True,xml_declaration=False)
    tree.write(savepath + name + '.xml',pretty_print=True,xml_declaration=False)

#with open('rename/txt/010001.txt','r') as f:
#objects = readtxt('rename/txt/010112.txt')
#writexml('010112.txt',objects)
#print(objects)
dstpath = '/home/zhanghan/person/data0329/rename/xml/'
srcpath = '/home/zhanghan/person/data0329/rename/txt/'

files = os.listdir(srcpath)
for f in files:
    objects = readtxt(srcpath + f)
    print(objects)
    writexml(f,objects,dstpath)
