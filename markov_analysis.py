import time
from RedistrictingMarkovChain import *

STEPS = [5000, 10000, 20000]

start_time = time.time()

print("Starting graph load")
ny_graph = Graph.from_file("./NY/NY.shp")
print("Graph loaded")
ny_markov_chain = RedistrictingMarkovChain(ny_graph,
                                           26,
                                           "CD",
                                           {"ATG18": {"Dem": "G18ATGD", "Rep": "G18ATGR"},
                                            "COM18": {"Dem": "G18COMD", "Rep": "G18COMR"},
                                            "GOV18": {"Dem": "G18GOVD", "Rep": "G18GOVR"},
                                            "SEN18": {"Dem": "G18SEND", "Rep": "G18SENR"}, },
                                           "TOTPOP",
                                           "HISP")
ny_markov_chain.init_partition()

for steps in STEPS:
    ny_markov_chain.init_markov_chain(steps=steps)
    cutedge_ensemble, lmaj_ensemble, dem_win_ensemble = ny_markov_chain.walk_the_run()

    # Histograms
    # 1. Cut edge
    plot_histograms(cutedge_ensemble, "histograms/cutedge_ensemble", steps)
    # 2. Majority-Latino districts
    plot_histograms(lmaj_ensemble, "histograms/lmaj_ensemble", steps)
    # 3. Democratic-won districts
    plot_histograms(dem_win_ensemble, "histograms/dem_win_ensemble", steps)

    end_time = time.time()
    print("The time of execution of above program for step-count ", steps, "is :",
          (end_time - start_time) / 60, "mins")
