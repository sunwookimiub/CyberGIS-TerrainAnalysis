from evansyoung_methods import *
import argparse

def main():
	parser = argparse.ArgumentParser(description='Process from geoTIFF')
	parser.add_argument('filename', metavar='T', type=str, nargs='+', help='a geoTIFF file for analysis')
	args = parser.parse_args()
	print args.accumulate(args.integers)
	
if __name__ == ("__main__") :
	main()
