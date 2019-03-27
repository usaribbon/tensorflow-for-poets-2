@echo off

set image_dir=C:/Users/chekolart/Desktop/kabuto_dataset/500x500_ver3
set graph=retrain_results_ver3/graph.pb

python scripts/evaluate.py %graph% %image_dir%

exit /B 0
