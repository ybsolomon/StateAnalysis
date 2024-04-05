import matplotlib.pyplot as plt
from gerrychain import Graph, Partition, proposals, updaters, constraints, accept, MarkovChain, Election, \
    GeographicPartition
from gerrychain.updaters import cut_edges, Tally
from gerrychain.proposals import recom
from gerrychain.accept import always_accept
from functools import partial


class RedistrictingMarkovChain:
    def __init__(self, graph, num_dist, assignment, election_name,
                 dem_col_name, rep_col_name, pop_col_name, hpop_col_name, pop_tolerance=0.02):
        self.graph = graph
        self.initial_partition = None
        self.updaters = None
        self.random_walk = None

        self.pop_tolerance = pop_tolerance
        self.num_dist = num_dist

        self.assignment = assignment
        self.election_name = election_name  # TODO accept a str or list
        self.dem_col_name = dem_col_name
        self.rep_col_name = rep_col_name
        self.pop_col_name = pop_col_name
        self.hpop_col_name = hpop_col_name

    def _dem_win_updater(self, partition):
        dem_shares = partition[self.election_name].percents("Democratic")
        dem_wins = 0
        for dist in dem_shares:
            if dist > 0.5:
                dem_wins += 1
        return dem_wins

    def _init_updaters(self):
        self.updaters = {
            "our cut edges": cut_edges,
            self.pop_col_name: Tally(self.pop_col_name, alias=self.pop_col_name),
            self.hpop_col_name: Tally(self.hpop_col_name, alias=self.hpop_col_name)
        }
        # TODO update election initialization process : str or list
        e = Election(self.election_name, {"Democratic": self.dem_col_name, "Republican": self.rep_col_name})
        self.updaters.update({e.name: e})

    def init_partition(self):
        self._init_updaters()
        initial_partition = GeographicPartition(
            self.graph,
            assignment=self.assignment,
            updaters=self.updaters
        )
        self.initial_partition = initial_partition

    def _calc_population(self):
        tot_pop = sum([self.graph.nodes()[v][self.pop_col_name] for v in self.graph.nodes()])
        self.ideal_pop = tot_pop / self.num_dist

    def init_markov_chain(self, steps):
        self._calc_population()
        rw_proposal = partial(recom,
                              pop_col=self.pop_col_name,
                              pop_target=self.ideal_pop,
                              epsilon=self.pop_tolerance,
                              node_repeats=1
                              )
        population_constraint = constraints.within_percent_of_ideal_population(
            self.initial_partition,
            self.pop_tolerance,
            pop_key=self.pop_col_name)
        random_walk = MarkovChain(
            proposal=rw_proposal,
            constraints=[population_constraint],
            accept=always_accept,
            initial_state=self.initial_partition,
            total_steps=steps)
        self.random_walk = random_walk

        print(f"Markov Chain initialized with {steps} steps")

    def walk_the_run(self):
        cutedge_ensemble = []
        lmaj_ensemble = []
        dem_win_ensemble = []

        print("Walking the ensemble")
        for part in self.random_walk:
            cutedge_ensemble.append(len(part["our cut edges"]))

            num_maj_latino = 0
            for i in range(self.num_dist):
                l_perc = part[self.hpop_col_name][i + 1] / part[self.pop_col_name][i + 1]  # 1-indexed dist identifiers
                if l_perc >= 0.5:
                    num_maj_latino = num_maj_latino + 1
            lmaj_ensemble.append(num_maj_latino)
            dem_win_ensemble.append(self._dem_win_updater(part))

        print("Walk complete")
        return cutedge_ensemble, lmaj_ensemble, dem_win_ensemble


def plot_histograms(ensemble, filename):
    plt.figure()
    plt.hist(ensemble, align="left")
    plt.savefig(filename)
