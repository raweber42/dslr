import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from colors import colors
import sys
import math


def rename_columns(df):
	new_column_names = []
	i = 1
	for column in df:
		if column == "Index":
			new_column_names.append("Index")
		else:
			new_column_names.append("Feature " + str(i))
			i += 1
	df.columns = new_column_names


def arrange_columns(df):
	# drop non-numeric columns
	for column in df:
		if df[column].dtype.kind in 'biufc': # https://stackoverflow.com/a/38185438
			continue
		else:
			df.drop(columns=[column], inplace=True)


def calculate_percentiles(df, column, count):
	percentile_count = 0
	for value in df[column]:
		if math.isnan(value) == False:
			percentile_count += 1
		else:
			value = 0
		
		# linear interpolation: i + (j - i) * fraction, where fraction is the fractional part of the index surrounded by i and j.
		if percentile_count == round(count * 0.25):
			first_percentile = value
		if not ((count - 1) * 0.25).is_integer():
			if percentile_count == round(count * 0.25) + 1:
				first_percentile = first_percentile + ((value - first_percentile) * (((count - 1) * 0.25) - math.floor((count - 1) * 0.25)))

		if percentile_count == round(count * 0.5):
			second_percentile = value
		if not ((count - 1 * 0.5)).is_integer():
			if percentile_count == round(count * 0.5) + 1:
				second_percentile = second_percentile + ((value - second_percentile) * (((count - 1) * 0.5) - math.floor((count - 1) * 0.5)))

		if percentile_count == round(count * 0.75):
			third_percentile = value
		if not ((count - 1) * 0.75).is_integer():
			if percentile_count == round(count * 0.75) + 1:
				third_percentile = third_percentile + ((value - third_percentile) * (((count - 1) * 0.75) - math.floor((count - 1) * 0.75)))
				break
	return (first_percentile, second_percentile, third_percentile)


def calculate_standard_deviation(df, column, mean, count):
	std = 0
	for value in df[column]:
		if math.isnan(value) == True:
			continue
		std += (float(value) - mean) ** 2
	
	std /= (count - 1)
	std = math.sqrt(std)
	return (std)


def main():
	if len(sys.argv) != 2:
		print(f"{colors().RED}Error: you have to give a file as argument{colors().END}")
		exit()
	try:
		df = pd.read_csv(sys.argv[1])
		original_df = pd.read_csv(sys.argv[1])
	except:
		print(f"{colors().RED}Error: could not read file{colors().END}")
		print(sys.argv[1])
		exit()

	arrange_columns(df)
	rename_columns(df)
	
	count_array = []
	count = 0
	min_array = []
	min = 0
	max_array = []
	max = 0
	mean_array = []
	mean = 0.0
	std_array = []
	first_perc_array = []
	second_perc_array = []
	third_perc_array = []

	for column in df:
		# sort column ascending for percentiles
		df.sort_values(by=[column], inplace=True)
		
		count = 0.0
		mean = 0.0
		max = 0
		std = 0

		for value in df[column]:
			if math.isnan(value) == False:
				count += 1
				if count == 1:
					min = value
					max = value
				if value < min:
					min = value
				if value > max:
					max = value
			else:
				value = 0			
			mean = mean + value
		
		mean = mean / count

		std = calculate_standard_deviation(df, column, mean, count)
		first_percentile, second_percentile, third_percentile = calculate_percentiles(df, column, count)

		count_array.append(count)
		mean_array.append(mean)
		min_array.append(min)
		max_array.append(max)
		std_array.append(std)
		first_perc_array.append(first_percentile)
		second_perc_array.append(second_percentile)
		third_perc_array.append(third_percentile)

	# print out results
	print_table = []
	print_table.append(count_array)
	print_table.append(mean_array)
	print_table.append(std_array)
	print_table.append(min_array)
	print_table.append(first_perc_array)
	print_table.append(second_perc_array)
	print_table.append(third_perc_array)
	print_table.append(max_array)

	print_df = pd.DataFrame(print_table, columns = df.columns, index=['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max'])
	print(f"\n{colors().BLUE}", print_df, f"{colors().END}")

	# DESIRED END RESULT PART 1
	print("\nDESIRED RESULT: \n\n", original_df.describe(), "\n")

if __name__ == '__main__':
    main()