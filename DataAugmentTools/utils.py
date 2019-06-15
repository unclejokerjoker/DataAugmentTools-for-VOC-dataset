def computeIOU(rect1,rect2):
    #rect:xmin,ymin,xmax,ymax
    xOverlap = max(0,min(rect1[2],rect2[2]) - max(rect1[0],rect2[0]))
    yOverlap = max(0,min(rect1[3],rect2[3]) - max(rect1[1],rect1[1]))
    area1 = (rect1[2] - rect1[0]) * (rect1[3] - rect1[1])
    area2 = (rect2[2] - rect2[0]) * (rect2[3] - rect2[1])
    inter = xOverlap * yOverlap
    union = area1 + area2 - inter
    IOU = inter/union
    return IOU
