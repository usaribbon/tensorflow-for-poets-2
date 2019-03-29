# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time

import numpy as np
import tensorflow as tf
import sys
import os

import cv2

def load_graph(model_file):
    graph = tf.Graph()
    graph_def = tf.GraphDef()

    with open(model_file, "rb") as f:
        graph_def.ParseFromString(f.read())
    with graph.as_default():
        tf.import_graph_def(graph_def)

    return graph

# def read_tensor_from_image_file(file_name, input_height=299, input_width=299, input_mean=0, input_std=255):
#     input_name = "file_reader"
#     output_name = "normalized"
#     file_reader = tf.read_file(file_name, input_name)
#     if file_name.endswith(".png"):
#         image_reader = tf.image.decode_png(file_reader, channels = 3, name='png_reader')
#     elif file_name.endswith(".gif"):
#         image_reader = tf.squeeze(tf.image.decode_gif(file_reader, name='gif_reader'))
#     elif file_name.endswith(".bmp"):
#         image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
#     else:
#         image_reader = tf.image.decode_jpeg(file_reader, channels = 3, name='jpeg_reader')
#     float_caster = tf.cast(image_reader, tf.float32)
#     dims_expander = tf.expand_dims(float_caster, 0)
#     resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
#     normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
#     sess = tf.Session()
#     result = sess.run(normalized)

#     return result

def load_labels(label_file):
    label = []
    proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
    for l in proto_as_ascii_lines:
        label.append(l.rstrip())
    return label

#
# 引数設定
#

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--graph", help="graph/model to be executed")
parser.add_argument("--labels", help="name of file containing labels")
parser.add_argument("--dir_video", help="name of directory containing video files")
parser.add_argument("--f_img_steps", help="where image describing steps is")
args = parser.parse_args()
model_file = args.graph
label_file = args.labels
dir_video = args.dir_video
f_img_steps = args.f_img_steps

#
# ネットワーク設定
#

input_height = 299
input_width = 299
input_mean = 128
input_std = 128
input_layer = "Mul"
output_layer = "final_result"

graph = load_graph(model_file)
# t = read_tensor_from_image_file(file_name,
#                                 input_height=input_height,
#                                 input_width=input_width,
#                                 input_mean=input_mean,
#                                 input_std=input_std)

input_name = "import/" + input_layer
output_name = "import/" + output_layer
input_operation = graph.get_operation_by_name(input_name)
output_operation = graph.get_operation_by_name(output_name)


#
#  ここからはデモ用プログラム
#

sess=tf.Session(graph=graph)

# カメラの初期設定
cam_v_cap = cv2.VideoCapture(0)
ret, cam_frame = cam_v_cap.read()
h_frame = cam_frame.shape[0] # カメラ画像の立幅の取得
w_frame = cam_frame.shape[1] # カメラ画像の横幅の取得

# ガイド画像
img_steps=cv2.imread(f_img_steps)
img_steps=cv2.resize(img_steps, (w_frame, h_frame))

