import argparse

def parseArgs():
	parser = argparse.ArgumentParser(description='Process from geoTIFF')
	parser.add_argument('filename', metavar='T', type=str, nargs='+', help='a geoTIFF file for analysis')
	args = parser.parse_args()
	print args.accumulate(args.integers)
	
