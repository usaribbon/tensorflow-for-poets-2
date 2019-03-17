#!/usr/bin/env python
# coding: utf-8

# In[1]:


# イメージが保管されているフォルダに保存し、実行してください。
#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os
import glob
import re
from PIL import Image

# 同一フォルダにあるファイル名を読み込み
files = glob.glob('./*.jpg')

# 横幅指定。入力がない場合は800
wsize = input('Image Width Size: ')
if wsize=='':
    wsize = 800
else:
    wsize = int(wsize)
    
# 指定された横幅に変換。outを先頭に付与してファイル出力
# なお縦横比率は維持
for f in files:
    img = Image.open(f)
    m = re.match('out', os.path.basename(f))
    if m != None:
        pass
    else:
        rate = wsize/img.width
        hsize = int(img.height*rate)
        img_resize = img.resize((wsize, hsize))
        imgdir = os.path.dirname(f)
        imgname = os.path.basename(f)
        newfname = imgdir + '/out_' + str(wsize) + 'x' + str(hsize) + '_' + imgname
        print(newfname)
        img_resize.save(newfname)


# In[ ]:




