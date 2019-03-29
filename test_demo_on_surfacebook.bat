@echo off

python scripts/demo_on_surfacebook.py ^
    --graph=retrain_results_ver4/graph.pb ^
    --labels=retrain_results_ver4/labels.txt ^
    --dir_video=videos_ver4 ^
    --f_img_steps=demo_img/steps.png

exit /B 0
