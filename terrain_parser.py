import sys
import os
import textwrap
import argparse
import subprocess


def main():
    parser = argparse.ArgumentParser(
		usage = '%(prog)s [-np numberOfProcesses] [-p gridSize] filename',
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

    parser.add_argument("filename", type=str, help="name of the file need to be analysed" )
    parser.add_argument("-np", "--numberOfProcess", type=int, help="number of process, default value is 40")
    parser.add_argument("-p", "--gridSize", type=float, help="parameter p, default value is retrived from datafile")
    args = parser.parse_args()

    # default value for number of process is 40 default value of p is dependent on data file
    np = 40
    p = 0
    # update arguments
    if args.numberOfProcess:
        np = args.numberOfProcess
    if args.gridSize:
        p = args.gridSize
  
    # construct system call
    mpirun = os.environ.get('MPIRUN', 'mpirun')
    sys_call = '{0} -np {1} python young.py {2}'.format(mpirun, np, p)

    subprocess.call([sys_call], shell = True)

if __name__ == ("__main__"):
    main()

