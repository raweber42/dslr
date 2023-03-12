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
    print(df)

    fig, ax = plt.subplots(4,4)
    i = 0
    j = 0
    for column in df:
       
		# sort column ascending for percentiles
        df.sort_values(by=[column], inplace=True)

        # change color below! and make it subplots
        ax[i][j].scatter(list(range(0, len(df[column]))), df[column], s=1, color="black")
        # marker="s", markersize=10, markerfacecolor="lightblue"
        if j == 3:
           i += 1
           j = 0
        j += 1
        
        # plt.scatter(list(range(0, len(df.Arithmancy))), df.Arithmancy, color="black")

    # plt.plot(
    #     list(range(0, len(column))), 
    #     column, 
        # color="green")
    # uncomment below for prediction marker
    # plt.plot(input_mileage, prediction, marker="s", markersize=10, markerfacecolor="lightblue")
    plt.show()


if __name__ == '__main__':
    main()