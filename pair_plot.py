import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from colors import colors
import seaborn as sns


def arrange_columns(df):
	# drop index column
	df.drop(columns=['Index'], inplace=True)
	for column in df:
		if df[column].dtype.kind in 'biufc': # https://stackoverflow.com/a/38185438
			#print(df[column])
			continue
		if column == 'Hogwarts House':
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
	# get sub-df's by houses
	# ravenclaw = df[df["Hogwarts House"] == "Ravenclaw"]

	########### normalize data start (min-max) ###########
	for column in df:
		if df[column].dtype.kind not in 'biufc': # https://stackoverflow.com/a/38185438
			continue
		max_norm = df[column].max()
		min_norm = df[column].min()

		for i in range(len(df)):
			df.iloc[i, df.columns.get_loc(column)] = (df.iloc[i, df.columns.get_loc(column)] - min_norm) / (max_norm - min_norm) 
	########### normalize data end ###########

	
	sns.set_style('darkgrid')
	
	#REMOVE
	# i = 0
	# for column in df:
	# 	i += 1
	# 	if i > 5:
	# 		df.drop(columns=[column], inplace=True)
	#REMOVE

	pairplot = sns.pairplot(df, hue="Hogwarts House", height=0.8, palette="bright", kind="scatter", plot_kws={"s": 3})
	# pairplot.set_yticklabels(df.columns, rotation=90)
	# pairplot.tick_params(axis='both', rotation=90)
	# pairplot.set(xlabel)
	# for ax in pairplot.axes.flatten():
   		# ax.tick_params(rotation = 90)
	# ax.set_xticklabels(["one", "two", "three", "four", "five"], rotation=45)

	# plt.legend(bbox_to_anchor=(1.02, 0.15), loc='upper left', borderaxespad=0)
	# plt.yticks(rotation=90)
	# sns.xticks(rotation=90)

	# plt.tight_layout()
	plt.savefig('pair_plot.png')
	plt.show()


if __name__ == '__main__':
	main()
