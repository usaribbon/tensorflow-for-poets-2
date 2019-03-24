@echo off

set output_dir=retrain_results_2
if not exist %output_dir%\ (
    md %output_dir%
)

python scripts/retrain.py ^
    --image_dir=C:/Users/chekolart/Desktop/kabuto_dataset/500x500 ^
    --output_graph=%output_dir%/graph.pb ^
    --output_labels=%output_dir%/labels.txt ^
    --intermediate_output_graphs_dir=%output_dir%/intermediate_graphs/ ^
    --summaries_dir=%output_dir%/tensorboard_logs ^
    --random_crop=8 ^
    --intermediate_store_frequency=100 ^
    --how_many_training_steps=1000 ^
    --random_brightness=12 ^
    --random_scale=8 ^
    --flip_left_right ^
    --print_misclassified_test_images ^
    --architecture=inception_v3

exit /B 0
