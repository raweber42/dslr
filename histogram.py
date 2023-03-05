import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from colors import colors
import sys
import math


def main():
	try:
		df = pd.read_csv("datasets/dataset_train.csv")
	except:
		print(f"{colors().RED}Error: could not read file{colors().END}")
		exit()
	
	
	#https://mode.com/example-gallery/python_histogram/
	# df.hist(column='Hogwarts House')
	# hist = df.hist(column='Arithmancy')
	# hist = df.hist()


if __name__ == '__main__':
    main()