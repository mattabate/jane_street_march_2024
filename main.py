"""Code to hepl solve the Jane Street puzzle for March 2024."""

import fire
import json
import tqdm

from itertools import combinations, permutations


TEMPLATE = [
    ((0, 1), 18),
    ((0, 6), 7),
    ((1, 4), 12),
    ((2, 2), 9),
    ((2, 7), 31),
    ((4, 1), 5),
    ((4, 3), 11),
    ((4, 5), 22),
    ((4, 7), 22),
    ((6, 1), 9),
    ((6, 6), 19),
    ((7, 4), 14),
    ((8, 2), 22),
    ((8, 7), 15),
]
TEST_TEMPLATE = [
    ((0, 0), 0),
    ((1, 2), 9),
    ((1, 4), 7),
    ((2, 0), 8),
    ((3, 2), 15),
    ((3, 4), 12),
    ((4, 0), 10),
]


def transpose(grid: list[list[int]]) -> list[list[int]]:
    """
    Transpose a 2D grid.
    """

    return [[row[i] for row in grid] for i in range(len(grid[0]))]


def list_2_grid(grid_list: list[int], num_order: list[int]) -> list[list[int]]:
    """
    Convert a list of integers to a 2D grid. 4^8 = 65536 possible grids.
    """

    # all need to be 0, 1, 2, 3
    assert all(1 <= x <= 4 for x in grid_list)

    template = [[1]]

    for i in range(len(grid_list)):
        if grid_list[i] == 1:
            template.insert(0, [num_order[i]] * len(template[0]))
            template = transpose(template)
            template.append([num_order[i]] * len(template[0]))
            template = transpose(template)
        if grid_list[i] == 2:
            template.insert(0, [num_order[i]] * len(template[0]))
            template = transpose(template)
            template.insert(0, [num_order[i]] * len(template[0]))
            template = transpose(template)
        if grid_list[i] == 3:
            template.append([num_order[i]] * len(template[0]))
            template = transpose(template)
            template.insert(0, [num_order[i]] * len(template[0]))
            template = transpose(template)
        if grid_list[i] == 4:
            template.append([num_order[i]] * len(template[0]))
            template = transpose(template)
            template.append([num_order[i]] * len(template[0]))
            template = transpose(template)

    return template


def combinations_of_4m(m) -> list[list[int]]:
    """generate all lists of length m with all entries are in 1, 2, 3, 4."""

    def _append(m, current=[], result=[]) -> None:
        """Recursive implementation"""
        if m == 0:
            result.append(current)
            return None
        for digit in range(1, 5):
            _append(m - 1, current + [digit], result)
        return None

    result = []
    _append(m, [], result)
    return result


def sum_of_combinations(numbers):
    # Using a set to avoid duplicate sums
    sums_set = set()

    # Generate combinations of all lengths and calculate their sums
    for r in range(1, len(numbers) + 1):
        for combo in combinations(numbers, r):
            sums_set.add(sum(combo))

    # Convert the set to a sorted list before returning
    return sorted(list(sums_set))


def process_grid(
    grid: list[list[int]], template: list[tuple[tuple[int, int], int]]
) -> bool:
    """
    Process a grid and check if it fits with the numbers in the template.
    """
    legnth = len(grid)

    for pos, value in template:
        if grid[pos[0]][pos[1]] == 1:
            return False

        nums = []
        if pos[0] > 0:
            nums.append(grid[pos[0] - 1][pos[1]])
        if pos[0] < legnth - 1:
            nums.append(grid[pos[0] + 1][pos[1]])
        if pos[1] > 0:
            nums.append(grid[pos[0]][pos[1] - 1])
        if pos[1] < legnth - 1:
            nums.append(grid[pos[0]][pos[1] + 1])

        if value not in sum_of_combinations(nums) and value != 0:
            return False

    return True


def all_permutations(lwr=2, upr=9):
    numbers = range(lwr, upr + 1)  # Numbers from 2 to 9
    all_perms = [list(perm) for perm in permutations(numbers)]

    return all_perms


def main(
    test: bool = False,
):

    if test:
        k_size_grid = 5
        save_file = "test_solutions.json"
        template = TEST_TEMPLATE
    else:
        k_size_grid = 9
        save_file = "solutions.json"
        template = TEMPLATE

    combs = combinations_of_4m(k_size_grid - 1)

    num_orders = all_permutations(lwr=2, upr=k_size_grid)
    new_num_orders = []
    for num_order in num_orders:
        for i in range(len(num_order)):
            if num_order[i] > 2 * (i + 1) + 1:
                grid_list = combs[0]
                grid = list_2_grid(grid_list, num_order)
                break
        else:
            new_num_orders.append(num_order)

    num_orders = new_num_orders

    grid_work_set = []
    num_work_set = []
    for num_order in tqdm.tqdm(num_orders):
        for grid_list in combs:
            grid_list.reverse()
            grid = list_2_grid(grid_list, num_order)

            if process_grid(grid, template):
                grid_work_set.append(grid)
                tupples = [(num_order[i], grid_list[i]) for i in range(len(num_order))]
                num_work_set.append(tupples)

                with open(save_file, "w") as f:
                    json.dump(
                        {"grids": grid_work_set, "atts": num_work_set}, f, indent=1
                    )

    with open(save_file) as f:
        feasible_templates = json.load(f)

    grids = feasible_templates["grids"]

    all_templates = [[0] * k_size_grid for _ in range(k_size_grid)]

    for i in range(k_size_grid):
        for j in range(k_size_grid):
            cell = None
            for grid in grids:
                if not cell:
                    cell = grid[i][j]
                elif cell != grid[i][j]:
                    break
            else:
                all_templates[i][j] = cell

    print("Number of feasible combinations of L shapes:", len(grids))
    print("All feasible grids fit the form:")
    for i in all_templates:
        print(i)


if __name__ == "__main__":
    fire.Fire(main)
