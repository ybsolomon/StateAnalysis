import matplotlib.pyplot as plt
from gerrychain import Graph, Partition, proposals, updaters, constraints, accept, MarkovChain, Election, \
    GeographicPartition
from gerrychain.updaters import cut_edges, Tally
from gerrychain.proposals import recom
from gerrychain.accept import always_accept
from functools import partial


def plot_histograms(data, filepath, steps):
    if isinstance(data, dict):
        for election in data.keys():
            plt.figure()
            plt.hist(data.get(election), align="left")
            plt.savefig(f"{filepath}_{election}_{steps}.png")
    elif isinstance(data, list):
        plt.figure()
        plt.hist(data, align="left")
        plt.savefig(f"{filepath}_{steps}.png")
    else:
        raise TypeError(f"data must be either a dict or a list, instead received {type(data)}")


class RedistrictingMarkovChain:
    def __init__(self, graph, num_dist, assignment, elections_map, pop_col_name, hpop_col_name,
                 dem_party_name="Democratic", rep_party_name="Republican", pop_tolerance=0.10):
        self.graph = graph
        self.initial_partition = None
        self.updaters = None
        self.random_walk = None

        self.pop_tolerance = pop_tolerance
        self.num_dist = num_dist

        self.assignment = assignment
        self.election_names = elections_map.keys()
        self.election_party_cols = elections_map
        self.pop_col_name = pop_col_name
        self.hpop_col_name = hpop_col_name
        self.dem_party_name = dem_party_name
        self.rep_party_name = rep_party_name

    def _party_win_updater(self, partition):
        wins_per_election = dict()
        for election in self.election_names:
            dem_shares = partition[election].percents(self.dem_party_name)
            dem_seats = partition[election].seats(self.dem_party_name)
            rep_shares = partition[election].percents(self.rep_party_name)
            rep_seats = partition[election].seats(self.rep_party_name)
            party_wins = 0
            for dist in dem_shares:
                if dist > 0.5:
                    party_wins += 1
            wins_per_election.update({election: party_wins})
        return wins_per_election

    def _init_updaters(self):
        self.updaters = {
            "our cut edges": cut_edges,
            self.pop_col_name: Tally(self.pop_col_name, alias=self.pop_col_name),
            self.hpop_col_name: Tally(self.hpop_col_name, alias=self.hpop_col_name)
        }
        for election in self.election_names:
            e = Election(election, {self.dem_party_name: self.election_party_cols.get(election).get("Dem"),
                                    self.rep_party_name: self.election_party_cols.get(election).get("Rep")})
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
        party_win_ensemble = {}

        print("Walking the ensemble")
        for part in self.random_walk:
            cutedge_ensemble.append(len(part["our cut edges"]))

            num_maj_latino = 0
            for i in range(self.num_dist):
                l_perc = part[self.hpop_col_name][i + 1] / part[self.pop_col_name][i + 1]  # 1-indexed dist identifiers
                if l_perc >= 0.5:
                    num_maj_latino = num_maj_latino + 1
            lmaj_ensemble.append(num_maj_latino)
            election_wins = self._party_win_updater(part)
            party_win_ensemble = {k: election_wins.get(k) for k, v in election_wins.items()}
            # party_win_ensemble.update(self._party_win_updater(part))  # TODO test this instead of above 2 lines

        print("Walk complete")
        return cutedge_ensemble, lmaj_ensemble, party_win_ensemble

