#!/usr/bin/env python3
import cv2 as cv

file_jpg="jack.jpg"
file_yuv="ma420.yuv"
np_bgr=cv.imread(file_jpg)
np_yuv=cv.cvtColor(np_bgr, cv.COLOR_BGR2YUV_YV12)
np_yuv.tofile(file_yuv)

