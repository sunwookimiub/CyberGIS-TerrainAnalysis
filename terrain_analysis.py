#!/usr/bin/env python
"""
Reads a raster input file with elevation data and produces a multi-band
raster output based on Evans-Young method.
"""
import argparse
import logging

from worker_run import *

def parseArguments():
    parser = argparse.ArgumentParser(
        usage = 'mpirun -np <procs> %s [options] input output' % __file__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__)

    parser.add_argument("input", type=str, 
        help="input raster file")
    parser.add_argument("output", type=str, 
        help="output raster file")
    parser.add_argument("--nodata", type=float,
        help="value for no data points (default=matches input file)")
    parser.add_argument("--band", type=int, default=1,
        help="input raster band (default=1)")
    parser.add_argument("-v", "--verbose",  action='store_true', default=False,
        help = "print progress related information")
    parser.add_argument("-d", "--debug", action='store_true', default=False,
        help = "print detailed debugging information")

    return parser.parse_args()


def main():
    args = parseArguments()

    if args.verbose:
        logging.basicConfig(level=logging.INFO, 
                format='%(asctime)s %(message)s',
                datefmt='%I:%M:%S')
    elif args.debug:
        logging.basicConfig(level=logging.DEBUG, 
                format='%(asctime)s %(message)s',
                datefmt='%I:%M:%S')
    else:
        logging.basicConfig(format='%(asctime)s %(message)s',
                datefmt='%I:%M:%S')

    run_mpi_jobs(args.input, args.output, args.nodata, args.band)


if __name__ == "__main__" :
    main()
