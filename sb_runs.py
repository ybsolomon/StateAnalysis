#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 16:29:27 2023

@author: erv2, and all authors of https://github.com/vrdi/shortbursts-gingles/blob/main/state_experiments/sb_runs.py
"""

import argparse
import geopandas as gpd
import numpy as np
import pickle
from functools import partial
from gerrychain import Graph, GeographicPartition, Partition, Election, accept
from gerrychain.updaters import Tally, cut_edges
from gerrychain import MarkovChain
from gerrychain.proposals import recom
from gerrychain.accept import always_accept
from gerrychain import constraints
from gerrychain.tree import recursive_tree_part
from gingleator import Gingleator
#from little_helpers import *
import json
import multiprocessing

## Read in
parser = argparse.ArgumentParser(description="SB Chain run",
                                 prog="sb_runs.py")
parser.add_argument("--state", metavar="state_id", type=str,
                    choices=["VA", "TX", "AR", "CO", "LA", "NM", "NY"],
                    help="which state to run chains on")
parser.add_argument("--iters", metavar="chain_length", type=int,
                    help="how long to run each chain", default=1000)
parser.add_argument("--l", metavar="burst_length", type=int,
                    help="The length of each short burst", default=50)
parser.add_argument("--col", metavar="column", type=str,
                    help="Which column to optimize", default="HVAP")
parser.add_argument("--score", metavar="score_function", type=int,
                    help="How to count gingles districts",
                    choices=[0,1,2,3,4], default=0)
args = parser.parse_args()

num_h_districts = {"VA": 100, "TX": 150, "AR": 100, "CO": 65, "LA": 105, "NM": 70, "NY": 26}


score_functs = {0: None, 1: Gingleator.reward_partial_dist,
    2: Gingleator.reward_next_highest_close,
    3: Gingleator.penalize_maximum_over,
    4: Gingleator.penalize_avg_over}

BURST_LEN = args.l
NUM_DISTRICTS = num_h_districts["NY"]
ITERS = args.iters
POP_COL = "TOTPOP"
N_SAMPS = 10
SCORE_FUNCT = score_functs[0]
EPS = 0.045
MIN_POP_COL = args.col
TOLERANCE = 0.1

## Setup graph, updaters, elections, and initial partition

print("Reading in Data/Graph", flush=True)

# graph = Graph.from_json("BG_LA.json")
graph = Graph.from_file("./NY-lab/NY.shp")


my_updaters = {"TOT_POP" : Tally(POP_COL, alias="TOT_POP"),
               "VAP": Tally("VAP"),
               "BVAP": Tally("BVAP"),
               "HVAP": Tally("HVAP"),
               "WVAP": Tally("WVAP"),
               "nWVAP": lambda p: {k: v - p["WVAP"][k] for k,v in p["VAP"].items()},
               "cut_edges": cut_edges,
               "population" : Tally(POP_COL, alias="TOT_POP")}


print("Creating seed plan", flush=True)

total_pop = sum([graph.nodes()[n][POP_COL] for n in graph.nodes()])

init_partition = Partition(graph, assignment="CD", updaters=my_updaters)

gingles = Gingleator(init_partition, pop_col=POP_COL,
threshold=TOLERANCE, score_funct=SCORE_FUNCT, epsilon=EPS,
minority_perc_col="{}_perc".format(MIN_POP_COL))

gingles.init_minority_perc_col(MIN_POP_COL, "VAP",
"{}_perc".format(MIN_POP_COL))

num_bursts = int(ITERS/BURST_LEN)

print("Starting Short Bursts Runs", flush=True)

# for n in range(N_SAMPS):
#     sb_obs = gingles.short_burst_run(num_bursts=num_bursts, num_steps=BURST_LEN,
#     maximize=True, verbose=False)
#     print("\tFinished chain {}".format(n), flush=True)

#     print("\tSaving results", flush=True)

#     f_out = "data/states/{}_{}_dists{}_{}opt_{:.1%}_{}_sbl{}_score{}_{}.npy".format(TOLERANCE, "NY",
#                                                         NUM_DISTRICTS, MIN_POP_COL, EPS,
#                                                         ITERS, BURST_LEN, 0, n)
#     np.save(f_out, sb_obs[1])

#     f_out_part = "data/states/{}_{}_dists{}_{}opt_{:.1%}_{}_sbl{}_score{}_{}_max_part.p".format(TOLERANCE, "NY",
#                                                         NUM_DISTRICTS, MIN_POP_COL, EPS,
#                                                         ITERS, BURST_LEN, 0, n)

#     max_stats = {"VAP": sb_obs[0][0]["VAP"],
#     "BVAP": sb_obs[0][0]["BVAP"],
#     "WVAP": sb_obs[0][0]["WVAP"],
#     "HVAP": sb_obs[0][0]["HVAP"],}

#     with open(f_out_part, "wb") as f_out:
#         pickle.dump(max_stats, f_out)

def func(n):
    sb_obs = gingles.short_burst_run(num_bursts=num_bursts, num_steps=BURST_LEN,
    maximize=True, verbose=False)
    print("\tFinished chain {}".format(n), flush=True)

    print("\tSaving results", flush=True)

    f_out = "data/states/{}_{}_dists{}_{}opt_{:.1%}_{}_sbl{}_score{}_{}.npy".format(TOLERANCE, "NY",
                                                        NUM_DISTRICTS, MIN_POP_COL, EPS,
                                                        ITERS, BURST_LEN, 0, n)
    np.save(f_out, sb_obs[1])

    f_out_part = "data/states/{}_{}_dists{}_{}opt_{:.1%}_{}_sbl{}_score{}_{}_max_part.p".format(TOLERANCE, "NY",
                                                        NUM_DISTRICTS, MIN_POP_COL, EPS,
                                                        ITERS, BURST_LEN, 0, n)

    max_stats = {"VAP": sb_obs[0][0]["VAP"],
    "BVAP": sb_obs[0][0]["BVAP"],
    "WVAP": sb_obs[0][0]["WVAP"],
    "HVAP": sb_obs[0][0]["HVAP"],}

    with open(f_out_part, "wb") as f_out:
        pickle.dump(max_stats, f_out)

# pool_obj = multiprocessing.Pool()

print("Running jobs {} times".format(N_SAMPS))

# ans = pool_obj.map(func,range(0,N_SAMPS))
# pool_obj.close()

for i in range(0,N_SAMPS):
    func(i)