import argparse
import textwrap
from worker_run import *

def parseArguments():
    parser = argparse.ArgumentParser( \
        usage = 'qsub script.sh -v inImg=a[,outImg=b,p=c] [-l nodes=x:ppn=y]',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
                        Program Description
                        -----------------------------------------
                        To receive an image file as input
                        from the user and to return a file of the
                        equivalent format with values calculated
                        by running the Evans-Young methods in
                        parallel.
            '''))

    parser.add_argument("inImg", type=str, help="Name of the file need to be analysed")
    parser.add_argument("outImg_", type=str, help="Name of the output file. Default value: output_image.tif")
    parser.add_argument("p_", type=int, help="Pixel size. Default value: pixel size of the given input image")
    parser.add_argument("-l", help= "nodes=Number of Nodes:ppn=Number of ppn")
    return parser.parse_args()

if __name__ == ("__main__") :
    args = parseArguments()
    run_mpi_jobs(args.inImg, args.p_, args.outImg_)
