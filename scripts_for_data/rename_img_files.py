import sys
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt
import shutil

# 画像名の変更
def rename_image_files(f_path_bef_arr, f_path_aft_arr):
    #map(os.rename, f_path_bef_arr, f_path_aft_arr)
    #map(shutil.copy2, f_path_bef_arr, f_path_aft_arr)
    for f_path_bef, f_path_aft in zip(f_path_bef_arr, f_path_aft_arr):
        print('f_path_bef: '+f_path_bef)
        print('f_path_aft: '+f_path_aft)
        shutil.copy2(f_path_bef, f_path_aft)
    return

# 確認用の画像閲覧
def view_images(img_arr, f_name_bef_arr, f_name_aft_arr):
    n_imgs = len(img_arr)
    # プロット領域(Figure, Axes)の初期化
    #plt.title('Press Any Key to Close.')
    ax_list=[]
    n_cols = 5
    n_rows = int(np.ceil(n_imgs/n_cols))
    fig = plt.figure(figsize=(5*n_cols, 2*n_rows))

    for i in range(len(img_arr)):
        ax = fig.add_subplot(n_rows,n_cols,i+1)
        str_before='before:'+f_name_bef_arr[i]
        str_after='after:'+f_name_aft_arr[i]
        ax.text(img_arr[i].shape[1]*0.03, img_arr[i].shape[1]*0.1, str_before+'\n'+str_after, size=9, linespacing=1, backgroundcolor='white')
        ax.imshow(img_arr[i])
    plt.show()
    #plt.waitforbuttonpress(0) # this will wait for indefinite time

    return

# 変更後の名前を含むリストの作成
def get_renamed_arr(member_id, cnt, f_type):
    dst_arr=[]
    str_cnt = str(cnt).zfill(3)
    for i in range(8):
        step = i+1
        str_step = str(step).zfill(3)+'00'
        directions = ['1_center', '2_above', '3_bottom', '4_left', '5_right']
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

# 入力画像データの入っているフォルダパス
dir_in='C:/Users/chekolart/Desktop/origami_dataset/set_010-014'
# 出力画像データを置くフォルダパス
dir_out='C:/Users/chekolart/Desktop/origami_dataset/set_010-014_renamed'
# メンバーのID
member_id='A'
# 扱う画像ファイルの形式
img_type='jpg'
# 表示フラグ
view_flag=False

# 出力フォルダがないなら作成する
if not os.path.exists(dir_out):
    os.mkdir(dir_out)
# 入力画像ファイル名のリスト作成
f_name_bef_arr=os.listdir(dir_in)
f_name_bef_arr.sort() # 名前順にソート
# 入力画像ファイルパスのリスト作成
f_path_bef_arr=[]
for f_name in f_name_bef_arr:
    if f_name.endswith(img_type):
        f_path_bef_arr.append(os.path.join(dir_in,f_name))
# ループごとで1セット分の画像データの名前を変更する
loop_cnt = 0
while True:
    # 変更後の名前リストの取得
    f_name_aft_arr = get_renamed_arr(member_id=member_id,cnt=loop_cnt+1,f_type=img_type)
    n_imgs = len(f_name_aft_arr)
    if loop_cnt*n_imgs >= len(f_name_bef_arr):
        break
    sliced_f_path_arr=f_path_bef_arr[loop_cnt*n_imgs:(loop_cnt+1)*n_imgs]
    img_arr = load_images(sliced_f_path_arr)
    # 画像リストの表示
    sliced_f_name_arr=f_name_bef_arr[loop_cnt*n_imgs:(loop_cnt+1)*n_imgs]
    if view_flag == True:
        view_images(img_arr, sliced_f_name_arr, f_name_aft_arr)
        # 変更するのかの決定（Yならば変更，それ以外のキーをたたいた場合，プログラムを止める）
        key = input('Press y to rename, or other key to end program.')
    if view_flag==False or key == 'y':
        f_path_aft_arr=[]
        for f_name in f_name_aft_arr:
            f_path_aft_arr.append(os.path.join(dir_out, f_name))
        rename_image_files(sliced_f_path_arr, f_path_aft_arr)
    else:
        break
    loop_cnt = loop_cnt+1
