"""
Advanced Features Module
Dynamic obstacles, parallel execution, and advanced maze generation
"""
import threading
import time
from typing import List, Callable, Dict
from src.maze import Maze
from src.algorithms import PathfindingAlgorithms
from src.metrics import AlgorithmMetrics
import random


class DynamicMazeSolver:
    """
    Solver with dynamic obstacle support
    """
    
    def __init__(self, maze: Maze):
        """Initialize dynamic solver"""
        self.maze = maze
        self.obstacles: List[tuple] = []
        self.running = False
    
    def add_random_obstacles(self, count: int = 5):
        """
        Add random obstacles to the maze during pathfinding
        
        Args:
            count: Number of obstacles to add
        """
        for _ in range(count):
            row = random.randint(0, self.maze.rows - 1)
            col = random.randint(0, self.maze.cols - 1)
            
            # Don't place obstacles at start or end
            if (row, col) != self.maze.start and (row, col) != self.maze.end:
                self.maze.set_wall(row, col)
                self.obstacles.append((row, col))
    
    def clear_obstacles(self):
        """Clear all dynamic obstacles"""
        from src.maze import CellType
        for row, col in self.obstacles:
            self.maze.grid[row][col] = CellType.EMPTY.value
        self.obstacles.clear()
        self.maze._build_adjacency_list()


class ParallelAlgorithmRunner:
    """
    Run multiple algorithms in parallel and compare results
    """
    
    def __init__(self, maze: Maze):
        """Initialize parallel runner"""
        self.maze = maze
        self.results: Dict[str, AlgorithmMetrics] = {}
        self.threads: List[threading.Thread] = []
    
    def _run_algorithm(self, name: str, algorithm_func: Callable):
        """Thread worker to run an algorithm"""
        try:
            # Create a copy of the maze for thread safety
            import copy
            maze_copy = copy.deepcopy(self.maze)
            pathfinder = PathfindingAlgorithms(maze_copy)
            
            # Run algorithm
            metrics = algorithm_func(pathfinder)
            
            # Store results
            self.results[name] = metrics
            
        except Exception as e:
            print(f"Error in {name}: {e}")
    
    def run_all_parallel(self) -> Dict[str, AlgorithmMetrics]:
        """
        Run all algorithms in parallel
        
        Returns:
            Dictionary of algorithm name to metrics
        """
        self.results.clear()
        self.threads.clear()
        
        # Define algorithms to run
        algorithms = [
            ('DFS', lambda p: p.dfs()),
            ('BFS', lambda p: p.bfs()),
            ('Dijkstra', lambda p: p.dijkstra()),
            ('A* (Manhattan)', lambda p: p.astar('manhattan')),
            ('A* (Euclidean)', lambda p: p.astar('euclidean')),
            ('Greedy Best-First', lambda p: p.greedy_best_first('manhattan')),
            ('Bidirectional BFS', lambda p: p.bidirectional_search()),
        ]
        
        # Create threads
        for name, algo_func in algorithms:
            thread = threading.Thread(
                target=self._run_algorithm,
                args=(name, algo_func)
            )
            self.threads.append(thread)
        
        # Start all threads
        start_time = time.time()
        for thread in self.threads:
            thread.start()
        
        # Wait for all to complete
        for thread in self.threads:
            thread.join()
        
        total_time = time.time() - start_time
        
        print(f"\n✓ All algorithms completed in {total_time:.3f} seconds (parallel execution)")
        print(f"✓ {len(self.results)} algorithms executed successfully\n")
        
        return self.results


