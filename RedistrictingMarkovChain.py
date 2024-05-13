from metrics import *

import matplotlib.pyplot as plt
from gerrychain import GeographicPartition, constraints, MarkovChain, Election
from gerrychain.updaters import Tally, cut_edges
from gerrychain.accept import always_accept
from functools import partial
from gerrychain.proposals import propose_random_flip


class RedistrictingMarkovChain(object):
    def __init__(self, graph, num_dist, assignment, election_name,
                 dem_col_name, rep_col_name, pop_col_name, hpop_col_name,
                 bvap,  # TODO
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
        self.bvap = bvap  # TODO
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
        # Initialize population and vote updaters
        self.updaters = {
            "our cut edges": cut_edges,
            "population": Tally("TOTPOP", alias="population"),
            "democratic_votes": Tally("G20PRED", alias="democratic_votes"),
            "republican_votes": Tally("G20PRER", alias="republican_votes"),
            "HISP": Tally("HISP", alias="HISP"),
            "BVAP": Tally("BVAP", alias="BVAP"), # TODO keep column in shp file
        }

        # Initialize election updaters
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
        # Initialize updaters and partition
        self._init_updaters()
        initial_partition = GeographicPartition(
            self.graph,
            assignment="CD",
            updaters=self.updaters
        )
        self.initial_partition = initial_partition

        # Use random flips as the algorithm
        proposal = partial(
            propose_random_flip,
        )

        # Initialize population constraint
        population_constraint = constraints.within_percent_of_ideal_population(
            self.initial_partition,
            self.pop_tolerance,
            pop_key="population"
        )

        # Initialize Markov Chain
        chain = MarkovChain(
            proposal=proposal,
            constraints=[population_constraint],
            accept=always_accept,
            initial_state=self.initial_partition,
            total_steps=steps
        )

        self.random_walk = chain

        return chain

    def _calc_metrics(self):
        part_mmd = mm(self.random_walk.initial_state, "G20PRE", "Democratic")
        part_eg = eg(self.random_walk.initial_state, "G20PRE")
        part_pb = pb(self.random_walk.initial_state, "G20PRE", "Democratic")

        return part_mmd, part_eg, part_pb

    def walk_the_run(self):
        cutedge_ensemble = []
        bmaj_ensemble = []  # TODO
        lmaj_ensemble = []
        party_win_ensemble = []
        mmd_ensemble = []
        eg_ensemble = []
        pb_ensemble = []

        mm_init, eg_init, pb_init = self._calc_metrics()

        print("Walking the ensemble")
        for part in self.random_walk:
            cutedge_ensemble.append(len(part["our cut edges"]))

            # num_maj_latino = 0
            # num_maj_black = 0
            # num_democratic_maj = 0

            # Calculate metrics for each state in the Markov Chain
            mmd_ensemble.append(mm(part, "G20PRE", "Democratic"))
            eg_ensemble.append(eg(part, "G20PRE"))
            pb_ensemble.append(pb(part, "G20PRE", "Democratic"))

            # for i in range(self.num_dist):
            # Count black-majority districts
            num_maj_black = md(part, self.bvap)
                # b_perc = part[self.bvap][i + 1] / part["population"][i + 1]  # 1-indexed dist identifiers
                # if b_perc >= 0.5:
                #     num_maj_black = num_maj_black + 1

            # Count latino-majority districts
            num_maj_latino = md(part, self.hpop_col_name)
                # l_perc = part[self.hpop_col_name][i + 1] / part["population"][i + 1]  # 1-indexed dist identifiers
                # if l_perc >= 0.5:
                #     num_maj_latino = num_maj_latino + 1

            # Count democratic-won districts
            num_democratic_maj = pd(part, "G20PRE", "Democratic")
                # if part["democratic_votes"][i + 1] > part["republican_votes"][i + 1]:
                #     num_democratic_maj += 1

            bmaj_ensemble.append(num_maj_black)
            lmaj_ensemble.append(num_maj_latino)
            party_win_ensemble.append(num_democratic_maj)

        print("Walk complete")
        return cutedge_ensemble, lmaj_ensemble, bmaj_ensemble, party_win_ensemble, mmd_ensemble, eg_ensemble, pb_ensemble


# def plot_histograms(ensemble, filename):
#     plt.figure()
#     plt.hist(ensemble, align="left")
#     plt.savefig(filename)
