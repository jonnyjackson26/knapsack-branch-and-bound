# knapsack-branch-and-bound
### https://www.algorithmsilluminated.org/ 16.7

In this problem, each file describes an instance of the knapsack problem and has the format:
[knapsack_size][number_of_items]
[value_1] [weight_1]
[value_2] [weight_2]
...
You can assume that all numbers are positive. You should assume that item weights and the knapsack capacity are integers.
Test case: What is the value of an optimal solution to the knapsack instance described in this file? (Answer: 2493893)
Challenge data set: Repeat the previous problem for the knapsack instance described in this file. This instance is so big that the straightforward iterative implementation described in the book uses an infeasible amount of time and space. So you will have to be creative to compute an optimal solution. One idea is to go back to a recursive implementation, solving subproblems --- and, of course, caching the results to avoid redundant work --- only on an "as needed" basis. Also, be sure to think about appropriate data structures for storing and looking up solutions to subproblems.

# notes:
if, even if you cheat (fractional knapsack, which is n log n), you wont be able to get higher than your temp max, then you obviosuly dont even want to try to go down that branch.

# read dataset (a.txt)

# find ratios of each

# sort by ratios

# create a tree with the left most side not including anything and the rightmost side including everything in order of highest ratio things.

# prune tree to remove branches that are higher than capacity 'C'.

# go down all the way the right side and find your tempMax

# backtrack and see if the fractional knapsack of the next node is higher than tempMax. if it is, go down that branch. If not, backtrack again.


