from fractions import *
from AVector import AVector
from AMatrix import AMatrix
from Matrices import *

damping = 0.85
dampingAdd = (1 - damping) / 8


def Create_Matrix(data):
    vectors = []
    for i in data:
        vectors.append(AVector(i))
    TheMatrix = AMatrix(vectors)
    return TheMatrix


def find_nonparticipating_teams(matrix):
    all_zero_teams = []
    for i in range(matrix.num_rows):
        all_zero = True
        for j in range(matrix.num_columns):
            if matrix[i][j] != 0 or matrix[j][i] != 0:
                all_zero = False
                break
        if all_zero:
            all_zero_teams.append(i)
    return all_zero_teams


def remove_nonparticipating_teams(matrix, non_participants):
    new_matrix = matrix
    index_adjustment = 0  # indices decrease if we remove one
    for team_index in non_participants:
        adjusted_index = team_index - index_adjustment
        new_matrix = new_matrix.find_matrix_without_row_column(adjusted_index, adjusted_index)
        index_adjustment += 1
    return new_matrix


def get_Noramlized_Eigenvector_of1(leMatrix):
    simplifiedMatrix = leMatrix.get_stochastic_matrix()
    pageRankVector = simplifiedMatrix.get_eigenvector(1)
    total = 0
    for i in pageRankVector:
        total += i
    PageRankValue = []
    for i in range(pageRankVector.size):
        pageRankVector[i] = pageRankVector[i] / total
        PageRankValue.append(float(pageRankVector[i]))
    return PageRankValue


def Dampeining(EigVec):
    withDamping = []
    for i in EigVec:
        withDamping.append(dampingAdd + damping * i)
    return (withDamping)


def add_non_participants_back_in(page_rank_values, non_participating_teams):
    added_back = []
    index_adjustment = 0
    for i in range(len(page_rank_values) + len(non_participating_teams)):
        if i in non_participating_teams:
            added_back.append(None)
            index_adjustment += 1
        else:
            added_back.append(page_rank_values[i-index_adjustment])
    return added_back


def get_pageRankVector(TheMatrix):
    non_participating_teams = find_nonparticipating_teams(TheMatrix)
    TheMatrix = remove_nonparticipating_teams(TheMatrix, non_participating_teams)
    Eigenvector = get_Noramlized_Eigenvector_of1(TheMatrix)
    PageRankValues = Dampeining(Eigenvector)
    PageRankValues = add_non_participants_back_in(PageRankValues, non_participating_teams)
    return PageRankValues, non_participating_teams


def sort_teams_by_rank(page_ranks, removed_teams, team_names):
    sorted_ranks = page_ranks.copy()
    while None in sorted_ranks:
        sorted_ranks.remove(None)
    sorted_ranks.sort(reverse=True)
    sorted_team_names = []
    for i in range(len(sorted_ranks)):
        for j in range(len(page_ranks)):
            if sorted_ranks[i] == page_ranks[j]:
                sorted_team_names.append(team_names[j])
    for team_index in removed_teams:
        sorted_team_names.append(team_names[team_index])
        sorted_ranks.append(None)
    return sorted_ranks, sorted_team_names


def printResults(results, removed_teams):
    names = ["HDX", "BRS", "MIL", "CEN", "SEW", "BER", "OGL", "RHD"]
    sorted_results, sorted_names = sort_teams_by_rank(results, removed_teams, names)
    for i in range(len(sorted_results)):
        if sorted_results[i] is not None:
            print(f"{i+1}. {sorted_names[i]} {sorted_results[i]}")
        else:
            print(f"{sorted_names[i]} N/A")
    print('\n')


def average_results_for_season(season_ranks):
    team_totals = [0] * len(season_ranks[0])
    total_seasons_teams_played = [0] * len(season_ranks[0])
    averaged_ranks = []
    non_participating_teams = []
    for season in season_ranks:
        for i in range(len(season)):
            if season[i] is not None:
                team_totals[i] += season[i]
                total_seasons_teams_played[i] += 1
    for team_index in range(len(team_totals)):
        if total_seasons_teams_played[team_index] > 0:
            averaged_ranks.append(team_totals[team_index] / total_seasons_teams_played[team_index])
        else:
            averaged_ranks.append(None)
            non_participating_teams.append(team_index)
    return averaged_ranks, non_participating_teams


if __name__ == '__main__':
    def print_all_pageranks(sport, sport_name):
        all_season_ranks = []
        for i in range(len(sport)):
            print(f'{sport_name} {2013 + i} Season')
            season_matrix = Create_Matrix(sport[i])
            season_results, excluded_teams = get_pageRankVector(season_matrix.get_transpose())
            printResults(season_results, excluded_teams)
            all_season_ranks.append(season_results)
        print(f'{sport_name} Ranks Averaged Across All Seasons')
        averaged_ranks, non_participants = average_results_for_season(all_season_ranks)
        printResults(averaged_ranks, non_participants)


    def main():
        print_all_pageranks(mensbaseball, "Baseball")
        print_all_pageranks(softball, "Softball")
        print_all_pageranks(menslacrosse, "Men's Lacrosse")
        print_all_pageranks(womenslacrosse, "Women's Lacrosse")


    main()
