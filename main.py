
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

def create_tree(items):
    pass

def prune_impossible_branches(tree, capacity):
    pass

def main():
    items, capacity = read_data("a")
    #print(items)
    print(capacity)

    items=find_ratios_and_sort_by_them(items)
    #print(items)

    tree=create_tree(items)

    tree=prune_impossible_branches(tree,capacity)
    print(tree)



if __name__=="__main__":
    main()