#!/bin/bash
#SBATCH --output=/net/acadia5a/data/ssun/HumanML3D/runserverlog/arrayJob_%A_%a.txt
#SBATCH --time=480:00:00
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1
#SBATCH --constraint="TITANXp|RTX2080Ti|TITANX"
#SBATCH --job-name=n
#SBATCH --array=0-31

# Total number of Sketchfab objects (you may need to adjust this)
TOTAL_OBJECTS=29229

# Number of objects to download per task
OBJECTS_PER_TASK=914

# Calculate start and end indices for this task
START_INDEX=$((SLURM_ARRAY_TASK_ID * OBJECTS_PER_TASK))
END_INDEX=$((START_INDEX + OBJECTS_PER_TASK))

# Ensure the last task doesn't go beyond the total number of objects
if [ $END_INDEX -gt $TOTAL_OBJECTS ]; then
    END_INDEX=$TOTAL_OBJECTS
fi

echo "Task ${SLURM_ARRAY_TASK_ID}: Preprocess scene $START_INDEX to $END_INDEX"

blender-2.93.17-linux-x64/blender --background --python \
    render2video.py -- --cfg=./configs/render.yaml --dir=/net/acadia5a/data/ssun/HumanML3D/new_joints/ \
    --start_idx $START_INDEX --end_idx $END_INDEX --mode=video