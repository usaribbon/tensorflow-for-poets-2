@echo off

python scripts/demo_on_surfacebook.py ^
    --graph=retrain_results/graph.pb ^
    --labels=retrain_results/labels.txt ^
    --dir_video=videos

exit /B 0
