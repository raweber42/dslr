import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import time
from colors import colors
import sys
import math
from describe import calculate_standard_deviation
#Gradient Color Bar Plots
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from matplotlib import colors as mcolors, path


def arrange_columns_for_houses(df):
	# drop index column
	df.drop(columns=['Index'], inplace=True)

	# drop non-numeric columns
	for column in df:
		if df[column].dtype.kind in 'biufc':
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
	
	arrange_columns_for_houses(df)

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
	
	count = 0
	mean = 0.0
	global_std_array = []
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
			local_std_array = []
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
			
			# print("gr_std: ", gryffindor_std, " huf_std: ", hufflepuff_std, " rav_std: ", ravenclaw_std)

			local_std_array.append(gryffindor_std)
			local_std_array.append(hufflepuff_std)
			local_std_array.append(ravenclaw_std)
			local_std_array.append(slytherin_std)
			# print(local_std_array)
			global_std_array.append(local_std_array)
	### END MATHS PART
	

	hist_array = []
	for array in global_std_array:
		hist_count = 0
		hist_mean = 0
		for value in array:
			if math.isnan(value) == False:
				hist_count += 1
			else:
				value = 0			
			hist_mean += value
		hist_mean = hist_mean / hist_count

		hist_std = 0
		for value in array:
			if math.isnan(value) == True:
				continue
			hist_std += (value - hist_mean) ** 2
		
		hist_std /= (len(array) - 1)
		hist_std = math.sqrt(hist_std)
		hist_array.append(hist_std)

		
	def gradientbars(bars,ydata,cmap):
		ax = bars[0].axes
		lim = ax.get_xlim()+ax.get_ylim()
		ax.axis(lim)
		for bar in bars:
			bar.set_facecolor("none")
			x,y = bar.get_xy()
			w, h = bar.get_width(), bar.get_height()
			grad = np.atleast_2d(np.linspace(0,1*h/max(ydata),256)).T
			# zorder of 2 to get gradients above the facecolor, but below the bar outlines
			ax.imshow(grad, extent=[x,x+w,y,y+h], origin='lower',aspect="auto",zorder=2, norm=cm.colors.NoNorm(vmin=0,vmax=1),cmap=plt.get_cmap(cmap))


	fig, ax = plt.subplots()
	# show horizontal grid lines
	ax.grid(which='major', axis='y', linestyle='--', color='gray', zorder=0)
	# zorder=3 makes our edges show
	courses = ['Arithmancy' ,'Astronomy', 'Herbology', 'Defense Against the Dark Arts', 'Divination', 'Muggle Studies', 'Ancient Runes', 'History of Magic', 'Transfiguration', 'Potions', 'Care of Magical Creatures', 'Charms', 'Flying']
	my_bar = ax.bar(courses ,hist_array, edgecolor='gray', zorder=3)
	gradientbars(my_bar, hist_array, 'YlOrRd')

	plt.xticks(rotation=90)
	plt.title("Homogenity of scores per Hogwarts course", fontsize=16, fontweight=0)
	plt.xlabel("hogwarts course",  fontsize=14)
	plt.ylabel("standard deviation",  fontsize=14)
	ax.xaxis.label.set_color('grey')
	ax.yaxis.label.set_color('grey')
	plt.tight_layout()
	plt.savefig('histogram.png')
	plt.show()


if __name__ == '__main__':
    main()


# wanna have measure for: homogenity for course BUT: per house
# so we'll have 4 numbers per Feature, I will combine them