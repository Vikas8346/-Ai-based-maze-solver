"""
Maze Representation Module
Graph-based maze with 2D grid + adjacency mapping
"""
import random
from typing import List, Tuple, Set, Dict
from enum import Enum


class CellType(Enum):
    """Cell types in the maze"""
    EMPTY = 0
    WALL = 1
    START = 2
    END = 3
    PATH = 4
    VISITED = 5
    EXPLORING = 6


class Maze:
    """
    Graph-based maze representation using 2D grid and adjacency list
    """
    
    def __init__(self, rows: int, cols: int):
        """
        Initialize maze with given dimensions
        
        Args:
            rows: Number of rows in the maze
            cols: Number of columns in the maze
        """
        self.rows = rows
        self.cols = cols
        self.grid: List[List[int]] = [[CellType.EMPTY.value for _ in range(cols)] for _ in range(rows)]
        self.start: Tuple[int, int] = (0, 0)
        self.end: Tuple[int, int] = (rows - 1, cols - 1)
        self.adjacency_list: Dict[Tuple[int, int], List[Tuple[int, int]]] = {}
        self._build_adjacency_list()
    
    def _build_adjacency_list(self):
        """Build adjacency list representation of the maze graph"""
        self.adjacency_list.clear()
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] != CellType.WALL.value:
                    neighbors = self.get_neighbors(row, col)
                    self.adjacency_list[(row, col)] = neighbors
    
    def get_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """
        Get valid neighbors for a cell (4-directional movement)
        
        Args:
            row: Row index
            col: Column index
            
        Returns:
            List of valid neighbor coordinates
        """
        neighbors = []
        # 4-directional movement: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < self.rows and 
                0 <= new_col < self.cols and 
                self.grid[new_row][new_col] != CellType.WALL.value):
                neighbors.append((new_row, new_col))
        
        return neighbors
    
    def set_wall(self, row: int, col: int):
        """Set a cell as wall"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = CellType.WALL.value
            self._build_adjacency_list()
    
    def set_start(self, row: int, col: int):
        """Set start position"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.start = (row, col)
            self.grid[row][col] = CellType.START.value
    
    def set_end(self, row: int, col: int):
        """Set end position"""
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.end = (row, col)
            self.grid[row][col] = CellType.END.value
    
    def is_valid_cell(self, row: int, col: int) -> bool:
        """Check if a cell is valid and not a wall"""
        return (0 <= row < self.rows and 
                0 <= col < self.cols and 
                self.grid[row][col] != CellType.WALL.value)
    
    def reset_path_visualization(self):
        """Reset visualization cells (keep walls, start, end)"""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] in [CellType.PATH.value, CellType.VISITED.value, CellType.EXPLORING.value]:
                    self.grid[row][col] = CellType.EMPTY.value
        
        # Restore start and end
        self.grid[self.start[0]][self.start[1]] = CellType.START.value
        self.grid[self.end[0]][self.end[1]] = CellType.END.value
    
    def generate_random_maze(self, wall_probability: float = 0.3):
        """
        Generate a random maze using random wall placement
        
        Args:
            wall_probability: Probability of a cell being a wall (0.0 to 1.0)
        """
        # Reset grid
        self.grid = [[CellType.EMPTY.value for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Add random walls
        for row in range(self.rows):
            for col in range(self.cols):
                if random.random() < wall_probability:
                    self.grid[row][col] = CellType.WALL.value
        
        # Ensure start and end are not walls
        self.grid[self.start[0]][self.start[1]] = CellType.START.value
        self.grid[self.end[0]][self.end[1]] = CellType.END.value
        
        # Rebuild adjacency list
        self._build_adjacency_list()
    
    def generate_maze_dfs(self):
        """
        Generate a perfect maze using recursive DFS (maze generation algorithm)
        Creates a maze with exactly one path between any two points
        """
        # Initialize all cells as walls
        self.grid = [[CellType.WALL.value for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Start from (1, 1)
        start_row, start_col = 1, 1
        
        def carve_path(row: int, col: int):
            """Recursively carve paths in the maze"""
            self.grid[row][col] = CellType.EMPTY.value
            
            # Get all possible directions
            directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
            random.shuffle(directions)
            
            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                
                if (0 <= new_row < self.rows and 
                    0 <= new_col < self.cols and 
                    self.grid[new_row][new_col] == CellType.WALL.value):
                    
                    # Carve the wall between
                    wall_row, wall_col = row + dr // 2, col + dc // 2
                    self.grid[wall_row][wall_col] = CellType.EMPTY.value
                    
                    # Recursively carve from new position
                    carve_path(new_row, new_col)
        
        if self.rows > 2 and self.cols > 2:
            carve_path(start_row, start_col)
        
        # Set start and end
        self.grid[self.start[0]][self.start[1]] = CellType.START.value
        self.grid[self.end[0]][self.end[1]] = CellType.END.value
        
        # Rebuild adjacency list
        self._build_adjacency_list()
    
    def get_edge_weight(self, from_cell: Tuple[int, int], to_cell: Tuple[int, int]) -> float:
        """
        Get edge weight between two cells (default is 1.0 for uniform cost)
        Can be modified for weighted graphs
        """
        return 1.0
    
    def __str__(self) -> str:
        """String representation of the maze"""
        symbols = {
            CellType.EMPTY.value: '.',
            CellType.WALL.value: '#',
            CellType.START.value: 'S',
            CellType.END.value: 'E',
            CellType.PATH.value: '*',
            CellType.VISITED.value: 'v',
            CellType.EXPLORING.value: 'o'
        }
        
        result = []
        for row in self.grid:
            result.append(' '.join(symbols.get(cell, '?') for cell in row))
        return '\n'.join(result)
