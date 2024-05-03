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
                 dem_col_name, rep_col_name, pop_col_name, hpop_col_name,
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
        self.dem_party_name = dem_party_name
        self.rep_party_name = rep_party_name

        self.blocks_df = gpd.read_file("./new_states/shapefiles/vt_election_df.shp")

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
        # self.updaters = {
        #     "our cut edges": cut_edges,
        #     self.pop_col_name: Tally(self.pop_col_name, alias=self.pop_col_name),
        #     self.hpop_col_name: Tally(self.hpop_col_name, alias=self.hpop_col_name),
        #     "democratic_votes": Tally(self.dem_col_name, alias="democratic_votes"),
        #     "republican_votes": Tally(self.rep_col_name, alias="republican_votes"),
        # }
        self.updaters = {
            "our cut edges": cut_edges,
            "population": Tally("TOTPOP", alias="population"),
            "democratic_votes": Tally("G20PRED", alias="democratic_votes"),
            "republican_votes": Tally("G20PRER", alias="republican_votes"),
        }
        # e = Election(self.election_name, {"Democratic": self.dem_col_name, "Republican": self.rep_col_name})
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
            assignment="SEN",
            updaters=self.updaters
        )
        self.initial_partition = initial_partition

    # def _calc_population(self):
    #     tot_pop = sum([self.graph.nodes()[v][self.pop_col_name] for v in self.graph.nodes()])
    #     self.ideal_pop = tot_pop / self.num_dist

    def init_markov_chain(self, steps=10):
        # my_updaters = {
        #     "population": Tally("TOTPOP", alias="population"),
        #     "democratic_votes": Tally("G20PRED", alias="democratic_votes"),
        #     "republican_votes": Tally("G20PRER", alias="republican_votes"),
        # }

        # elections = [
        #     Election("G20PRE", {"Democratic": "G20PRED", "Republican": "G20PRER"}),
        # ]
        # my_updaters.update(
        #     {election.name: election for election in elections}
        # )

        initial_partition = GeographicPartition(
            self.graph,
            assignment= "SEN",
            updaters=self.updaters
        )

        tot_pop = sum([self.graph.nodes()[v]['TOTPOP'] for v in self.graph.nodes()])
        num_dist = len(set(self.blocks_df['SEN'])) # Number of Congressional Districts in Illinois

        pop_tolerance = 0.7

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
            total_steps=10
        )

        self.random_walk = chain


    def walk_the_run(self):
        cutedge_ensemble = []
        lmaj_ensemble = []
        party_win_ensemble = []

        print("Walking the ensemble")
        for part in self.random_walk:
            cutedge_ensemble.append(len(part["our cut edges"]))

            num_maj_latino = 0
            num_democratic_maj = 0
            # for i in range(self.num_dist):
                # l_perc = part[self.hpop_col_name][i + 1] / part[self.pop_col_name][i + 1]  # 1-indexed dist identifiers
                # if l_perc >= 0.5:
                #     num_maj_latino = num_maj_latino + 1
            for i in set(self.blocks_df['SEN']):
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
