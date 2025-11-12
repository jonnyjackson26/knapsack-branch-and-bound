import heapq

class Node:
    def __init__(self, level=-1, value=0, weight=0, bound=0.0):
        self.level = level
        self.value = value
        self.weight = weight
        self.bound = bound

    def __lt__(self, other):
        # For heapq (max-heap using negative bound)
        return self.bound > other.bound


def read_data(filename):
    items = []
    with open(f'{filename}.txt', 'r') as f:
        lines = f.readlines()
        first_line = lines[0].strip().split()
        capacity = int(first_line[0])
        num_items = int(first_line[1])
        for line in lines[1:]:
            parts = line.strip().split()
            if len(parts) == 2:
                value, weight = map(int, parts)
                items.append((value, weight))
    return items, capacity


def find_ratios_and_sort_by_them(items):
    items_with_ratio = [(v, w, v / w) for v, w in items]
    return sorted(items_with_ratio, key=lambda x: x[2], reverse=True)


def fractional_knapsack_bound(node, items, capacity):
    if node.weight >= capacity:
        return 0

    total_weight = node.weight
    bound = node.value
    idx = node.level

    while idx < len(items) and total_weight < capacity:
        value, weight, ratio = items[idx]
        if total_weight + weight <= capacity:
            total_weight += weight
            bound += value
        else:
            remain = capacity - total_weight
            bound += ratio * remain
            break
        idx += 1

    return bound


def branch_and_bound_knapsack(items, capacity):
    # Items are assumed sorted by ratio
    pq = []
    best_value = 0

    # Root node
    root = Node(level=0, value=0, weight=0)
    root.bound = fractional_knapsack_bound(root, items, capacity)
    heapq.heappush(pq, (-root.bound, root))  # max-heap by bound

    while pq:
        _, node = heapq.heappop(pq)

        if node.bound <= best_value:
            continue  # prune

        if node.level >= len(items):
            continue

        # Consider next item
        next_level = node.level + 1
        item_value, item_weight, _ = items[node.level]

        # --- Case 1: Include item ---
        include = Node(next_level, node.value + item_value, node.weight + item_weight)
        if include.weight <= capacity and include.value > best_value:
            best_value = include.value
        include.bound = fractional_knapsack_bound(include, items, capacity)
        if include.bound > best_value:
            heapq.heappush(pq, (-include.bound, include))

        # --- Case 2: Exclude item ---
        exclude = Node(next_level, node.value, node.weight)
        exclude.bound = fractional_knapsack_bound(exclude, items, capacity)
        if exclude.bound > best_value:
            heapq.heappush(pq, (-exclude.bound, exclude))

    return best_value


def main():
    items, capacity = read_data("a")
    items = find_ratios_and_sort_by_them(items)
    bestValue = branch_and_bound_knapsack(items, capacity)
    print(f"Maximum value for knapsack of capacity {capacity} = {bestValue}")


if __name__ == "__main__":
    main()
