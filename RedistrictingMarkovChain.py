from metrics import *

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
        self.bvap = bvap
        self.dem_party_name = dem_party_name
        self.rep_party_name = rep_party_name

    def _init_updaters(self):
        # Initialize population and vote updaters
        self.updaters = {
            "our cut edges": cut_edges,
            "population": Tally("TOTPOP", alias="population"),
            "democratic_votes": Tally("G20PRED", alias="democratic_votes"),
            "republican_votes": Tally("G20PRER", alias="republican_votes"),
            "HISP": Tally("HISP", alias="HISP"),
            "BVAP": Tally("BVAP", alias="BVAP"),
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

    def walk_the_run(self):
        cutedge_ensemble = []
        bmaj_ensemble = []
        lmaj_ensemble = []
        party_win_ensemble = []
        mmd_ensemble = []
        eg_ensemble = []
        pb_ensemble = []

        print("Walking the ensemble")
        for part in self.random_walk:
            # Calculate metrics for each state in the Markov Chain
            cutedge_ensemble.append(len(part["our cut edges"]))

            mmd_ensemble.append(mm(part, "G20PRE", "Democratic"))
            eg_ensemble.append(eg(part, "G20PRE"))
            pb_ensemble.append(pb(part, "G20PRE", "Democratic"))

            # Count black-majority districts
            bmaj_ensemble.append(md(part, self.bvap))

            # Count latino-majority districts
            lmaj_ensemble.append(md(part, self.hpop_col_name))

            # Count democratic-won districts
            party_win_ensemble.append(pd(part, "G20PRE", "Democratic"))

        print("Walk complete")
        return (cutedge_ensemble, lmaj_ensemble, bmaj_ensemble, party_win_ensemble,
                mmd_ensemble, eg_ensemble, pb_ensemble)
