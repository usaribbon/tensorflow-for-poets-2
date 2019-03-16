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
kabuto.ipynbに、以下と同様の手順がまとまっています。

#### 1. iLect上の任意のディレクトリにこのリポジトリをcloneします
```
git clone https://github.com/usaribbon/tensorflow-for-poets-2.git
```

#### 2.iLectでかぶとの折り紙の画像を学習させます
```
python3 scripts/retrain.py --output_graph=tf_files/retrained_graph.pb --output_labels=tf_files/retrained_labels.txt --image_dir=tf_files/kabuto
```

#### 3.学習したモデルで折り紙の手順番号を予測し、次のステップ動画を再生します  
iLectでは動画再生できないため、OpenCV対応の環境で以下のスクリプト実行してください。
例）08ステップ目の画像
```
python3 scripts/label_image.py --image tf_files/answer/08_answer.jpeg
```

# 参考URL
* https://towardsdatascience.com/training-inception-with-tensorflow-on-custom-images-using-cpu-8ecd91595f26

# そのた
* See original README -> README.md.org
