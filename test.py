from mpi4py import MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_rank()
name = MPI.Get_processor_name()

print("Rank:%d, Size:%d, Name:%s" % (rank,size,name))
