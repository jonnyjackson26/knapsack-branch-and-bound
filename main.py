def fractional_knapsack_bound(node, items, capacity):
    # Compute upper bound on profit by taking items greedily (fractional allowed)
    total_weight = node.weight
    total_profit = node.value
    idx = node.level
    while idx < len(items) and total_weight < capacity:
        value, weight, ratio = items[idx]
        if total_weight + weight <= capacity:
            total_weight += weight
            total_profit += value
        else:
            remain = capacity - total_weight
            total_profit += ratio * remain
            break
        idx += 1
    return total_profit
import heapq

class Node:
    def __init__(self, level=-1, value=0, weight=0, bound=0.0):
        self.level = level
        self.value = value
        self.weight = weight
        self.bound = bound


# read dataset (a.txt)

# find ratios of each

# sort by ratios

# create a tree with the left most side not including anything and the rightmost side including everything in order of highest ratio things.

#prune tree to remove branches that are higher than capacity 'C'.

# go down all the way the right side and find your tempMax

# backtrack and see if the fractional knapsack of the next node is higher than tempMax. if it is, go down that branch. If not, backtrack again.

def read_data(filename):
    items = []
    with open(f'{filename}.txt', 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                value, weight = map(int, parts)
                items.append((value, weight))
    capacity = items[0][1]
    return items[1:], capacity

def find_ratios_and_sort_by_them(items):
    # Compute value/weight ratio for each item
    items_with_ratio = [(value, weight, value/weight) for value, weight in items]
    # Sort by ratio descending
    sorted_items = sorted(items_with_ratio, key=lambda x: x[2], reverse=True)
    return sorted_items

def create_tree(items,capacity):
    q = [] #queue of nodes
    root = Node(level=0, value=0, weight=0, bound=0.0)
    q.append(root)

    while q:
        node = q.pop(0)
        print(f"Level: {node.level}, Value: {node.value}, Weight: {node.weight}")

        # If we've considered all items, skip expansion
        if node.level >= len(items):
            continue

        # --- Generate child nodes ---
        # Child 1: Take the current item
        value_with = node.value + items[node.level][0]
        weight_with = node.weight + items[node.level][1]
        # Prune branches that exceed capacity
        if weight_with <= capacity:
            child_with = Node(node.level + 1, value_with, weight_with, 0.0)
            # Compute bound for child_with using fractional knapsack
            child_with.bound = fractional_knapsack_bound(child_with, items, capacity)
            q.append(child_with)

        # Child 2: Do not take the current item
        value_without = node.value
        weight_without = node.weight
        child_without = Node(node.level + 1, value_without, weight_without, 0.0)
        # Compute bound for child_without using fractional knapsack
        child_without.bound = fractional_knapsack_bound(child_without, items, capacity)
        q.append(child_without)




def main():
    items, capacity = read_data("a")
    #print(items)
    print(capacity)

    items=find_ratios_and_sort_by_them(items)
    #print(items)

    tree=create_tree(items,capacity)
    print(tree)

    



if __name__=="__main__":
    main()