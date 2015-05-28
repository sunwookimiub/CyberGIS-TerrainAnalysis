## Terrain Analysis

To receive an image file as input from the user and to return a file of the equivalent format with values calculated by running the Evans-Young methods in parallel.

##### Running the program:

Run through a script for qsub, **script.sh**:

> qsub script.sh -v inImg=*a*,outImg=*b*,p=*c* -l nodes=*x*:ppn=*y*

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *a* = the name of input image

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *b* = the name of output image

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *c* = value of the pixel size

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *x* = number of nodes to be assigned

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *y* = number of ppn to be assigned

*(Note: number of nodes is the CPU Qty and number of ppn is Total Cores as listed in the [Roger Technical Summary page of the NCSA Wiki](https://wiki.ncsa.illinois.edu/display/ROGER/ROGER+Technical+Summary))*

#### For further information:
[Go to the CIGI Wiki](https://wiki.cigi.illinois.edu/display/UP/Parallel+Terrain+Analysis+on+DEMs)
