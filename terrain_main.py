import sys
from worker_run import *

def main():
	file = sys.argv[1]
	output=sys.argv[2]
	p = float(sys.argv[3])
	run_mpi_jobs(file, p, output)
	
if __name__ == ("__main__") :
	main()
