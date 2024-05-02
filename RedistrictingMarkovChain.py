import matplotlib.pyplot as plt
from gerrychain import Graph, Partition, proposals, updaters, constraints, accept, MarkovChain, Election, \
    GeographicPartition
from gerrychain.updaters import cut_edges, Tally
from gerrychain.proposals import recom
from gerrychain.accept import always_accept
from functools import partial
from gerrychain.proposals import propose_random_flip


class RedistrictingMarkovChain:
    def __init__(self, graph, num_dist, assignment, election_name,
                 dem_col_name, rep_col_name, pop_col_name, hpop_col_name,
                 dem_party_name="Democratic", rep_party_name="Republican", pop_tolerance=0.10):
        self.graph = graph
        self.initial_partition = None
        self.updaters = None
        self.random_walk = None

        self.pop_tolerance = pop_tolerance
        self.num_dist = num_dist

        self.assignment = assignment
        self.election_name = election_name
        self.dem_col_name = dem_col_name
        self.rep_col_name = rep_col_name
        self.pop_col_name = pop_col_name
        self.hpop_col_name = hpop_col_name
        self.dem_party_name = dem_party_name
        self.rep_party_name = rep_party_name

    def _party_win_updater(self, partition):
        dem_shares = partition[self.election_name].percents("Democratic")
        dem_seats = partition[self.election_name].seats(self.dem_party_name)
        rep_shares = partition[self.election_name].percents(self.rep_party_name)
        rep_seats = partition[self.election_name].seats(self.rep_party_name)
        party_wins = 0
        for dist in dem_shares:
            if dist >= 0.5:
                party_wins += 1
        return party_wins

    def _init_updaters(self):
        self.updaters = {
            "our cut edges": cut_edges,
            self.pop_col_name: Tally(self.pop_col_name, alias=self.pop_col_name),
            self.hpop_col_name: Tally(self.hpop_col_name, alias=self.hpop_col_name),
            "democratic_votes": Tally(self.dem_col_name, alias="democratic_votes"),
            "republican_votes": Tally(self.rep_col_name, alias="republican_votes"),
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
        # rw_proposal = partial(recom,
        #                       pop_col=self.pop_col_name,
        #                       pop_target=self.ideal_pop,
        #                       epsilon=self.pop_tolerance,
        #                       node_repeats=1
        # )
        proposal = partial(
            propose_random_flip,
        )
        population_constraint = constraints.within_percent_of_ideal_population(
            self.initial_partition,
            self.pop_tolerance,
            pop_key=self.pop_col_name
        )
        chain = MarkovChain(
            proposal=proposal,
            constraints=[population_constraint],
            accept=always_accept,
            initial_state=self.initial_partition,
            total_steps=steps)
        self.random_walk = chain
        print(f"Markov Chain initialized with {steps} steps")

    def walk_the_run(self):
        cutedge_ensemble = []
        lmaj_ensemble = []
        party_win_ensemble = []

        print("Walking the ensemble")
        for part in self.random_walk:
            cutedge_ensemble.append(len(part["our cut edges"]))

            num_maj_latino = 0
            num_democratic_maj = 0
            for i in range(self.num_dist):
                l_perc = part[self.hpop_col_name][i + 1] / part[self.pop_col_name][i + 1]  # 1-indexed dist identifiers
                if l_perc >= 0.5:
                    num_maj_latino = num_maj_latino + 1

                if part["democratic_votes"][i+1] > part["republican_votes"][i+1]:
                    num_democratic_maj += 1

            lmaj_ensemble.append(num_maj_latino)
            # dem_win_ensemble.append(self._dem_win_updater(part))
            party_win_ensemble.append(num_democratic_maj)

        print("Walk complete")
        return cutedge_ensemble, lmaj_ensemble, party_win_ensemble


def plot_histograms(ensemble, filename):
    plt.figure()
    plt.hist(ensemble, align="left")
    plt.savefig(filename)
