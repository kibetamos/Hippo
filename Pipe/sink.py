def read_grid_from_file(filename):
    """ Reads the grid from a text file and returns a dictionary with coordinates. """
    grid = {}
    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = float('-inf'), float('-inf')

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) != 3:
                continue
            char, x, y = parts[0], int(parts[1]), int(parts[2])
            grid[(x, y)] = char
            min_x, min_y = min(min_x, x), min(min_y, y)
            max_x, max_y = max(max_x, x), max(max_y, y)

    # Adjust coordinates to have zero-based indexing if needed
    return grid, min_x, min_y, max_x, max_y

def connected_sinks(grid, min_x, min_y, max_x, max_y):
    from collections import deque

    # Define pipe connections
    connections = {
        '═': [(0, -1), (0, 1)],
        '║': [(-1, 0), (1, 0)],
        '╔': [(-1, 0), (0, 1)],
        '╗': [(-1, 0), (0, -1)],
        '╚': [(1, 0), (0, 1)],
        '╝': [(1, 0), (0, -1)],
        '╠': [(-1, 0), (1, 0), (0, 1)],
        '╣': [(-1, 0), (1, 0), (0, -1)],
        '╦': [(-1, 0), (0, 1), (0, -1)],
        '╩': [(1, 0), (0, 1), (0, -1)],
        '*': [(-1, 0), (1, 0), (0, 1), (0, -1)]
    }


    # Directional moves for up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    def in_bounds(x, y):
        return min_x <= x <= max_x and min_y <= y <= max_y
    
    def can_connect(c1, d, c2):
        """ Check if two cells can connect based on their pipe and direction """
        if c1 == '*' or c2 == '*':
            return True
        if c1 not in connections or c2 not in connections:
            return False
        return (-d[0], -d[1]) in connections[c2] and d in connections[c1]

    # Find the source and prepare BFS
    source = None
    for (x, y), char in grid.items():
        if char == '*':
            source = (x, y)
            break

    if not source:
        return []

    # BFS to find all reachable sinks
    visited = set()
    sinks = set()
    queue = deque([source])
    visited.add(source)
    
    while queue:
        x, y = queue.popleft()
        
        for d in directions:
            nx, ny = x + d[0], y + d[1]
            if in_bounds(nx, ny) and (nx, ny) not in visited:
                if (nx, ny) in grid and grid[nx, ny] != ' ' and can_connect(grid[x, y], d, grid[nx, ny]):
                    visited.add((nx, ny))
                    if grid[nx, ny] not in '*':
                        sinks.add(grid[nx, ny])
                    queue.append((nx, ny))
    
    return sorted(sinks)

# Usage example
filename = '/home/bench/Documents/projects/cloned/Hippo/Pipe/input.txt'  # replace with your actual filename
grid, min_x, min_y, max_x, max_y = read_grid_from_file(filename)
print(connected_sinks(grid, min_x, min_y, max_x, max_y))  # Outputs connected sinks
