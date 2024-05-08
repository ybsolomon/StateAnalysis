import statistics


# Mean-Median Difference
def mm(part, election, party):
    # Validate party
    if not (party == "Democratic" or party == "Republican"):
        raise ValueError("Unknown party")

    # Get the vote totals for the Democratic and Republican parties
    votes = part[election].percents(party)

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

    dem_wasted_votes = 0
    rep_wasted_votes = 0

    # Calculate the number of wasted votes for the Democratic and Republican parties
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
def pb(part, election, party):
    # Validate party
    if not (party == "Democratic" or party == "Republican"):
        raise ValueError("Unknown party")

    # Calculate party vote share
    votes_party = sum(part[election].votes(party))
    pop = sum(part[election].totals.values())
    vs_party = votes_party / pop

    # Get total votes per party
    total_votes_party = part[election].totals_for_party[party]
    totals = part[election].totals

    dist_above_vs = 0
    districts = len(totals)

    # Count districts vote percentages above party vote share
    for district, votes in totals.items():
        if (total_votes_party[district] / votes) > vs_party:
            dist_above_vs += 1

    # Calculate partisan bias
    partisan_bias = (dist_above_vs / districts) - 0.5

    return partisan_bias
