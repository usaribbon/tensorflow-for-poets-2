#!/usr/bin/env python
# coding: utf-8

import sys
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
import argparse

def rename_image_files():
    
    return

def view_images(img_arr, f_name_bef_arr, f_name_aft_arr, n_rows=3, n_cols=4):
    n_imgs = len(img_arr)
    # プロット領域(Figure, Axes)の初期化
    fig = plt.figure(figsize=(25, 15))
    plt.title('Press Any Key to Close.')
    ax_list=[]
    for i in range(len(img_arr)):
        ax = fig.add_subplot(n_rows,n_cols,i+1)
        str_before='bef:'+f_name_bef_arr[i]
        str_after='aft:'+f_name_aft_arr[i]
        ax.text(img_arr[i].shape[1]*0.03, img_arr[i].shape[1]*0.1, str_before+'\n'+str_after, size=12, linespacing=1, backgroundcolor='white')
        ax.imshow(img_arr[i])
    plt.show()
    return

def get_renamed_arr():
    
    # 命名規則に沿って
    dst_arr=[]
    dst_arr.append()

def load_images(file_img_list):
    img_arr=[]
    for file_img in file_img_list:
        img = cv2.imread(file_img, cv2.IMREAD_UNCHANGED)
        img_arr.append(img)
    return img_arr


dir_in='./test_data'
f_name_bef_arr=os.listdir(dir_in)
f_name_aft_arr=[]
f_path_arr=[]
for f_name in f_name_bef_arr:
    f_path_arr.append(dir_in+'/'+f_name)
    f_name_aft_arr.append('str_after')
n_imgs = 10
loop_cnt = 0
while loop_cnt*n_imgs < len(f_name_bef_arr):
    img_arr = load_images(f_path_arr[loop_cnt*n_imgs:(loop_cnt+1)*n_imgs])
    f_name_aft_arr = get_renamed_arr()
    view_images(img_arr, f_name_bef_arr, f_name_aft_arr)
#     key = input('Press y to rename, or press n to end program.')
#     if key == 'y':
#         pass
#     if key == 'n':
#         break
    loop_cnt = loop_cnt+1