class AdvancedMazeGenerator:
    """
    Advanced maze generation algorithms
    """
    
    @staticmethod
    def generate_spiral_maze(maze: Maze):
        """Generate a spiral pattern maze"""
        from src.maze import CellType
        
        # Reset to empty
        maze.grid = [[CellType.EMPTY.value for _ in range(maze.cols)] for _ in range(maze.rows)]
        
        # Create spiral walls
        row_start, row_end = 0, maze.rows - 1
        col_start, col_end = 0, maze.cols - 1
        
        while row_start <= row_end and col_start <= col_end:
            # Top wall
            for col in range(col_start, col_end + 1, 2):
                if 0 <= row_start < maze.rows:
                    maze.grid[row_start][col] = CellType.WALL.value
            row_start += 2
            
            # Right wall
            for row in range(row_start, row_end + 1, 2):
                if 0 <= col_end < maze.cols:
                    maze.grid[row][col_end] = CellType.WALL.value
            col_end -= 2
            
            # Bottom wall
            if row_start <= row_end:
                for col in range(col_end, col_start - 1, -2):
                    if 0 <= row_end < maze.rows:
                        maze.grid[row_end][col] = CellType.WALL.value
                row_end -= 2
            
            # Left wall
            if col_start <= col_end:
                for row in range(row_end, row_start - 1, -2):
                    if 0 <= col_start < maze.cols:
                        maze.grid[row][col_start] = CellType.WALL.value
                col_start += 2
        
        # Set start and end
        maze.grid[maze.start[0]][maze.start[1]] = CellType.START.value
        maze.grid[maze.end[0]][maze.end[1]] = CellType.END.value
        maze._build_adjacency_list()
    
    @staticmethod
    def generate_room_maze(maze: Maze, room_count: int = 5):
        """Generate a maze with rooms connected by corridors"""
        from src.maze import CellType
        
        # Fill with walls
        maze.grid = [[CellType.WALL.value for _ in range(maze.cols)] for _ in range(maze.rows)]
        
        # Create rooms
        for _ in range(room_count):
            room_width = random.randint(3, 7)
            room_height = random.randint(3, 7)
            
            room_x = random.randint(1, maze.cols - room_width - 1)
            room_y = random.randint(1, maze.rows - room_height - 1)
            
            # Carve room
            for y in range(room_y, min(room_y + room_height, maze.rows)):
                for x in range(room_x, min(room_x + room_width, maze.cols)):
                    maze.grid[y][x] = CellType.EMPTY.value
        
        # Create corridors (simple random walk)
        for _ in range(maze.rows * maze.cols // 4):
            y = random.randint(1, maze.rows - 2)
            x = random.randint(1, maze.cols - 2)
            maze.grid[y][x] = CellType.EMPTY.value
        
        # Ensure start and end are accessible
        maze.grid[maze.start[0]][maze.start[1]] = CellType.EMPTY.value
        maze.grid[maze.end[0]][maze.end[1]] = CellType.EMPTY.value
        
        # Create path near start and end
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = maze.start[0] + dy, maze.start[1] + dx
            if 0 <= ny < maze.rows and 0 <= nx < maze.cols:
                maze.grid[ny][nx] = CellType.EMPTY.value
            
            ny, nx = maze.end[0] + dy, maze.end[1] + dx
            if 0 <= ny < maze.rows and 0 <= nx < maze.cols:
                maze.grid[ny][nx] = CellType.EMPTY.value
        
        maze.grid[maze.start[0]][maze.start[1]] = CellType.START.value
        maze.grid[maze.end[0]][maze.end[1]] = CellType.END.value
        maze._build_adjacency_list()
    
    @staticmethod
    def generate_cross_pattern(maze: Maze):
        """Generate a cross/plus pattern maze"""
        from src.maze import CellType
        
        # Reset to empty
        maze.grid = [[CellType.EMPTY.value for _ in range(maze.cols)] for _ in range(maze.rows)]
        
        # Add walls in cross pattern
        mid_row = maze.rows // 2
        mid_col = maze.cols // 2
        
        # Vertical line
        for row in range(0, maze.rows, 3):
            if row != mid_row:
                maze.grid[row][mid_col] = CellType.WALL.value
        
        # Horizontal line
        for col in range(0, maze.cols, 3):
            if col != mid_col:
                maze.grid[mid_row][col] = CellType.WALL.value
        
        # Add some random walls
        for _ in range(maze.rows * maze.cols // 10):
            row = random.randint(0, maze.rows - 1)
            col = random.randint(0, maze.cols - 1)
            if (row, col) != maze.start and (row, col) != maze.end:
                maze.grid[row][col] = CellType.WALL.value
        
        maze.grid[maze.start[0]][maze.start[1]] = CellType.START.value
        maze.grid[maze.end[0]][maze.end[1]] = CellType.END.value
        maze._build_adjacency_list()


def demo_parallel_execution():
    """Demonstrate parallel algorithm execution"""
    print("=" * 80)
    print(" " * 20 + "PARALLEL ALGORITHM EXECUTION DEMO")
    print("=" * 80)
    print()
    
    # Create maze
    maze = Maze(20, 30)
    maze.set_start(1, 1)
    maze.set_end(18, 28)
    maze.generate_random_maze(0.3)
    
    print("Running all algorithms in parallel...")
    print()
    
    # Run parallel
    runner = ParallelAlgorithmRunner(maze)
    results = runner.run_all_parallel()
    
    # Display results
    print("=" * 80)
    print("RESULTS")
    print("=" * 80)
    
    for name, metrics in sorted(results.items()):
        print(f"\n{name}:")
        print(f"  Path Found: {'✓' if metrics.path_found else '✗'}")
        print(f"  Nodes Explored: {metrics.nodes_explored}")
        print(f"  Path Length: {metrics.path_length}")
        print(f"  Time: {metrics.execution_time:.3f} ms")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    demo_parallel_execution()
