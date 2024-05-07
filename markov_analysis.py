import time
from RedistrictingMarkovChain import *


STEPS = [5000, 10000, 20000] #[100, 500]

start_time = time.time()

print("Starting graph load")
ny_graph = Graph.from_file("./NY-lab/NY.shp")
print("Graph loaded")

elections = [
    ["PRE20", "G20PRED", "G20PRER"],
    # ["SEN18", "G18SEND", "G18SENR"],  ## election for previous graphs
    # ["GOV18", "G18GOVD", "G18GOVR"],
    # ["COM18", "G18COMD", "G18COMR"],
    # ["ATG18", "G18ATGD", "G18ATGR"]
]

pop_tols = [0.4,] #  0.4, 0.5, 0.6

for election in elections:
    for pop_tol in pop_tols:
        ny_markov_chain = RedistrictingMarkovChain(ny_graph,
                                                   26,
                                                   "CD",
                                                   election[0],
                                                   election[1],
                                                   election[2],
                                                   "TOTPOP",
                                                   "HISP",
                                                   "BVAP",
                                                   pop_tol)
        ny_markov_chain.init_partition()

        for step in STEPS:
            ny_markov_chain.init_markov_chain(steps=step)
            cutedge_ensemble, lmaj_ensemble, dem_win_ensemble = ny_markov_chain.walk_the_run()

            # Histograms
            # 1. Cut edge
            plot_histograms(cutedge_ensemble,
                            f"histograms/propose_random_flip_cutedge_ensemble_{step}_{pop_tol}_{election[0]}.png")
            # 2. Majority-Latino districts
            plot_histograms(lmaj_ensemble,
                            f"histograms/propose_random_flip_lmaj_ensemble_{step}_{pop_tol}_{election[0]}.png")
            # 3. Democratic-won districts
            plot_histograms(dem_win_ensemble,
                            f"histograms/propose_random_flip_dem_win_ensemble_{step}_{pop_tol}_{election[0]}.png")

            end_time = time.time()
            print("The time of execution of above program for step-count ", step, " for election ", election[0], "is :",
                  (end_time - start_time) / 60, "mins")
