"""
Pathfinding Algorithms Module
Implements DFS, BFS, Dijkstra, A*, and Greedy Best-First Search
"""
from typing import List, Tuple, Optional, Callable, Set, Dict
from collections import deque
import heapq
import math
from src.maze import Maze, CellType
from src.metrics import MetricsTracker, AlgorithmMetrics


class PathfindingAlgorithms:
    """
    Collection of pathfinding algorithms with visualization support
    """
    
    def __init__(self, maze: Maze):
        """
        Initialize pathfinding algorithms with a maze
        
        Args:
            maze: Maze object to solve
        """
        self.maze = maze
        self.visualization_callback: Optional[Callable] = None
    
    def set_visualization_callback(self, callback: Callable):
        """
        Set callback function for visualization
        
        Args:
            callback: Function to call for each step (row, col, state)
        """
        self.visualization_callback = callback
    
    def _visualize_step(self, row: int, col: int, state: str):
        """Call visualization callback if set"""
        if self.visualization_callback:
            self.visualization_callback(row, col, state)
    
    def _reconstruct_path(self, came_from: Dict[Tuple[int, int], Tuple[int, int]], 
                         current: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Reconstruct path from start to end using came_from dictionary
        
        Args:
            came_from: Dictionary mapping each node to its predecessor
            current: End node
            
        Returns:
            List of coordinates representing the path
        """
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
    
    # ===== DFS (Stack-based) =====
    def dfs(self) -> AlgorithmMetrics:
        """
        Depth-First Search using explicit stack
        
        Time Complexity: O(V + E) where V = vertices, E = edges
        Space Complexity: O(V) for the stack and visited set
        
        Returns:
            AlgorithmMetrics object with performance data
        """
        tracker = MetricsTracker()
        tracker.start_tracking()
        
        start = self.maze.start
        end = self.maze.end
        
        # Stack for DFS (LIFO)
        stack = [start]
        visited: Set[Tuple[int, int]] = {start}
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        
        found = False
        
        while stack:
            tracker.update_frontier_size(len(stack))
            current = stack.pop()
            tracker.increment_nodes()
            
            self._visualize_step(current[0], current[1], 'exploring')
            
            if current == end:
                found = True
                break
            
            # Explore neighbors
            for neighbor in self.maze.get_neighbors(current[0], current[1]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
                    came_from[neighbor] = current
                    self._visualize_step(neighbor[0], neighbor[1], 'visited')
        
        # Reconstruct path
        path = []
        if found:
            path = self._reconstruct_path(came_from, end)
            for row, col in path:
                if (row, col) != start and (row, col) != end:
                    self._visualize_step(row, col, 'path')
        
        return tracker.create_metrics(
            algorithm_name="DFS (Stack)",
            path=path,
            time_complexity="O(V + E)",
            space_complexity="O(V)",
            is_optimal=False  # DFS does not guarantee shortest path
        )
    
    # ===== BFS (Queue-based) =====
    def bfs(self) -> AlgorithmMetrics:
        """
        Breadth-First Search using queue
        
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        
        Returns:
            AlgorithmMetrics object with performance data
        """
        tracker = MetricsTracker()
        tracker.start_tracking()
        
        start = self.maze.start
        end = self.maze.end
        
        # Queue for BFS (FIFO)
        queue = deque([start])
        visited: Set[Tuple[int, int]] = {start}
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        
        found = False
        
        while queue:
            tracker.update_frontier_size(len(queue))
            current = queue.popleft()
            tracker.increment_nodes()
            
            self._visualize_step(current[0], current[1], 'exploring')
            
            if current == end:
                found = True
                break
            
            # Explore neighbors
            for neighbor in self.maze.get_neighbors(current[0], current[1]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    came_from[neighbor] = current
                    self._visualize_step(neighbor[0], neighbor[1], 'visited')
        
        # Reconstruct path
        path = []
        if found:
            path = self._reconstruct_path(came_from, end)
            for row, col in path:
                if (row, col) != start and (row, col) != end:
                    self._visualize_step(row, col, 'path')
        
        return tracker.create_metrics(
            algorithm_name="BFS (Queue)",
            path=path,
            time_complexity="O(V + E)",
            space_complexity="O(V)",
            is_optimal=True  # BFS guarantees shortest path in unweighted graphs
        )
    
    # ===== Dijkstra's Algorithm (Priority Queue / Min-Heap) =====
    def dijkstra(self) -> AlgorithmMetrics:
        """
        Dijkstra's Algorithm using Min-Heap (Priority Queue)
        
        Time Complexity: O((V + E) log V)
        Space Complexity: O(V)
        
        Returns:
            AlgorithmMetrics object with performance data
        """
        tracker = MetricsTracker()
        tracker.start_tracking()
        
        start = self.maze.start
        end = self.maze.end
        
        # Priority queue: (cost, node)
        pq = [(0, start)]
        visited: Set[Tuple[int, int]] = set()
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        cost_so_far: Dict[Tuple[int, int], float] = {start: 0}
        
        found = False
        
        while pq:
            tracker.update_frontier_size(len(pq))
            current_cost, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            visited.add(current)
            tracker.increment_nodes()
            
            self._visualize_step(current[0], current[1], 'exploring')
            
            if current == end:
                found = True
                break
            
            # Explore neighbors
            for neighbor in self.maze.get_neighbors(current[0], current[1]):
                new_cost = current_cost + self.maze.get_edge_weight(current, neighbor)
                
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(pq, (new_cost, neighbor))
                    came_from[neighbor] = current
                    self._visualize_step(neighbor[0], neighbor[1], 'visited')
        
        # Reconstruct path
        path = []
        if found:
            path = self._reconstruct_path(came_from, end)
            for row, col in path:
                if (row, col) != start and (row, col) != end:
                    self._visualize_step(row, col, 'path')
        
        return tracker.create_metrics(
            algorithm_name="Dijkstra (Min-Heap)",
            path=path,
            time_complexity="O((V + E) log V)",
            space_complexity="O(V)",
            is_optimal=True  # Dijkstra guarantees optimal path
        )
    
    # ===== Heuristic Functions =====
    @staticmethod
    def manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """
        Manhattan distance heuristic (L1 norm)
        Good for 4-directional movement
        """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    @staticmethod
    def euclidean_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """
        Euclidean distance heuristic (L2 norm)
        Straight-line distance
        """
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
    
    @staticmethod
    def chebyshev_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """
        Chebyshev distance heuristic (L∞ norm)
        Good for 8-directional movement
        """
        return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))
    
    # ===== A* Algorithm =====
    def astar(self, heuristic: str = 'manhattan') -> AlgorithmMetrics:
        """
        A* Algorithm with selectable heuristic
        
        Time Complexity: O(E) in worst case, O(b^d) average
        Space Complexity: O(V)
        
        Args:
            heuristic: Heuristic function ('manhattan', 'euclidean', 'chebyshev')
            
        Returns:
            AlgorithmMetrics object with performance data
        """
        tracker = MetricsTracker()
        tracker.start_tracking()
        
        # Select heuristic function
        heuristic_func = {
            'manhattan': self.manhattan_distance,
            'euclidean': self.euclidean_distance,
            'chebyshev': self.chebyshev_distance
        }.get(heuristic, self.manhattan_distance)
        
        start = self.maze.start
        end = self.maze.end
        
        # Priority queue: (f_score, g_score, node)
        pq = [(heuristic_func(start, end), 0, start)]
        visited: Set[Tuple[int, int]] = set()
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        g_score: Dict[Tuple[int, int], float] = {start: 0}
        
        found = False
        
        while pq:
            tracker.update_frontier_size(len(pq))
            f, current_g, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            visited.add(current)
            tracker.increment_nodes()
            
            self._visualize_step(current[0], current[1], 'exploring')
            
            if current == end:
                found = True
                break
            
            # Explore neighbors
            for neighbor in self.maze.get_neighbors(current[0], current[1]):
                new_g = current_g + self.maze.get_edge_weight(current, neighbor)
                
                if neighbor not in g_score or new_g < g_score[neighbor]:
                    g_score[neighbor] = new_g
                    h = heuristic_func(neighbor, end)
                    f_score = new_g + h
                    heapq.heappush(pq, (f_score, new_g, neighbor))
                    came_from[neighbor] = current
                    self._visualize_step(neighbor[0], neighbor[1], 'visited')
        
        # Reconstruct path
        path = []
        if found:
            path = self._reconstruct_path(came_from, end)
            for row, col in path:
                if (row, col) != start and (row, col) != end:
                    self._visualize_step(row, col, 'path')
        
        return tracker.create_metrics(
            algorithm_name=f"A* ({heuristic.capitalize()})",
            path=path,
            time_complexity="O(b^d)",
            space_complexity="O(V)",
            is_optimal=True,  # A* is optimal with admissible heuristic
            heuristic=heuristic.capitalize()
        )
    
    # ===== Greedy Best-First Search =====
    def greedy_best_first(self, heuristic: str = 'manhattan') -> AlgorithmMetrics:
        """
        Greedy Best-First Search
        Uses only heuristic (no path cost consideration)
        
        Time Complexity: O(b^m) where m is maximum depth
        Space Complexity: O(V)
        
        Args:
            heuristic: Heuristic function ('manhattan', 'euclidean', 'chebyshev')
            
        Returns:
            AlgorithmMetrics object with performance data
        """
        tracker = MetricsTracker()
        tracker.start_tracking()
        
        # Select heuristic function
        heuristic_func = {
            'manhattan': self.manhattan_distance,
            'euclidean': self.euclidean_distance,
            'chebyshev': self.chebyshev_distance
        }.get(heuristic, self.manhattan_distance)
        
        start = self.maze.start
        end = self.maze.end
        
        # Priority queue: (h_score, node)
        pq = [(heuristic_func(start, end), start)]
        visited: Set[Tuple[int, int]] = set()
        came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
        
        found = False
        
        while pq:
            tracker.update_frontier_size(len(pq))
            h, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            visited.add(current)
            tracker.increment_nodes()
            
            self._visualize_step(current[0], current[1], 'exploring')
            
            if current == end:
                found = True
                break
            
            # Explore neighbors
            for neighbor in self.maze.get_neighbors(current[0], current[1]):
                if neighbor not in visited:
                    h_score = heuristic_func(neighbor, end)
                    heapq.heappush(pq, (h_score, neighbor))
                    if neighbor not in came_from:
                        came_from[neighbor] = current
                    self._visualize_step(neighbor[0], neighbor[1], 'visited')
        
        # Reconstruct path
        path = []
        if found:
            path = self._reconstruct_path(came_from, end)
            for row, col in path:
                if (row, col) != start and (row, col) != end:
                    self._visualize_step(row, col, 'path')
        
        return tracker.create_metrics(
            algorithm_name=f"Greedy Best-First ({heuristic.capitalize()})",
            path=path,
            time_complexity="O(b^m)",
            space_complexity="O(V)",
            is_optimal=False,  # Greedy is not optimal
            heuristic=heuristic.capitalize()
        )
    
    # ===== Bidirectional Search (Bonus) =====
    def bidirectional_search(self) -> AlgorithmMetrics:
        """
        Bidirectional BFS - searches from both start and end simultaneously
        
        Time Complexity: O(b^(d/2))
        Space Complexity: O(b^(d/2))
        
        Returns:
            AlgorithmMetrics object with performance data
        """
        tracker = MetricsTracker()
        tracker.start_tracking()
        
        start = self.maze.start
        end = self.maze.end
        
        # Two queues for forward and backward search
        forward_queue = deque([start])
        backward_queue = deque([end])
        
        forward_visited: Dict[Tuple[int, int], Tuple[int, int]] = {start: None}
        backward_visited: Dict[Tuple[int, int], Tuple[int, int]] = {end: None}
        
        meeting_point = None
        
        while forward_queue and backward_queue:
            tracker.update_frontier_size(len(forward_queue) + len(backward_queue))
            
            # Forward search
            if forward_queue:
                current = forward_queue.popleft()
                tracker.increment_nodes()
                self._visualize_step(current[0], current[1], 'exploring')
                
                # Check if paths meet
                if current in backward_visited:
                    meeting_point = current
                    break
                
                for neighbor in self.maze.get_neighbors(current[0], current[1]):
                    if neighbor not in forward_visited:
                        forward_visited[neighbor] = current
                        forward_queue.append(neighbor)
                        self._visualize_step(neighbor[0], neighbor[1], 'visited')
            
            # Backward search
            if backward_queue:
                current = backward_queue.popleft()
                tracker.increment_nodes()
                self._visualize_step(current[0], current[1], 'exploring')
                
                # Check if paths meet
                if current in forward_visited:
                    meeting_point = current
                    break
                
                for neighbor in self.maze.get_neighbors(current[0], current[1]):
                    if neighbor not in backward_visited:
                        backward_visited[neighbor] = current
                        backward_queue.append(neighbor)
                        self._visualize_step(neighbor[0], neighbor[1], 'visited')
        
        # Reconstruct path
        path = []
        if meeting_point:
            # Build forward path
            forward_path = []
            current = meeting_point
            while current is not None:
                forward_path.append(current)
                current = forward_visited[current]
            forward_path.reverse()
            
            # Build backward path
            backward_path = []
            current = backward_visited[meeting_point]
            while current is not None:
                backward_path.append(current)
                current = backward_visited[current]
            
            path = forward_path + backward_path
            
            for row, col in path:
                if (row, col) != start and (row, col) != end:
                    self._visualize_step(row, col, 'path')
        
        return tracker.create_metrics(
            algorithm_name="Bidirectional BFS",
            path=path,
            time_complexity="O(b^(d/2))",
            space_complexity="O(b^(d/2))",
            is_optimal=True
        )
