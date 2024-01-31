class Maze:
    """
    Interprete the maze as an undirected graph.

    Attributes:
        world: A 2D list representing the maze layout with 0 for walls and 1 for open paths.
        adjacency_list: A dictionary to store the adjacency list representation of the graph.
    """
    def __init__(self, world):
        """
        Initializes tow Maze object with the given Matrix layout.
        Args:
            world (list[list[int]]): A 2D list representing the maze.
        """
        self.world = world
        self.adjacency_list = {}
        rows = len(world)
        cols = len(world[0])
        for i in range(rows):
            for j in range(cols):
                node_index = cols * i + j

                if j + 1 < cols:
                    if world[i][j] != 0 and world[i][j+1] != 0:
                        if node_index not in self.adjacency_list:
                            self.adjacency_list[node_index] = [(node_index + 1, 1)]
                        else:
                            self.adjacency_list[node_index].append((node_index + 1, 1))

                if j - 1 >= 0:
                    if world[i][j-1] != 0 and world[i][j] != 0:
                        if node_index not in self.adjacency_list:
                            self.adjacency_list[node_index] = [(node_index - 1, 1)]
                        else:
                            self.adjacency_list[node_index].append((node_index - 1, 1))

                if i + 1 < rows:
                    if world[i][j] != 0 and world[i+1][j] != 0:
                        if node_index not in self.adjacency_list:
                            self.adjacency_list[node_index] = [(node_index + cols, 1)]
                        else:
                            self.adjacency_list[node_index].append((node_index + cols, 1))

                if i - 1 >= 0:
                    if world[i-1][j] != 0 and world[i][j] != 0:
                        if node_index not in self.adjacency_list:
                            self.adjacency_list[node_index] = [(node_index - cols, 1)]
                        else:
                            self.adjacency_list[node_index].append((node_index - cols, 1))

    def shortest_path(self, start, end):
        """
        Find the shortest path between two nodes using Dijkstra's algorithm.

        Args:
            start (int): The starting node index.
            end (int): The destination node index.

        Returns:
            list[int]: A list of node indices representing the shortest path.
        """
        import heapq

        # Priority queue for Dijkstra's algorithm
        priority_queue = [(0, start)]
        # Dictionary to store the shortest distance from the start node to each node
        shortest_distances = {node: float('infinity') for node in self.adjacency_list}
        shortest_distances[start] = 0
        # Dictionary to store the previous node in the shortest path
        previous_nodes = {node: None for node in self.adjacency_list}

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_distance > shortest_distances[current_node]:
                continue

            for neighbor, weight in self.adjacency_list[current_node]:
                distance = current_distance + weight

                if distance < shortest_distances[neighbor]:
                    shortest_distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        path = []
        current_node = end

        while previous_nodes[current_node] is not None:
            path.append(current_node)
            current_node = previous_nodes[current_node]

        path.append(start)
        path.reverse()
        directions = self.get_directions(path)

        return self.mark_shortest_path(path), directions

    def mark_shortest_path(self, path):
        """
        Mark the shortest path on the maze.

        Args:
            path (list[int]): A list of node indices representing the shortest path.

        Returns:
            list[list[int]]: A modified maze layout with the shortest path marked.
        """
        marked_path = [row[:] for row in self.world]

        for node_index in path:
            i = node_index // len(self.world[0])
            j = node_index % len(self.world[0])
            marked_path[i][j] = "x"

        return marked_path

    def get_directions(self, path):
        """
        Get directions (N, S, E, W) from one node to the next in a path.

        Args:
            path (list[int]): A list of node indices representing the path.

        Returns:
            list[str]: A list of directions.
        """
        directions = []
        for i in range(len(path) - 1):
            current_node = path[i]
            next_node = path[i + 1]

            current_row, current_col = divmod(current_node, len(self.world[0]))
            next_row, next_col = divmod(next_node, len(self.world[0]))

            if current_row < next_row:
                directions.append("Go South for next 1 meter")
            elif current_row > next_row:
                directions.append("Go North for next 1 meter")
            elif current_col < next_col:
                directions.append("Go East for next 1 meter")
            elif current_col > next_col:
                directions.append("Go West for next 1 meter")

        return directions
