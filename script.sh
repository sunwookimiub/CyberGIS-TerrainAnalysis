#!/usr/bin/env sh
#PBS -N output_qsub
#PBS -j oe

cd $PBS_O_WORKDIR
chmod +x terrain_main.py
module load anaconda
/usr/bin/mpirun -np $PBS_NP python terrain_main.py $inImg $outImg $p
