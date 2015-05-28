## Terrain Analysis

To receive an image file as input from the user and to return a file of the equivalent format with values calculated by running the Evans-Young methods in parallel.

##### Running the program:
1) Run through a python file **terrainanalysis.py**:

 *(Note: If number of processes, np, or pixel size, p, is not specified, the default values will be set to 40 and 1 respectively.)*
  > python terrainanalysis.py *filename* [-np x] [-p y]

2) Run through a script for qsub, **terrainanalysis.pbs**:

*(Note: No default values are provided for filename, np, or p)*
> qsub terrainanalysis.pbs -v inImg=*a*,outImg=*b*,p=*c* -l nodes=*x*:ppn=*y*

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *a* = the name of input image

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *b* = the name of output image

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *c* = value of the pixel size

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *x* = number of nodes to be assigned

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *y* = number of ppn to be assigned

*(Note: number of nodes is the CPU Qty and number of ppn is Total Cores as listedinhttps://wiki.ncsa.illinois.edu/display/ROGER/ROGER+Technical+Summary) *

#### For further information:
[Go to the CIGI Wiki](https://wiki.cigi.illinois.edu/display/UP/Parallel+Terrain+Analysis+on+DEMs)
