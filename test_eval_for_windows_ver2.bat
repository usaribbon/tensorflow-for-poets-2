@echo off

set image_dir=dataset/500x500_ver2
set graph=retrain_results_ver2/graph.pb

python scripts/evaluate.py %graph% %image_dir%

exit /B 0
