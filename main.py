from PIL import ImageDraw,ImageFont,Image
import cv2
import numpy as np
import math
from multiprocessing import Pool

fileName="Chipi chipi chapa chapa cat.mp4"
chars = " .'`^\",:;Il!i><~+_-?][}{1)(|\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
charlist=list(chars)
charlen=len(charlist)
interval=charlen/256
scale_factor=0.08
charwidth=12
charheight=12
Font=ImageFont.truetype('C:\\Windows\\Fonts\\lucon.ttf',15)

def get_char(i):
    return charlist[math.floor(i*interval)]

def process_frame(img):
    img=Image.fromarray(img)
    width,height=img.size
    img=img.resize((int(scale_factor*width),int(scale_factor*height*(charwidth/charheight))),Image.NEAREST)
    width,height=img.size
    pixel=img.load()
    outputImage=Image.new("RGB",(charwidth*width,charheight*height),color=(0,0,0))
    dest=ImageDraw.Draw(outputImage)
    for i in range(height):
        for j in range(width):
            r,g,b=pixel[j,i]
            h=int(0.299*r+0.587*g+0.114*b)
            pixel[j,i]=(h,h,h)
            dest.text((j*charwidth,i*charheight),get_char(h),font=Font,fill=(r,g,b))
    return np.array(outputImage)

def main():
    cap=cv2.VideoCapture(fileName)

    pool = Pool() # creates a pool of process, controls worksers

    while True:
        _,img=cap.read()
        open_cv_image = pool.map(process_frame, [img]) # process each frame
        key=cv2.waitKey(1)
        if key == ord("q"):
            break
        cv2.imshow("AScii Art",open_cv_image[0]) # use the first item in the list
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
