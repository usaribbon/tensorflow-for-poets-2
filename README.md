# Overview
tensorflowが提供している、画像認識モデルのサンプルを使って  
かぶとの折り紙が何番目の手順かを当てます。

# ファイルの説明
よく使うスクリプトと画像は以下です。
```
.
├── scripts
│   ├── label_image.py -> 順番予測スクリプト
│   └── retrain.py     -> モデル学習スクリプト
├── tf_files
│   └── kabuto         -> かぶとの画像
```

# 実行
iLectのコンソールで実行してください。

1. iLect上の任意のディレクトリにこのリポジトリをcloneします
```
git clone https://github.com/usaribbon/tensorflow-for-poets-2.git
```

2.かぶとの折り紙の画像を学習させます
```
python3 scripts/retrain.py --output_graph=tf_files/retrained_graph.pb --output_labels=tf_files/retrained_labels.txt --image_dir=tf_files/kabuto
```

3.学習したモデルで折り紙の手順番号を当ててみます
例）10ステップ目の画像
```
python3 scripts/label_image.py --image tf_files/answer/10_answer.jpeg
```

4.予測結果
2番目とでたので改良の余地あり...
```
2019-03-15 12:10:24.580165: I tensorflow/core/platform/cpu_feature_guard.cc:137] Your CPU supports instructions that this TensorFlow binary was not compiled to use: SSE4.1 SSE4.2 AVX
2019-03-15 12:10:24.686310: I tensorflow/stream_executor/cuda/cuda_gpu_executor.cc:892] successful NUMA node read from SysFS had negative value (-1), but there must be at least one NUMA node, so returning NUMA node zero
2019-03-15 12:10:24.686605: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1030] Found device 0 with properties:
name: GRID K520 major: 3 minor: 0 memoryClockRate(GHz): 0.797
pciBusID: 0000:00:03.0
totalMemory: 3.94GiB freeMemory: 3.90GiB
2019-03-15 12:10:24.686658: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1120] Creating TensorFlow device (/device:GPU:0) -> (device: 0, name: GRID K520, pci bus id: 0000:00:03.0, compute capability: 3.0)
2019-03-15 12:10:24.982714: I tensorflow/core/common_runtime/gpu/gpu_device.cc:1120] Creating TensorFlow device (/device:GPU:0) -> (device: 0, name: GRID K520, pci bus id: 0000:00:03.0, compute capability: 3.0)
2019-03-15 12:10:25.365768: W tensorflow/core/framework/op_def_util.cc:334] Op BatchNormWithGlobalNormalization is deprecated. It will cease to work in GraphDef version 9. Use tf.nn.batch_normalization().

Evaluation time (1-image): 1.530s

02 (score=0.66252)
01 (score=0.18554)
09 (score=0.08829)
10 (score=0.02805)
03 (score=0.01287)
```

# 参考URL
* https://towardsdatascience.com/training-inception-with-tensorflow-on-custom-images-using-cpu-8ecd91595f26

# そのた
* See original README -> README.md.org
