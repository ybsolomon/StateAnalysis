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
population_df = gpd.read_file("./new_states/wa_pl2020_vtd/wa_pl2020_vtd.shp")
election_df = gpd.read_file("./new_states/wa_vest_20/wa_vest_20.shp")
cong_df = gpd.read_file("./new_states/wa_cong_adopted_2022/CONG_AMEND_FINAL.shp")

# %%
print(cong_df.shape) # 27 senate districts

# "G18SEND", "G18SENR"

replacing_columns_info = {
    "G20PREDBID": "G18PRED",
    "G20PRERTRU": "G18PRER",
    "G20GOVDINS": "G18GOVD",
    "G20GOVRCUL": "G18GOVR",
    # "G18COMDDIN": "G18COMD",
    # "G18COMRTRI": "G18COMR",
    "G20SOSDTAR": "G18SOSD",
    "G20SOSRWYM": "G18SOSR",
    "G20ATGDFER": "G18ATGD",
    "G20ATGRLAR": "G18ATGR"
}

election_df.rename(columns=replacing_columns_info, inplace=True)

safe_cols = ["geometry", 'COUNTY', 'PRECCODE', 'COUNTYNAME', 'ST_CODE', 'PRECNAME'] + list(replacing_columns_info.values())

cols_to_drop = [i for i in election_df.columns if i not in safe_cols]

# print(cols_to_drop)
election_df.drop(columns=cols_to_drop, inplace=True)

print(election_df.columns)

# %%
district_col_name = "DISTRICT"

# %%
# election_df.to_crs(4269, inplace=True)

# election_df.to_crs(population_df.crs, inplace=True)
# cong_df.to_crs(population_df.crs, inplace=True)

population_df.to_crs(election_df.crs, inplace=True)
cong_df.to_crs(election_df.crs, inplace=True)

print(population_df.crs)
print(cong_df.crs)

# %%

print(population_df.crs)

vtds_to_precincts_assignment = maup.assign(population_df.geometry, election_df.geometry)

# %%

print(vtds_to_precincts_assignment.dtypes)

# %%

pop_column_names = ['P0020001', 'P0020002', 'P0020005', 'P0020006',
                    'P0020007', 'P0020008', 'P0020009', 'P0020010']

vap_column_names = ['P0040001', 'P0040002', 'P0040005', 'P0040006',
                    'P0040007', 'P0040008', 'P0040009', 'P0040010']

print(election_df.columns)

# %%
# elections_copy = election_df.copy()

election_df[pop_column_names] = population_df[pop_column_names].groupby(vtds_to_precincts_assignment).sum()

election_df[pop_column_names].head()

# %%

print(population_df[pop_column_names].sum())
print(election_df[pop_column_names].sum())

election_cols = ["G18PRED", "G18PRER", "G18GOVD", "G18GOVR", "G18SOSD", "G18SOSR", "G18ATGD", "G18ATGR"]

# %%

# weights2018 = population_df["P0040001"] / vtds_to_precincts_assignment.map(population_df["P0040001"].groupby(vtds_to_precincts_assignment).sum())
# weights2018 = weights2018.fillna(0)

# %%

# prorated2018 = maup.prorate(vtds_to_precincts_assignment, election_df[pop_column_names], weights2018)
# print(prorated2018.head())

# population_df[election_cols] = prorated2018

# %%
print(population_df[pop_column_names].sum())
print(election_df[pop_column_names].sum())

# %% this takes 30 seconds
print(maup.doctor(population_df))

# %%

print(cong_df.shape)

# %%
# pop_copy = population_df.copy()

precincts_to_districts_assignment = maup.assign(cong_df.geometry, election_df.geometry)
population_df["CD"] = precincts_to_districts_assignment

# %%

for precinct_index in range(len(population_df)):
    population_df.at[precinct_index, "CD"] = int(cong_df.at[population_df.at[precinct_index, "CD"], district_col_name])


# %%
print(population_df.columns)
rename_dict = {'P0020001': 'TOTPOP', 'P0020002': 'HISP', 'P0020005': 'NH_WHITE', 'P0020006': 'NH_BLACK', 'P0020007': 'NH_AMIN',
                    'P0020008': 'NH_ASIAN', 'P0020009': 'NH_NHPI', 'P0020010': 'NH_OTHER',
                    'P0040001': 'VAP', 'P0040002': 'HVAP', 'P0040005': 'WVAP', 'P0040006': 'BVAP', 'P0040007': 'AMINVAP',
                                        'P0040008': 'ASIANVAP', 'P0040009': 'NHPIVAP', 'P0040010': 'OTHERVAP'}

population_df.rename(columns=rename_dict, inplace=True)
print(population_df.columns)

# %%
# sanity type check
print(population_df['CD'].dtypes)

# %%
ny_map = gpd.GeoDataFrame(population_df, geometry='geometry')
ny_map.plot()

pop_vals = []

for i in range(1, 10):
  pop_vals.append(population_df.loc[population_df["CD"] == i, "TOTPOP"].sum())

print(pop_vals)

# %%
population_df.to_file("./WA/WA.shp")

# %%
