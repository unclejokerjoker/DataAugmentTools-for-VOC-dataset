Data Augment Tools for VOC dataset

Note that you should modify the paths to save the cropped images and the xml files in each python scripts.
1.Crop
Run 'python crop.py' to randomly crop images.
You can specify the width and height of the cropped images and the default width and height are set 400x300.
And you should be careful that cropped image should be smaller than the original image.
The default thresh is 0.4.You can modify this value to determine how much of the total number of the images are cropped.
The defalut N is 2.It means that one image will randomly generate N cropped images.

2.Flip
Run 'python flip.py' to randomly flip images in a horizontal direction.
The default thresh is 0.4.You can modify this value to determine how much of the total number of the images are flipped.

3.Rotate
Run 'python rotate.py' to randomly rotate images by a random angle.
The default thresh is 0.4.You can modify this value to determine how much of the total number of the images are rotated.
The default angle range is [5,15].It is declared in this line:
60             angle = round(5 + 10 * random.random())
So you can specify the angle range on your own. 
Note that the center of the rotation is the center of the image.

4.Translate
Run 'python translate.py' to randomly translate images by a random offset.
The default thresh is 0.5.You can modify this value to determine how much of the total number of the images are translated.
The default range of the offset in X and Y direction is decided by the param boundX and boundY,which is [-40,40] and [-30,30].

5.Label the image and Check
Run 'python labelXML.py' to label the images with bounding boxes which is given by its xml files.This script helps you label
the images with its xml files and save the labeled images.So you can use these labeled images to check if the data augmentation 
above is correct.
