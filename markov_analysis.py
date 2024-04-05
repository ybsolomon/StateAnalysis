import time
from RedistrictingMarkovChain import *

start_time = time.time()

print("Starting graph load")
# la_graph = Graph.from_json("./LA/LA.geojson")  # node issue  # TODO change to NY files
la_graph = Graph.from_file("./LA/LA.shp")  # TODO change to NY files
print("Graph loaded")
la_markov_chain = RedistrictingMarkovChain(la_graph,
                                           6,  # TODO change to NY dist count
                                           "CD",
                                           "PRES20",  # TODO change election
                                           "G20PRED",
                                           "G20PRER",
                                           "TOTPOP",  # TODO verify naming convention
                                           "HISP")
la_markov_chain.init_partition()
la_markov_chain.init_markov_chain(steps=1000)
cutedge_ensemble, lmaj_ensemble, dem_win_ensemble = la_markov_chain.walk_the_run()

# Histograms
# 1. Cut edge
plot_histograms(cutedge_ensemble, "histograms/cutedge_ensemble.png")
# 2. Majority-Latino districts
plot_histograms(lmaj_ensemble, "histograms/lmaj_ensemble.png")
# 3. Democratic-won districts
plot_histograms(dem_win_ensemble, "histograms/dem_win_ensemble.png")

end_time = time.time()
print("The time of execution of above program is :",
      (end_time - start_time) / 60, "mins")