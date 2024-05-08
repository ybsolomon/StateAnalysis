import statistics

import matplotlib.pyplot as plt
from gerrychain import GeographicPartition, Graph, constraints, MarkovChain, Election
from gerrychain.updaters import Tally, cut_edges
# from gerrychain.proposals import recom
from gerrychain.accept import always_accept
from functools import partial
from gerrychain.proposals import propose_random_flip

from geopandas import gpd


class RedistrictingMarkovChain(object):
    def __init__(self, graph, num_dist, assignment, election_name,
                 dem_col_name, rep_col_name, pop_col_name, hpop_col_name, bvap,
                 dem_party_name="Democratic", rep_party_name="Republican", pop_tolerance=0.10):
        self.graph = graph
        self.initial_partition = None
        self.updaters = {}
        self.random_walk = None

        self.pop_tolerance = pop_tolerance
        self.num_dist = num_dist

        self.assignment = assignment
        self.election_name = election_name
        self.dem_col_name = dem_col_name
        self.rep_col_name = rep_col_name
        self.pop_col_name = pop_col_name
        self.hpop_col_name = hpop_col_name
        self.bvap = bvap
        self.dem_party_name = dem_party_name
        self.rep_party_name = rep_party_name

    def _party_win_updater(self, partition):
        dem_shares = partition[self.election_name].percents("Democratic")
        # dem_seats = partition[self.election_name].seats(self.dem_party_name)
        # rep_shares = partition[self.election_name].percents(self.rep_party_name)
        # rep_seats = partition[self.election_name].seats(self.rep_party_name)
        party_wins = 0
        for dist in dem_shares:
            if dist >= 0.5:
                party_wins += 1
        return party_wins

    def _init_updaters(self):
        self.updaters = {
            "our cut edges": cut_edges,
            "population": Tally("TOTPOP", alias="population"),
            "democratic_votes": Tally("G20PRED", alias="democratic_votes"),
            "republican_votes": Tally("G20PRER", alias="republican_votes"),
        }

        elections = [
            Election("G20PRE", {"Democratic": "G20PRED", "Republican": "G20PRER"}),
        ]
        self.updaters.update(
            {election.name: election for election in elections}
        )

    def init_partition(self):
        self._init_updaters()
        initial_partition = GeographicPartition(
            self.graph,
            assignment="CD",
            updaters=self.updaters
        )
        self.initial_partition = initial_partition

        return initial_partition

    def init_markov_chain(self, steps=10):
        initial_partition = GeographicPartition(
            self.graph,
            assignment= "CD",
            updaters=self.updaters
        )

        pop_tolerance = 0.02

        proposal = partial(
            propose_random_flip,
        )

        population_constraint = constraints.within_percent_of_ideal_population(
            initial_partition,
            pop_tolerance,
            pop_key="population"
        )

        chain = MarkovChain(
            proposal=proposal,
            constraints=[population_constraint],
            accept=always_accept,
            initial_state=initial_partition,
            total_steps=steps
        )

        self.random_walk = chain

    def walk_the_run(self):
        cutedge_ensemble = []
        lmaj_ensemble = []
        party_win_ensemble = []
        mmd_ensemble = []
        eg_ensemble = []
        pb_ensemble = []

        print("Walking the ensemble")
        for part in self.random_walk:
            cutedge_ensemble.append(len(part["our cut edges"]))

            num_maj_latino = 0
            num_democratic_maj = 0

            mmd_ensemble.append(mm(part, "G20PRE", "Democratic"))
            eg_ensemble.append(eg(part, "G20PRE"))
            pb_ensemble.append(pb(part, "G20PRE"))

            for i in range(self.num_dist):
                b_perc = part[self.bvap][i + 1] / part[self.pop_col_name][i + 1]  # 1-indexed dist identifiers
                if b_perc >= 0.5:
                    num_maj_latino = num_maj_latino + 1

                l_perc = part[self.hpop_col_name][i + 1] / part[self.pop_col_name][i + 1]  # 1-indexed dist identifiers
                if l_perc >= 0.5:
                    num_maj_latino = num_maj_latino + 1

            # for i in set(self.blocks_df['SEN']):
                if part["democratic_votes"][i] > part["republican_votes"][i]:
                    num_democratic_maj += 1

            lmaj_ensemble.append(num_maj_latino)
            # party_win_ensemble.append(self._party_win_updater(part))
            party_win_ensemble.append(num_democratic_maj)

        print("Walk complete")
        return cutedge_ensemble, lmaj_ensemble, party_win_ensemble


def plot_histograms(ensemble, filename):
    plt.figure()
    plt.hist(ensemble, align="left")
    plt.savefig(filename)


# MM is directly proportional to the gerymandering of the districting plan
def mm(part, election, party):
    # Get the vote totals for the Democratic and Republican parties
    if party == "Democratic":
        votes = part[election].percents("Democratic")
    else:
        votes = part[election].percents("Republican")

    # Calculate the mean-median difference
    mean_median_diff = statistics.median(votes) - statistics.mean(votes)

    return mean_median_diff


# Efficiency Gap
def eg(part, election):
    # Get the vote totals for the Democratic and Republican parties
    dem_votes = list(part[election].totals_for_party['Democratic'].values())
    rep_votes = list(part[election].totals_for_party['Republican'].values())

    winning_areas = set()

    # Get winning areas
    for i in range(len(dem_votes)):
        if dem_votes[i] >= rep_votes[i]:
            winning_areas.add(i)

    # Calculate the number of wasted votes for the Democratic and Republican parties
    dem_wasted_votes = 0
    rep_wasted_votes = 0

    for i in range(len(dem_votes)):
        if i in winning_areas:
            dem_wasted_votes += dem_votes[i] - (0.5 * (dem_votes[i] + rep_votes[i]))
            rep_wasted_votes += rep_votes[i]
        else:
            dem_wasted_votes += dem_votes[i]
            rep_wasted_votes += rep_votes[i] - (0.5 * (dem_votes[i] + rep_votes[i]))

    # Calculate the efficiency gap
    efficiency_gap = (rep_wasted_votes - dem_wasted_votes) / sum(dem_votes + rep_votes)

    return efficiency_gap


# Partisan Bias
def pb(part, election):
    votes_dem = sum(part[election].votes("Democratic"))
    pop = sum(part[election].totals.values())
    vs_dem = votes_dem / pop

    total_votes_dem = part[election].totals_for_party["Democratic"]
    totals = part[election].totals

    dist_above_vs = 0
    districts = len(totals)

    for district, votes in totals.items():
        if (total_votes_dem[district] / votes) > vs_dem:
            dist_above_vs += 1

    pb = (dist_above_vs / districts) - 0.5

    return pb