while True:
    # カメラフレームの取得
    ret, cam_frame = cam_v_cap.read()
    # カメラフレームに対して円を真ん中に描画
    center = (cam_frame.shape[1]//2, cam_frame.shape[0]//2)
    circle_radius = int(cam_frame.shape[0]*0.35)
    circle_clr = (0,0,255)
    drawn_cam_frame=cam_frame.copy()
    drawn_cam_frame = cv2.circle(drawn_cam_frame, center, circle_radius, circle_clr, thickness=5, lineType=cv2.LINE_AA)
    # 説明テキストの描画
    font = cv2.FONT_HERSHEY_PLAIN
    text = '(q): Quit, (s): Shoot'
    white = (255,255,255)
    drawn_cam_frame=cv2.putText(drawn_cam_frame,text,(int(w_frame*0.05),int(h_frame*0.05)),font,1.5,white)
    # カメラフレームの描画
    cv2.imshow('DEMO', cv2.hconcat([drawn_cam_frame, img_steps]))

    # キー入力によるオプションの選択
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'): # 終了
        break
    if key & 0xFF == ord('s'): # 撮影し折り紙の状態を識別
        # 指定範囲の画像をクロップし，その画像に対してラベル付けする
        crop_size=int(h_frame*0.7)
        y_start=(h_frame-crop_size)//2
        y_end=y_start+crop_size
        x_start=(w_frame-crop_size)//2
        x_end=x_start+crop_size
        cropped_frame=cam_frame[y_start:y_end,x_start:x_end]
        cropped_frame=cv2.resize(cropped_frame, (input_width, input_height))
        #_=cv2.imwrite('tmp.png', cropped_frame)
        cropped_frame=(cropped_frame-input_mean)/input_std
        # (h,w,c)->(batch_size=1,h,w,c)
        t=np.expand_dims(cropped_frame, axis=0)
        # ネットワークの順伝播
        start = time.time()
        results = sess.run(output_operation.outputs[0], {input_operation.outputs[0]: t})
        end=time.time()
        results = np.squeeze(results)
        top_k = results.argsort()[:][::-1]
        labels = load_labels(label_file)

        print('\nEvaluation time (1-image): {:.3f}s\n'.format(end-start))
        template = "{} (score={:0.5f})"
        for i in top_k:
            print(template.format(labels[i], results[i]))

        # 再生する動画の決定
        best_label = labels[top_k[0]]
        video_names = os.listdir(dir_video)
        file_video = dir_video+'/dummy.mp4'
        for video_name in video_names:
            if video_name.startswith(best_label):
                file_video=dir_video+'/'+video_name

        # 現在の進捗度を示すガイド画像の生成
        drawn_img_steps=img_steps.copy()
        font = cv2.FONT_HERSHEY_PLAIN
        text = 'YOU\'RE HERE'
        red = (0,0,255)
        def get_loc_to_put_text(label_name):
            if   label_name == 'step00':
                return (int(w_frame*0.02),int(h_frame*0.435))
            elif label_name == 'step01':
                return (int(w_frame*0.26),int(h_frame*0.435))
            elif label_name == 'step02':
                return (int(w_frame*0.51),int(h_frame*0.435))
            elif label_name == 'step03':
                return (int(w_frame*0.76),int(h_frame*0.435))
            elif label_name == 'step04':
                return (int(w_frame*0.02),int(h_frame*0.93))
            elif label_name == 'step05':
                return (int(w_frame*0.26),int(h_frame*0.93))
            elif label_name == 'step06':
                return (int(w_frame*0.51),int(h_frame*0.93))
            elif label_name == 'step07':
                return (int(w_frame*0.76),int(h_frame*0.93))
            else:
                return None
        text_loc = get_loc_to_put_text(best_label)
        if text_loc is not None:
            drawn_img_steps=cv2.putText(drawn_img_steps,text,text_loc,font, 1.3,red,2)
        
        # 動画再生
        inst_v_cap = cv2.VideoCapture(file_video)
        loop_end = False
        while not loop_end:
            # 動画フレームの取得
            ret, video_frame = inst_v_cap.read()
            if ret:
                # 動画フレームのリサイズ
                video_frame = cv2.resize(video_frame, (w_frame, h_frame))
                font = cv2.FONT_HERSHEY_PLAIN
                text = '(q): Quit, (r): Repeat'
                white = (255,255,255)
                video_frame=cv2.rectangle(video_frame, (0, 0), (w_frame-1, int(h_frame*0.1)), (0, 0, 0), -1)
                video_frame=cv2.putText(video_frame,text,(int(w_frame*0.05),int(h_frame*0.05)),font, 1.5,white)
                # カメラフレームの描画
                cv2.imshow('DEMO', cv2.hconcat([video_frame, drawn_img_steps]))
                # 再生速度調整のため，毎フレーム10ms待つ
                key = cv2.waitKey(20)
            else:
                while True:
                    key = cv2.waitKey(1)
                    if key & 0xFF == ord('q'): # 終了
                        loop_end=True
                        break
                    if key & 0xFF == ord('r'): # もう一度再生
                        inst_v_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        break
        inst_v_cap.release()

print('DEMO FIN')

cam_v_cap.release()
cv2.destroyWindow('DEMO')

sess.close()
#cv2.destroyAllWindows()
