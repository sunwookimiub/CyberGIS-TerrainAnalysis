#!/usr/bin/env sh
#PBS -N qsub_output
#PBS -j oe

cd $PBS_O_WORKDIR
chmod +x terrain_main.py
module load anaconda

outImg_="output_image.tif"
p_=0

if [ -n "$inImg" ]; then

    if ! [ -e $inImg ]; then
        echo "$inImg file does not exist."
    fi

    if [ -n "$outImg" ]; then outImg_=$outImg
    fi

    if [ -n "$p" ]; then p_=$p
    fi
    
else echo "Please input an input image file."
fi

/usr/bin/mpirun -np $PBS_NP python terrain_main.py $inImg $outImg_ $p_
