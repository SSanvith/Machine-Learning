class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def a_star_search(grid, start, end):
    """
    Returns a list of tuples as a path from the given start to the given end in the given grid.
    Returns None if no path is found.
    """
    
    # Create start and end nodes
    start_node = Node(None, start)
    end_node = Node(None, end)

    # Initialize both open and closed lists
    open_list = []
    closed_list = []

    # Add the start node to the open list
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:
        # Get the node with the lowest f_cost
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # --- Goal Check ---
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # --- Generate Children ---
        children = []
        # Adjacent squares (no diagonals)
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            
            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within grid range
            if not (0 <= node_position[0] < len(grid) and 0 <= node_position[1] < len(grid[0])):
                continue

            # Make sure walkable terrain
            if grid[node_position[0]][node_position[1]] != 0:
                continue
            
            # Create new node
            new_node = Node(current_node, node_position)
            children.append(new_node)

        # Loop through children
        for child in children:
            
            # Child is on the closed list
            if child in closed_list:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            # Heuristic: Manhattan distance
            child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])
            child.f = child.g + child.h

            # Child is already in the open list with a higher g_cost
            if any(open_node for open_node in open_list if child == open_node and child.g > open_node.g):
                continue
            
            # Add the child to the open list
            open_list.append(child)
            
    return None # Path not found

def main():
    """Example of how to use the a_star_search function"""
    
    # Define the grid (0 = walkable, 1 = obstacle)
    grid = [
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], # A walkable "bridge"
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    
    start = (0, 0)
    end = (8, 7)

    path = a_star_search(grid, start, end)
    
    if path:
        print(f"Path found from {start} to {end}:")
        print(path)
        # Optional: Print the grid with the path
        for step in path:
            grid[step[0]][step[1]] = '*'
        for row in grid:
            print(" ".join(map(str, row)))
    else:
        print(f"No path found from {start} to {end}.")

if __name__ == '__main__':
    main()