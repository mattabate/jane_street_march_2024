# Jane Street Puzzle March 2024

This repository contains a Python solution to the Jane Street Puzzle of March 2024. This puzzle challenged solvers to creatively partition a 9x9 grid following certain rules.

Before reading further, you should consider attempting the puzzle yourself, and thinking about the rules.

Puzzle Link: [Jane Street Puzzles - Hooks 10](https://www.janestreet.com/puzzles/hooks-10/)

## Puzzle Rules Overview

The "Hooks 10" puzzle requires solvers to partition a 9x9 grid into nine L-shaped regions. The solver must then place nine 9’s in one of the regions, eight 8’s in another, seven 7’s in another, and so on. Certain specific cells in the grid also impose sum constraints on adjacent cells, and the filled squares must form an orthogonally connected region. The puzzle's ultimate solution is an integer derived by multiplying specific values once all L-shaped regions are fully populated.

For detailed rules and the puzzle board, refer to the [Jane Street link](https://www.janestreet.com/puzzles/hooks-10/) provided above.

## Solution Approach

The main challenge of the puzzle is identifying the locations of the L shaped regions and which the integer to assign to each. Once the nine regions are identified with their corresponding integer, the puzzle is actually of reasonable difficulty so that it might be printed and solved in a few minutes with a pen.

Initially, I thought it wouldn't be computationally feasible to check every possible pairing of L shapes and integers, since there are 4<sup>8</sup> = 65,536 possible configurations of L regions and I assumed the number of ways you could tie integers to them was around the order of 9!. However, the actual number of ways to assign integers to regions is only (5 x 4)(4 x 3)(3 x 2)(2 x 1) = 2880, since it is true that certain regions are too small to accommodate larger numbers, e.g. nine 9's. At this point, a brute force search for the location of the L regions becomes both feasible and attractive.

The result is `main.py`, a Python script that searches for feasible configurations of L's and paired integers, given the sum constraints posed in the initial problem.

## Installation

No additional libraries are required beyond the Python Standard Library. The code is compatible with Python 3.6+.

## Usage Instructions

### Solving the Puzzle

To start the solution process, simply run the `main.py` script from your terminal. This script performs an exhaustive search to find configurations that satisfy the puzzle's constraints.

```sh
python3  main.py
```

### Expected Output

Of the initial 65536 x 2880 = 188,743,680 configurations, the search disqualifies all but 20 possibilities for the final configurations of L's and assignments of integers. All remaining configurations are saved to `solutions.json`. Additionally, cells for which there are only one option are printed to the user in the following representation:

```plaintext
[9, 9, 9, 9, 9, 9, 9, 9, 9]
[7, 7, 7, 7, 7, 7, 7, 7, 9]
[0, 0, 5, 5, 5, 5, 8, 7, 9]
[0, 0, 0, 0, 4, 0, 8, 7, 9]
[0, 0, 0, 0, 0, 0, 8, 7, 9]
[0, 0, 0, 0, 0, 0, 8, 7, 9]
[0, 0, 0, 0, 0, 0, 8, 7, 9]
[0, 6, 6, 6, 6, 0, 8, 7, 9]
[8, 8, 8, 8, 8, 8, 8, 7, 9]`
```

The above solution may be interpreted as, e.g., the largest L-region, which contains 17 squares must occupy the top row and the rightmost column, and this region must contain nine 9's, etc. At this point, the solver may attempt to solve the puzzle by hand using the puzzle board and the remaining constraints.

### Testing a Simplified Template

The user may also run the script `--test` flag set to `True`.

```sh
python3  main.py  --test  True
```

When the test flag is set to `True` the script performs the same search, now directed at the 5x5 example puzzle given on Jane Street Website. Note that the example puzzle actually has certain interesting features and considerations that the main puzzle does not: for example, a sum constraint that adds to 0.

### Performance

The script considers approximately 189 million different ways of placing L shaped regions with assigned integers, and disqualifies assignments which cannot are proven to fail to pass the sum constraints.

The search is optimized to the extent that the total search time took on a under 2 hours on a MacBook Pro with 16GB RAM and an M1 chip. In the end, only 20 configurations of the initial 200 million remain allowable.

## Contact Information
  
Email: <mabate13@gmail.com>
