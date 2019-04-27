#!/usr/bin/env python3
import cv2 as cv
import argparse

def arg_parser():
    parser = argparse.ArgumentParser(description='image to yuv')
    parser.add_argument("-i", "--input", required=True, help="image input file")
    parser.add_argument("-o", "--output", required=True, help="output yuv file")
    args=parser.parse_args()
    return args

args = arg_parser()

file_jpg = args.input
file_yuv = args.output
if None == file_jpg or None == file_yuv:
    print("wrong data")
    print("file_jpg:{}".format(file_jpg))
    print("file_yuv:{}".format(file_yuv))
    exit(-1)
np_bgr = cv.imread(file_jpg)
np_yuv = cv.cvtColor(np_bgr, cv.COLOR_BGR2YUV_YV12)
np_yuv.tofile(file_yuv)

