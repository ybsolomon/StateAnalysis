from metrics import *

import matplotlib.pyplot as plt
from gerrychain import GeographicPartition, constraints, MarkovChain, Election
from gerrychain.updaters import Tally, cut_edges
from gerrychain.accept import always_accept
from functools import partial
from gerrychain.proposals import propose_random_flip


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

    # TODO delete method ? OR move logic in chain run below
    def _party_win_updater(self, partition, party):
        # Validate party
        if not (party == "Democratic" or party == "Republican"):
            raise ValueError("Unknown party")

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

    def init_markov_chain(self, steps=10):
        self._init_updaters()
        initial_partition = GeographicPartition(
            self.graph,
            assignment="CD",
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

        return chain

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

            # Calculate metrics for each state in the Markov Chain
            mmd_ensemble.append(mm(part, "G20PRE", "Democratic"))
            eg_ensemble.append(eg(part, "G20PRE"))
            pb_ensemble.append(pb(part, "G20PRE", "Democratic"))

            for i in range(self.num_dist):
                # Count black-majority districts
                b_perc = part[self.bvap][i + 1] / part[self.pop_col_name][i + 1]  # 1-indexed dist identifiers
                if b_perc >= 0.5:
                    num_maj_latino = num_maj_latino + 1

                # Count latino-majority districts
                l_perc = part[self.hpop_col_name][i + 1] / part[self.pop_col_name][i + 1]  # 1-indexed dist identifiers
                if l_perc >= 0.5:
                    num_maj_latino = num_maj_latino + 1

                # Count democratic-won districts
                if part["democratic_votes"][i] > part["republican_votes"][i]:
                    num_democratic_maj += 1

            lmaj_ensemble.append(num_maj_latino)
            party_win_ensemble.append(num_democratic_maj)

        print("Walk complete")
        return cutedge_ensemble, lmaj_ensemble, party_win_ensemble


def plot_histograms(ensemble, filename):
    plt.figure()
    plt.hist(ensemble, align="left")
    plt.savefig(filename)
