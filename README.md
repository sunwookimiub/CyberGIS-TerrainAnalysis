## Terrain Analysis

To receive an image file as input from the user and to return a file of the equivalent format with values calculated by running the Evans-Young methods in parallel.

##### Running the program:

Run through a script for qsub, **script.sh**:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;qsub script.sh -v inImg=*A*[,outImg=*B*,p=*C*] [-l nodes=*X*:ppn=*Y*]

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *A* = the name of input image

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *B* = the name of output image (Optional)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *C* = value of the pixel size (Optional)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *X* = number of nodes to be assigned (Optional)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *Y* = number of ppn to be assigned (Optional)

*(Note: number of nodes is the CPU Qty and number of ppn is Total Cores as listed in the [Roger Technical Summary page of the NCSA Wiki](https://wiki.ncsa.illinois.edu/display/ROGER/ROGER+Technical+Summary).)*

#### For further information:
[Go to the CIGI Wiki](https://wiki.cigi.illinois.edu/display/UP/Parallel+Terrain+Analysis+on+DEMs)
