## Terrain Analysis

To receive an image file as input from the user and to return a file of the equivalent format with values calculated by running the Evans-Young methods in parallel.

###### Running the program:
1) Run through a python file *terrainanalysis.py*:

    a) Only specify the filename. The default value for the number of processes will be set to 40 and pixel size to 1
  > python terrainanalysis.py *filename*

or
> python terrainanalysis.py *filename*

2) Run through a script for qsub, *terrainanalysis.pbs*:
> qsub terrainanalysis.pbs -v np=x,filename=y,p=z

#### For further information:
[Go to the CIGI Wiki](https://wiki.cigi.illinois.edu/display/UP/Parallel+Terrain+Analysis+on+DEMs)
