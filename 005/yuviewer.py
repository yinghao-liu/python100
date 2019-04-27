#!/usr/bin/env python3
import cv2 as cv
import numpy as np

file_name="ma420.yuv"
width=1920
height=1080

with open(file_name, "rb") as fd:
    yuv_raw=fd.read()

if None == yuv_raw:
    print("with no data")
    exit(-1)
np_yuv=np.array(list(yuv_raw), dtype=np.uint8).reshape(int(height*1.5), width)
np_bgr=cv.cvtColor(np_yuv, cv.COLOR_YUV2BGR_YV12)
cv.imshow("YUV", np_yuv)
cv.imshow("BGR", np_bgr)
cv.waitKey()


