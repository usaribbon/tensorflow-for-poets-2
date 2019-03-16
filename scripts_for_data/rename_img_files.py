import sys
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

# 画像名の変更
def rename_image_files(f_path_bef_arr, f_path_aft_arr):
    map(os.rename, f_path_bef_arr, f_path_aft_arr)
    return

# 確認用の画像閲覧
def view_images(img_arr, f_name_bef_arr, f_name_aft_arr):
    n_imgs = len(img_arr)
    # プロット領域(Figure, Axes)の初期化
    fig = plt.figure(figsize=(18, 5))
    #plt.title('Press Any Key to Close.')
    ax_list=[]
    n_cols = 5
    n_rows = int(np.ceil(n_imgs/n_cols))
    for i in range(len(img_arr)):
        ax = fig.add_subplot(n_rows,n_cols,i+1)
        str_before='bef:'+f_name_bef_arr[i]
        str_after='aft:'+f_name_aft_arr[i]
        ax.text(img_arr[i].shape[1]*0.03, img_arr[i].shape[1]*0.1, str_before+'\n'+str_after, size=12, linespacing=1, backgroundcolor='white')
        ax.imshow(img_arr[i])
    plt.show()
    #plt.waitforbuttonpress(0) # this will wait for indefinite time

    return

# 命名規則にのっとった名前に変更
def get_renamed_arr(cnt, step, f_type='png'):
    dst_arr=[]
    member_id = 'A'
    str_cnt = str(cnt).zfill(3)
    str_step = str(step).zfill(3)+'00'
    directions = ['center', 'left', 'right', 'above', 'bottom']
    for direction in directions:
        f_name = member_id+'_'+str_cnt+'_'+str_step+'_'+direction
        f_name = f_name + '.' + f_type
        dst_arr.append(f_name)
    return dst_arr

# 画像群ロード
def load_images(file_img_list):
    img_arr=[]
    for file_img in file_img_list:
        img = cv2.imread(file_img, cv2.IMREAD_UNCHANGED)
        img_arr.append(img)
    return img_arr

# main

dir_in='./test_data'
dir_out='./test_data_out'
if not os.path.exists(dir_out):
    os.mkdir(dir_out)
f_name_bef_arr=os.listdir(dir_in)
# 変更後の名前リストの取得
f_name_aft_arr = get_renamed_arr(0,0)
n_imgs = len(f_name_aft_arr)
loop_cnt = 0
while loop_cnt*n_imgs < len(f_name_bef_arr):
    # 変更する画像リストの取得
    f_path_bef_arr=[]
    for f_name in f_name_bef_arr:        
        f_path_bef_arr.append(os.path.join(dir_in,f_name))
    img_arr = load_images(f_path_bef_arr[loop_cnt*n_imgs:(loop_cnt+1)*n_imgs])
    # 画像リストの表示
    view_images(img_arr, f_name_bef_arr, f_name_aft_arr)
    # 変更するのかの決定（Yならば変更，それ以外のキーをたたいた場合，プログラムを止める）
    key = input('Press y to rename, or other key to end program.')
    if key == 'y':
        f_path_aft_arr=[]
        for f_name in f_name_aft_arr:
            f_path_aft_arr.append(os.path.join(dir_out, f_name))
            #rename_image_files(f_path_bef_arr, f_path_aft_arr)
    else:
        break
    loop_cnt = loop_cnt+1
