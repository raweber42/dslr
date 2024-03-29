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
		if df[column].dtype.kind in 'biufc': # https://stackoverflow.com/a/38185438
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
		if df[column].dtype.kind not in 'biufc': # https://stackoverflow.com/a/38185438
			continue
		max_norm = df[column].max()
		min_norm = df[column].min()

		for i in range(len(df)):
			df.iloc[i, df.columns.get_loc(column)] = (df.iloc[i, df.columns.get_loc(column)] - min_norm) / (max_norm - min_norm) 
	########### normalize data end ###########

	




if __name__ == '__main__':
	main()
