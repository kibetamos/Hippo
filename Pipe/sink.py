def connected_sinks_from_file(file_path):
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
    
    def in_bounds(x, y, min_x, min_y, max_x, max_y):
        return min_x <= x <= max_x and min_y <= y <= max_y
    
    def can_connect(c1, d, c2):
        """ Check if two cells can connect based on their pipe and direction """
        if c1 == '*' or c2 == '*':
            return True
        if c1 not in connections or c2 not in connections:
            return False
        return (-d[0], -d[1]) in connections[c2] and d in connections[c1]

    # Read the grid from the file
    def read_grid_from_file(filename):
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

    grid, min_x, min_y, max_x, max_y = read_grid_from_file(file_path)

    # Find the source and prepare BFS
    source = None
    for (x, y), char in grid.items():
        if char == '*':
            source = (x, y)
            break

    if not source:
        return ''

    # BFS to find all reachable sinks
    visited = set()
    sinks = set()
    queue = deque([source])
    visited.add(source)
    
    while queue:
        x, y = queue.popleft()
        
        for d in directions:
            nx, ny = x + d[0], y + d[1]
            if in_bounds(nx, ny, min_x, min_y, max_x, max_y) and (nx, ny) not in visited:
                if (nx, ny) in grid and grid[nx, ny] != ' ' and can_connect(grid[x, y], d, grid[nx, ny]):
                    visited.add((nx, ny))
                    if grid[nx, ny] not in '*':
                        sinks.add(grid[nx, ny])
                    queue.append((nx, ny))
    
    return ''.join(sorted(sinks))

# Usage example:
file_path  = '/home/bench/Documents/projects/cloned/Hippo/Pipe/input.txt'  # replace with your actual filename
result = connected_sinks_from_file(file_path)
print(result)  # Outputs connected sinks as a sorted string