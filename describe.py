import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from colors import colors
import sys
import math

def main():
	if len(sys.argv) != 2:
		print(f"{colors().RED}Error: you have to give a file as argument{colors().END}")
		exit()
	try:
		df = pd.read_csv(sys.argv[1])
	except:
		print(f"{colors().RED}Error: could not read file{colors().END}")
		print(sys.argv[1])
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
	mean = 0.0
	std = 0.0
	for column in df:
		count = 0.0
		mean = 0.0
		min = float(df[column][0])
		max = 0
		std = 0
		first_percentile = 0
		second_percentile = 0
		third_percentile = 0
		
		# sort column ascending for percentiles
		df.sort_values(by=[column], inplace=True)
			

		for value in df[column]:
			if math.isnan(value) == False:
				count += 1 # this counts also empty values!
			else:
				value = 0
			# if count == n * 0.25:
			# 	first_percentile = value
			# elif count == n * 0.5:
			# 	second_percentile = value
			# elif count == n * 0.75:
			# 	third_percentile = value
			if float(value) < min:
				min = float(value)
			if float(value) > max:
				max = float(value)
			mean = mean + float(value)
		
		# print(f"MEAN inner: {mean}, value: {float(value)}, count: {count}")
		mean = mean / count

		# second round for std and the percentiles
		for value in df[column]:
			if math.isnan(value) == True:
				value = 0
			std += (float(value) - mean) ** 2
		
		std /= (count - 1)
		std = math.sqrt(std)
	
		percentile_count = 0
		for value in df[column]:
			if math.isnan(value) == False:
				percentile_count += 1
			else:
				value = 0
			
			# WARNING: check again, what happens if percentile is EXACTLY the index
			
			# linear interpolation: i + (j - i) * fraction, where fraction is the fractional part of the index surrounded by i and j.
			if percentile_count == round(count * 0.25):
				first_percentile = value
			print((count * 0.25), (count * 0.25).is_integer())
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
					break #nothing more to do

	print(f"first percentile: {first_percentile:.6f}, second percentile: {second_percentile:.6f}, third_percentile: {third_percentile:.6f}")
	print(f"count: {count:.6f}, min: {min:.6f}, max: {max:.6f}, mean: {mean:.6f}, std: {std:.6f}")

		# check std of first Feature again!
		
			
 

# Step 1: Arrange all data values in the data set in ascending order.
# Step 2: Count the number of values in the data set where it is represented as 'n'.
# Step 3: calculate the value of k/100, where k = any number between zero and one hundred.
# Step 4: Multiply 'k' percent by 'n'.The resultant number is called an index.
# Step 5: If the resultant index is not a whole number then round to the nearest whole number, then go to Step 7. If the index is a whole number, then go to Step 6. 
# Step 6: Count the values in your data set from left to right until you reach the number. Then find the mean for that corresponding number and the next number. The resultant value is the kth percentile of your data set. 
# Step 7: Count the values in your data set from left to right until you reach the number. The obtained value will be the kth percentile of your data set.


			

	
	# print(df)
	print(df.describe()) # DESIRED END RESULT PART 1

if __name__ == '__main__':
    main()