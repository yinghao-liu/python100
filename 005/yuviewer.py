#!/usr/bin/env python3
import cv2 as cv
import numpy as np
import argparse

g_color_map = {"I420":cv.COLOR_YUV2BGR_I420, "YV12":cv.COLOR_YUV2BGR_YV12, "NV12":cv.COLOR_YUV2BGR_NV12, "NV21":cv.COLOR_YUV2BGR_NV21}

def arg_parser():
    parser = argparse.ArgumentParser(description='view a yuv file, now only yuv420 are supported')
    parser.add_argument("-i", "--input", required=True, help="input file(yuv)")
    parser.add_argument("-w", "--width", help="width, default=1920")
    parser.add_argument("-e", "--height", help="height, default=1080")
    parser.add_argument("-c", "--color", help="color, now support only yuv420 format, include {}, default=yv12".format(g_color_map.keys()))
    args=parser.parse_args()
    return args

args = arg_parser()
file_name = args.input
width = 1920 if None == args.width else args.width
height = 1080 if None == args.height else args.height
color = "YV12" if args.color not in g_color_map.keys() else args.color
print("color format is {}".format(color))

with open(file_name, "rb") as fd:
    yuv_raw=fd.read()

if None == yuv_raw:
    print("with no data")
    exit(-1)

np_yuv=np.array(list(yuv_raw), dtype=np.uint8).reshape(int(height*1.5), width)
np_bgr=cv.cvtColor(np_yuv, g_color_map[color])
cv.imshow("YUV", np_yuv)
cv.imshow("BGR", np_bgr)
cv.waitKey()


