import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from colors import colors
import sys
import math
from describe import calculate_standard_deviation


def arrange_columns_for_houses(df):
	# drop index column
	df.drop(columns=['Index'], inplace=True)

	# drop non-numeric columns
	for column in df:
		if df[column].dtype.kind in 'biufc': # https://stackoverflow.com/a/38185438
			continue
		elif column== "Hogwarts House":
			continue
		else:
			df.drop(columns=[column], inplace=True)
	

def rename_columns(df):
	new_column_names = []
	i = 1
	for column in df:
		if column == "Hogwarts House":
			new_column_names.append("Hogwarts House")
		else:
			new_column_names.append("Feature " + str(i))
			i += 1
	df.columns = new_column_names


def main():
	try:
		df = pd.read_csv("datasets/dataset_train.csv")
	except:
		print(f"{colors().RED}Error: could not read file{colors().END}")
		exit()
	
	### MATHS PART COPIED FROM describe.py
	arrange_columns_for_houses(df)
	rename_columns(df)

	########### normalize data start ###########
	for column in df:
		if df[column].dtype.kind not in 'biufc': # https://stackoverflow.com/a/38185438
			continue
		max_norm = df[column].max()
		min_norm = df[column].min()

		# df[column] /= max_norm
		for i in range(len(df)):
			df.iloc[i, df.columns.get_loc(column)] = (df.iloc[i, df.columns.get_loc(column)] - min_norm) / (max_norm - min_norm) 
	########### normalize data end ###########

	print(df)
	
	count = 0
	mean = 0.0
	global_std_array = []
	
	# local_std_array = np.array([[], [], [], []])
	local_std_array = [[], [], [], []]
	std = 0

	for column in df:
		
		count = 0.0
		gryffindor_count = 0.0
		hufflepuff_count = 0.0
		ravenclaw_count = 0.0
		slytherin_count = 0.0
		mean = 0.0
		gryffindor_mean = 0.0
		hufflepuff_mean = 0.0
		ravenclaw_mean = 0.0
		slytherin_mean = 0.0
		std = 0
		gryffindor_std = 0.0
		hufflepuff_std = 0.0
		ravenclaw_std = 0.0
		slytherin_std = 0.0

		index_helper = 0
		for value in df[column]:
			local_std_array = [[], [], [], []]
			if value == "Gryffindor" or value == "Hufflepuff" or value == "Ravenclaw" or value == "Slytherin":
				break
			if df["Hogwarts House"][index_helper] == "Gryffindor":
				flag = "Gryffindor"
			if df["Hogwarts House"][index_helper] == "Hufflepuff":
				flag = "Hufflepuff"
			if df["Hogwarts House"][index_helper] == "Ravenclaw":
				flag = "Ravenclaw"
			if df["Hogwarts House"][index_helper] == "Slytherin":
				flag = "Slytherin"
			index_helper += 1

			#flags work!!
		
			if math.isnan(value) == False:
				if flag == "Gryffindor":
					gryffindor_count += 1
				if flag == "Hufflepuff":
					hufflepuff_count += 1
				if flag == "Ravenclaw":
					ravenclaw_count += 1
				if flag == "Slytherin":
					slytherin_count += 1
				count += 1
			else:
				value = 0
			if flag == "Gryffindor":
				gryffindor_mean += value
			if flag == "Hufflepuff":
				hufflepuff_mean += value
			if flag == "Ravenclaw":
				ravenclaw_mean += value
			if flag == "Slytherin":
				slytherin_mean += value
			mean = mean + value
			gryffindor_mean = gryffindor_mean + value
			hufflepuff_mean = hufflepuff_mean + value
			ravenclaw_mean = ravenclaw_mean + value
			slytherin_mean = slytherin_mean + value
		
		if column != "Hogwarts House":
			mean = mean / count
			gryffindor_mean = gryffindor_mean / gryffindor_count
			hufflepuff_mean = hufflepuff_mean / hufflepuff_count
			ravenclaw_mean = ravenclaw_mean / ravenclaw_count
			slytherin_mean = slytherin_mean / slytherin_count			
			
			std = calculate_standard_deviation(df, column, mean, count)
			gryffindor_std = calculate_standard_deviation(df, column, gryffindor_mean, gryffindor_count)
			hufflepuff_std = calculate_standard_deviation(df, column, hufflepuff_mean, hufflepuff_count)
			ravenclaw_std = calculate_standard_deviation(df, column, ravenclaw_mean, ravenclaw_count)
			slytherin_std = calculate_standard_deviation(df, column, slytherin_mean, slytherin_count)
			
			print("gr_std: ", gryffindor_std, " huf_std: ", hufflepuff_std, " rav_std: ", ravenclaw_std)

			local_std_array[0].append(gryffindor_std)
			local_std_array[1].append(hufflepuff_std)
			local_std_array[2].append(ravenclaw_std)
			local_std_array[3].append(slytherin_std)
			global_std_array.append(local_std_array)
	### END MATHS PART
	
	#https://mode.com/example-gallery/python_histogram/
	# df.hist(column='Hogwarts House')
	# normalize all values
	# balkendiagramm für jedes zählbare feature, dann alle balkendiagramme übereinander legen
	# either unterschiedliche häuser -> unterschiedliche farben
	# oder eine metrik für die homogenität und die alle nebeneinanber
	# print(local_std_array)
	for array in global_std_array:
		print(array)
		print("\n")
	# hist = df.hist(column='Arithmancy')
	# plt.show()


if __name__ == '__main__':
    main()


# wanna have measure for: homogenity for course BUT: per house
# so we'll have 4 numbers per Feature, maybe we could combine them then