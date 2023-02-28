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
	print(df)






	#print(df.describe()) # DESIRED END RESULT PART 1

if __name__ == '__main__':
    main()