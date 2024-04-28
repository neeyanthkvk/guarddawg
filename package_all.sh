#!/usr/bin/env bash

files=(xaa xab xac xad xae xaf xag xah xai xaj xak xal xam xan xao xap xaq xar xas xat)

for k in "${files[@]}"; do
  sbatch package_job.sh ./data/$k
done

# return the exit code
exit $?
