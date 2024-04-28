#!/usr/bin/env bash
#SBATCH --job-name=check_pkg
#SBATCH --nodes=1
#SBATCH --mem=4096
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --time=12:00:00

# Set up environment
spack load python@3.11.6%gcc@7.3.1
source venv/bin/activate

# Define the maximum number of concurrent jobs
MAX_JOBS=25
job_count=0

while IFS= read -r pkg_name; do
    echo "Scanning package: $pkg_name"
    python -m guarddog npm scan "$pkg_name" &

    # Increment the job counter
    ((job_count++))
    
    # If the maximum number of jobs has been reached, wait for them to finish
    if [ $job_count -eq $MAX_JOBS ]; then        
        # Wait for all background jobs to complete
        wait
        # Reset the job counter
        job_count=0
    fi
done < $1

wait

# return the exit code of srun above
exit $?
