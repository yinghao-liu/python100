#!/usr/bin/env python3
import cv2 as cv

np_bgr=cv.imread("jack.jpg")
np_yuv=cv.cvtColor(np_bgr, cv.COLOR_BGR2YUV_YV12)
np_yuv.tofile("ma420.yuv")

