import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from colors import colors
import sys


def main():
	if len(sys.argv) != 2:
		print(f"{colors().RED}Error: you have to give a file as argument{colors().END}")
		exit()
	try:
		df = pd.read_csv(sys.argv[1])
	except:
		print(f"{colors().RED}Error: could not read file{colors().END}")
		exit()


	# drop index column
	df.drop(columns=['Index'], inplace=True)

	# drop non-numeric columns
	for column in df:
		if df[column].dtype.kind in 'biufc': # https://stackoverflow.com/a/38185438
			#print(df[column])
			continue
		else:
			df.drop(columns=[column], inplace=True)

	new_column_names = []
	i = 1
	for column in df:
		new_column_names.append("Feature " + str(i))
		i += 1
	df.columns = new_column_names
	
	# count, mean, std, min, 25%, 50%, 75%, max
	count = 0
	min = 0
	max = 0
	first_percentile = 0
	second_percentile = 0
	third_percentile = 0
	mean = 0
	std = 0
	for column in df:
		min = float(df[column][0])
		count = 0
		for value in df[column]:
			if value != "":
				count += 1 # this counts too many!
			if float(value) < min:
				min = float(value)
			if float(value) > max:
				max = float(value)
			# mean += col
			# std =
			# PERCENTILES HERE
		print(f"count: {count}, min: {min}, max: {max}")

			

	
	# print(df)
	print(df.describe()) # DESIRED END RESULT PART 1

if __name__ == '__main__':
    main()