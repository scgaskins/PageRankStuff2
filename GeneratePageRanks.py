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


def printResults(results):
    names = ["HDX", "BRS", "MIL", "CEN", "SEW", "BER", "OGL", "RHD"]
    for i in range(len(results)):
        if results[i] is not None:
            print(names[i], results[i])
        else:
            print(f"{names[i]} N/A")
    print('\n')


def averageResults(a, b, c, d, e, f, g, h):
    names = ["HDX", "BRS", "MIL", "CEN", "SEW", "BER", "OGL", "RHD"]
    ranks = [1, 2, 3, 4, 5, 6, 7, 8]
    totals = []
    for i in range(8):
        totals.append((a[i] + b[i] + c[i] + d[i] + e[i] + f[i] + g[i] + h[i]) / 8)
    # for i in range(8):
    # print(names[i], totals[i])
    sorted_ranks = totals.copy()
    sorted_ranks.sort(reverse=True)
    for i in range(sorted_ranks.len()):
        for j in range(totals.len()):
            if sorted_ranks[i] == totals[j]:
                print(ranks[i], names[j], sorted_ranks[i])


if __name__ == '__main__':
    def print_all_pageranks(sport, sport_name):
        for i in range(len(sport)):
            print(f'{sport_name} {2013 + i} Season')
            season_matrix = Create_Matrix(sport[i])
            season_results, excluded_teams = get_pageRankVector(season_matrix.get_transpose())
            printResults(season_results)


    def main():
        print_all_pageranks(mensbaseball, "Baseball")
        print_all_pageranks(softball, "Softball")
        print_all_pageranks(menslacrosse, "Men's Lacrosse")
        print_all_pageranks(womenslacrosse, "Women's Lacrosse")


    main()
