#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#%%
"""
Created on Tue Nov 21 13:32:51 2023

@author: eveomett

Lab 3: MAUP and data.  See details on Canvas page

Make sure to say where/when you got your data!
"""

import pandas as pd
import geopandas as gpd
import maup
import time
import matplotlib as plt

maup.progress.enabled = True

# %%
# these two files alone take 13 minutes to download (census block level bc there wasnt a precinct shp file)
population_df = gpd.read_file("./ny_pl2020_b/ny_pl2020_p2_b.shp")
vap_df = gpd.read_file("./ny_pl2020_b/ny_pl2020_p4_b.shp")

# %%

election_df = gpd.read_file("./ny_2020_gen_2020_blocks/ny_2020_gen_2020_blocks.shp")
cong_df = gpd.read_file("./ny_pl2020_cd/ny_pl2020_cd.shp")

# %%
print(cong_df.shape) # 38 senate districts

# %%

print(population_df.columns)
print(vap_df.columns)
print(cong_df.columns)
print(election_df.columns)

# %%

print(cong_df)
cong_df.dtypes

# %%
district_col_name = "CD116FP"

# %%
# this takes 10 minutes
blocks_to_precincts_assignment = maup.assign(population_df.geometry, election_df.geometry)
vap_blocks_to_precincts_assignment = maup.assign(vap_df.geometry, election_df.geometry)

# %%

print(blocks_to_precincts_assignment.dtypes)

# %%

pop_column_names = ['P0020001', 'P0020002', 'P0020005', 'P0020006', 'P0020007',
                    'P0020008', 'P0020009', 'P0020010']

vap_column_names = ['P0040001', 'P0040002', 'P0040005', 'P0040006', 'P0040007',
                    'P0040008', 'P0040009', 'P0040010']

# %%

for name in pop_column_names:
    election_df[name] = population_df[name].groupby(blocks_to_precincts_assignment).sum()
for name in vap_column_names:
    election_df[name] = vap_df[name].groupby(vap_blocks_to_precincts_assignment).sum()

# %%

print(population_df['P0020001'].sum())
print(election_df['P0020001'].sum())
print(vap_df['P0040001'].sum())
print(election_df['P0040001'].sum())
# %%

# this takes 5 minutes
print(maup.doctor(election_df))

# %%

print(cong_df.shape)

# %%

precincts_to_districts_assignment = maup.assign(election_df.geometry, cong_df.geometry)
election_df["CD"] = precincts_to_districts_assignment

# %%
print(set(election_df["CD"]))
for precinct_index in range(len(election_df)):
    election_df.at[precinct_index, "CD"] = int(cong_df.at[election_df.at[precinct_index, "CD"], district_col_name])
print(set(cong_df[district_col_name]))
print(set(election_df["CD"]))

# %%

rename_dict = {'P0020001': 'TOTPOP', 'P0020002': 'HISP', 'P0020005': 'NH_WHITE', 'P0020006': 'NH_BLACK', 'P0020007': 'NH_AMIN',
                    'P0020008': 'NH_ASIAN', 'P0020009': 'NH_NHPI', 'P0020010': 'NH_OTHER',
                    'P0040001': 'VAP', 'P0040002': 'HVAP', 'P0040005': 'WVAP', 'P0040006': 'BVAP', 'P0040007': 'AMINVAP',
                                        'P0040008': 'ASIANVAP', 'P0040009': 'NHPIVAP', 'P0040010': 'OTHERVAP', 
                                        'G20PREDBID': 'G20PRED', 'G20PRERTRU': 'G20PRER', 'G20USSDDUR': 'G20USSD', 
                                        'G20USSRCUR': 'G20USSR'}

# %%
# sanity type check
print(election_df['CD'].dtypes)
# %%
election_df.rename(columns=rename_dict, inplace = True)

# %%
election_df.drop(columns=[ 'G20PRELJOR','G20PREGHAW', 'G20PREIPIE', 'G20PREOWRI'], inplace=True)

list(election_df.columns)

# %%
ny_map = gpd.GeoDataFrame(election_df, geometry='geometry')
ny_map.plot()

# %%
print(election_df.loc[election_df["CD"] == 1, "TOTPOP"].sum())
print(election_df.loc[election_df["CD"] == 2, "TOTPOP"].sum())

pop_vals = []

for i in range(1, 28):
  pop_vals.append(election_df.loc[election_df["CD"] == i, "TOTPOP"].sum())

print(pop_vals)
# %%

election_df.to_file("./NY/NY.shp")
