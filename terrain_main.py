import sys
from worker_run import *

def main():
	file = sys.argv[1]
	p = float(sys.argv[2])
	run_mpi_jobs(file, p)
	
if __name__ == ("__main__") :
	main()
