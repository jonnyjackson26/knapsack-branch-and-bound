import heapq  #heapq is used for the priority queue (max-heap)

# Node represents a state in the branch-and-bound tree
class Node:
    def __init__(self, level=-1, value=0, weight=0, bound=0.0):
        self.level = level      # Which item index we're considering
        self.value = value      # Total value so far
        self.weight = weight    # Total weight so far
        self.bound = bound      # Upper bound on best possible value from this node; the fractional knapsack of the node

    def __lt__(self, other): #less than
        # For heapq: we want a max-heap by bound, so we reverse the comparison
        return self.bound > other.bound



def read_data(filename):
    items = []
    with open(f'{filename}.txt', 'r') as f:
        lines = f.readlines()
        first_line = lines[0].strip().split()
        # First line: [knapsack_size] [number_of_items]
        # Remaining lines: [value] [weight] for each item
        capacity = int(first_line[0])
        num_items = int(first_line[1])
        for line in lines[1:]:
            parts = line.strip().split()
            if len(parts) == 2:
                value, weight = map(int, parts)
                items.append((value, weight))
    return items, capacity

def find_ratios_and_sort_by_them(items):
    # Calculates value/weight ratio for each item and sorts items by ratio (descending)
    items_with_ratio = [(v, w, v / w) for v, w in items]
    return sorted(items_with_ratio, key=lambda x: x[2], reverse=True)

# Computes the upper bound (best possible value) from a node using fractional knapsack. 
# the idea is "if i cheat (quick algorhtm) and dont even get higher than my current max, not cheating isnt even worth it"
def fractional_knapsack_bound(node, items, capacity):
    if node.weight >= capacity:
        return 0  # Overweight, can't add more

    total_weight = node.weight
    bound = node.value
    idx = node.level

    # Try to add items greedily by ratio
    while idx < len(items) and total_weight < capacity: #while theres still items and the bag isnt overflowing yet
        value, weight, ratio = items[idx]
        if total_weight + weight <= capacity:
            # Can take whole item
            total_weight += weight
            bound += value
        else:
            # Take fraction of item to fill knapsack
            remain = capacity - total_weight
            bound += ratio * remain
            break
        idx += 1

    return bound


def branch_and_bound_knapsack(items, capacity):
    pq = []  # priority queue
    tempMax = 0  # Track best value found

    # Start with root node (no items chosen yet)
    root = Node(level=0, value=0, weight=0)
    root.bound = fractional_knapsack_bound(root, items, capacity)
    heapq.heappush(pq, (-root.bound, root))  # max-heap by bound

    while pq:
        _, node = heapq.heappop(pq)  # Get node with highest bound

        # Prune if bound is not better than best found
        if node.bound <= tempMax:
            continue

        # If we've considered all items, skip
        if node.level >= len(items):
            continue

        #get the next node
        next_level = node.level + 1
        item_value, item_weight, _ = items[node.level] 

        # --- Case 1: Include item ---
        include = Node(next_level, node.value + item_value, node.weight + item_weight)
        if include.weight <= capacity and include.value > tempMax:
            tempMax = include.value  # Update best value if valid
        include.bound = fractional_knapsack_bound(include, items, capacity)
        if include.bound > tempMax:
            heapq.heappush(pq, (-include.bound, include))  # Explore further

        # --- Case 2: Exclude item ---
        exclude = Node(next_level, node.value, node.weight)
        exclude.bound = fractional_knapsack_bound(exclude, items, capacity)
        if exclude.bound > tempMax:
            heapq.heappush(pq, (-exclude.bound, exclude))  # Explore further

    return tempMax



# Main entry point
def main():
    items, capacity = read_data("b")
    items = find_ratios_and_sort_by_them(items)
    bestValue = branch_and_bound_knapsack(items, capacity)
    print(f"Maximum value for knapsack of capacity {capacity} = {bestValue}")


if __name__ == "__main__":
    main()
