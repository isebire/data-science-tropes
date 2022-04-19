
import pickle
import pandas
from nestedness_calculator import NestednessCalculator
import numpy as np

tv_binary = pandas.read_csv('tv_binary_alltime.csv').drop(['Unnamed: 0', 'title'], axis=1)
# drop 0s cols
tv_binary = tv_binary.loc[:, (tv_binary != 0).any(axis=0)]
tv_df_matrix = tv_binary.to_numpy()
nestedness = NestednessCalculator(tv_df_matrix).nodf(tv_df_matrix)
print(nestedness)

vg_binary = pandas.read_csv('vg_binary_alltime.csv').drop(['Unnamed: 0', 'title'], axis=1)
vg_binary = vg_binary.loc[:, (vg_binary != 0).any(axis=0)]
vg_df_matrix = vg_binary.to_numpy()
nestedness = NestednessCalculator(vg_df_matrix).nodf(vg_df_matrix)
print(nestedness)
