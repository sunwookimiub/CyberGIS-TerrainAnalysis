## Terrain Analysis

To receive an image file as input from the user and to return a file of the equivalent format with values calculated by running the Evans-Young methods in parallel.

##### Running the program:
1) Run through a python file **terrainanalysis.py**:

 *(Note: If number of processes (np) or pixel size (p) is not specified, the default values will be set to 40 and 1 respectively.)*
  > python terrainanalysis.py *filename* [-np x] [-p y]

2) Run through a script for qsub, **terrainanalysis.pbs**:

*(Note: No default values are provided for filename, np, or p)*
> qsub terrainanalysis.pbs -v filename=*filename*,np=x,p=y

#### For further information:
[Go to the CIGI Wiki](https://wiki.cigi.illinois.edu/display/UP/Parallel+Terrain+Analysis+on+DEMs)
