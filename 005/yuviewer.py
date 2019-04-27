#!/usr/bin/env python3
import cv2 as cv
import numpy as np

with open("ma420.yuv", "rb") as fd:
    yuv_raw=fd.read()

np_yuv=np.array(list(yuv_raw), dtype=np.uint8)
np_yuv420=np_yuv.reshape(1620, 1920)
bgr=cv.cvtColor(np_yuv420, cv.COLOR_YUV2BGR_YV12)
cv.imshow("YUV", np_yuv420)
cv.imshow("BGR", bgr)
cv.waitKey()


