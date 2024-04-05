import time
from gerrychain import Graph as gcG
from RedistrictingMarkovChain import *

STEPS = 1000  # TODO, [100, 5000, 10000, 20000]

start_time = time.time()

print("Starting graph load")
ny_graph = gcG.from_file("./NY/NY.shp")
print("Graph loaded")
ny_markov_chain = RedistrictingMarkovChain(ny_graph,
                                           27,
                                           "CD",
                                           "SEN18",  # TODO run multiple elections ?
                                           "G18SEND",
                                           "G18SENR",
                                           "TOTPOP",
                                           "HISP")  # TODO verify naming convention
ny_markov_chain.init_partition()
# TODO add loop for 4 dif number of steps : 100, 5k, 10k, 20k
ny_markov_chain.init_markov_chain(steps=STEPS)
cutedge_ensemble, lmaj_ensemble, dem_win_ensemble = ny_markov_chain.walk_the_run()

# Histograms
# 1. Cut edge
plot_histograms(cutedge_ensemble, f"histograms/cutedge_ensemble_{STEPS}.png")
# 2. Majority-Latino districts
plot_histograms(lmaj_ensemble, f"histograms/lmaj_ensemble_{STEPS}.png")
# 3. Democratic-won districts
plot_histograms(dem_win_ensemble, f"histograms/dem_win_ensemble_{STEPS}.png")

end_time = time.time()
print("The time of execution of above program is :",
      (end_time - start_time) / 60, "mins")
