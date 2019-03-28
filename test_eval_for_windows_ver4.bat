@echo off

set image_dir=dataset/500x500_ver4
set graph=retrain_results_ver4/graph.pb

python scripts/evaluate.py %graph% %image_dir%

exit /B 0
