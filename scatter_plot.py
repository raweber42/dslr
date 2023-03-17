import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from colors import colors


def arrange_columns(df):
	# drop index column
	df.drop(columns=['Index'], inplace=True)
	for column in df:
		if df[column].dtype.kind in 'biufc': # https://stackoverflow.com/a/38185438
			#print(df[column])
			continue
		else:
			df.drop(columns=[column], inplace=True)


def main():

	try:
		df = pd.read_csv("datasets/dataset_train.csv")
	except:
		print(f"{colors().RED}Error: could not read file{colors().END}")
		exit()

	arrange_columns(df)


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


	fig, ax = plt.subplots(4,4)
	i = 0
	j = 0
	counter = 0
	# show scatter plots for all features
	for column in df:
		if j == 4:
			i += 1
			j = 0
		# sort column ascending for percentiles
		df.sort_values(by=[column], inplace=True)

		# change color below! and make it subplots
		
		ax[i][j].scatter(df.index, df[column], s=1, color="black")
		ax[i][j].set_title(df.columns[counter])

		j += 1
		counter += 1
	
	plt.tight_layout()
	# show scatter plot with the highest correlation
	fig_cor, ax_cor = plt.subplots()
	# someVariable = df["Arithmancy"].corrwith(df["Flying"])
	max_corr = 0
	for column in df:
		someVariable = df.corrwith(df[column], axis=0)
		for (index, value) in enumerate(someVariable):
			if value > max_corr and column != someVariable.index[index]:
				max_corr = value
				max_corr_col_1 = column
				max_corr_col_2 = someVariable.index[index]
				print(f"Current max_corr of {max_corr} in column {column} comparing to {someVariable.index[index]}")
	ax_cor.set_title(f"Highest correlation: {max_corr_col_1} and {max_corr_col_2}")
	ax_cor.scatter(df.index, df[max_corr_col_1], s=8, color="yellow", marker="s", label=max_corr_col_1)
	ax_cor.scatter(df.index, df[max_corr_col_2], s=8, color="black", marker="^", label=max_corr_col_2)
	ax_cor.legend(loc="best")
	plt.tight_layout()
	plt.show()


if __name__ == '__main__':
	main()
