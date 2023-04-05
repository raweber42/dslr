import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from colors import colors
import seaborn as sns


# drops all non-numeric columns besides "Hogwarts House"
def arrange_columns(df):
	# drop index column
	df.drop(columns=['Index'], inplace=True)
	for column in df:
		if df[column].dtype.kind in 'biufc':
			continue
		if column == 'Hogwarts House':
			continue
		else:
			df.drop(columns=[column], inplace=True)


# adds newlines to long label names
def adjust_plot_labels(df):
	new_column_names = []
	for column in df:
		if column == 'Hogwarts House':
			new_column_names.append(column)
		elif len(column) > 15:
			split_col = column.split(" ")
			tmp_col_name = ""
			for i in range(len(split_col)):
				tmp_col_name += split_col[i]
				if i % 2:
					tmp_col_name += "\n"
				else:
					tmp_col_name += " "
			new_column_names.append(tmp_col_name)
		else:
			new_column_names.append(column)
	df.columns = new_column_names


def main():

	try:
		df = pd.read_csv("datasets/dataset_train.csv")
	except:
		print(f"{colors().RED}Error: could not read file{colors().END}")
		exit()

	arrange_columns(df)
	adjust_plot_labels(df)

	########### normalize data start (min-max) ###########
	for column in df:
		if df[column].dtype.kind not in 'biufc':
			continue
		max_norm = df[column].max()
		min_norm = df[column].min()

		for i in range(len(df)):
			df.iloc[i, df.columns.get_loc(column)] = (df.iloc[i, df.columns.get_loc(column)] - min_norm) / (max_norm - min_norm) 
	########### normalize data end ###########

	# scale down the font size
	sns.set_style('darkgrid')
	sns.set(font_scale=0.5)
	# plot the pairplot and give a hue according to the "Hogwarts House" feature
	pairplot = sns.pairplot(df, hue="Hogwarts House", height=0.8, palette="bright", kind="scatter", plot_kws={"s": 3})

	# remove labels in sub-plots
	for ax in pairplot.axes.flatten():
   		ax.set_xticklabels([])
   		ax.set_yticklabels([])

	# plt.tight_layout()
	plt.savefig('pair_plot.png')
	plt.show()


if __name__ == '__main__':
	main()
