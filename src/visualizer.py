"""
Pygame Visualization Module
Real-time visualization of pathfinding algorithms
"""
import pygame
import sys
from typing import Optional, List, Tuple
from src.maze import Maze, CellType
from src.algorithms import PathfindingAlgorithms
from src.metrics import AlgorithmMetrics


# Color palette
COLORS = {
    'empty': (255, 255, 255),      # White
    'wall': (40, 40, 40),          # Dark gray
    'start': (0, 255, 0),          # Green
    'end': (255, 0, 0),            # Red
    'path': (255, 215, 0),         # Gold
    'visited': (173, 216, 230),    # Light blue
    'exploring': (135, 206, 250),  # Sky blue
    'grid': (200, 200, 200),       # Light gray
    'bg': (245, 245, 245),         # Off-white
    'text': (0, 0, 0),             # Black
    'button': (70, 130, 180),      # Steel blue
    'button_hover': (100, 149, 237), # Cornflower blue
}


class MazeVisualizer:
    """
    Interactive maze visualization using Pygame
    """
    
    def __init__(self, maze: Maze, cell_size: int = 30):
        """
        Initialize visualizer
        
        Args:
            maze: Maze object to visualize
            cell_size: Size of each cell in pixels
        """
        pygame.init()
        
        self.maze = maze
        self.cell_size = cell_size
        self.grid_width = maze.cols * cell_size
        self.grid_height = maze.rows * cell_size
        
        # UI dimensions
        self.sidebar_width = 350
        self.header_height = 80
        
        self.width = self.grid_width + self.sidebar_width
        self.height = self.grid_height + self.header_height
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("AI Maze Solver - Pathfinding Visualization")
        
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Fonts
        self.title_font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 24)
        self.metrics_font = pygame.font.Font(None, 20)
        
        # State
        self.running = True
        self.algorithm_running = False
        self.current_metrics: Optional[AlgorithmMetrics] = None
        self.visualization_speed = 50  # milliseconds per step
        self.step_delay = 0
        
        # Buttons
        self.buttons = self._create_buttons()
        
        # Edit mode
        self.edit_mode = 'wall'  # 'wall', 'start', 'end'
        self.mouse_pressed = False
    
    def _create_buttons(self) -> List[dict]:
        """Create UI buttons"""
        button_x = self.grid_width + 20
        button_y = self.header_height + 20
        button_width = 310
        button_height = 40
        spacing = 10
        
        buttons = [
            {'name': 'DFS', 'rect': pygame.Rect(button_x, button_y, button_width, button_height), 'action': 'dfs'},
            {'name': 'BFS', 'rect': pygame.Rect(button_x, button_y + (button_height + spacing) * 1, button_width, button_height), 'action': 'bfs'},
            {'name': 'Dijkstra', 'rect': pygame.Rect(button_x, button_y + (button_height + spacing) * 2, button_width, button_height), 'action': 'dijkstra'},
            {'name': 'A* (Manhattan)', 'rect': pygame.Rect(button_x, button_y + (button_height + spacing) * 3, button_width, button_height), 'action': 'astar_manhattan'},
            {'name': 'A* (Euclidean)', 'rect': pygame.Rect(button_x, button_y + (button_height + spacing) * 4, button_width, button_height), 'action': 'astar_euclidean'},
            {'name': 'Greedy Best-First', 'rect': pygame.Rect(button_x, button_y + (button_height + spacing) * 5, button_width, button_height), 'action': 'greedy'},
            {'name': 'Bidirectional BFS', 'rect': pygame.Rect(button_x, button_y + (button_height + spacing) * 6, button_width, button_height), 'action': 'bidirectional'},
            {'name': 'Reset Maze', 'rect': pygame.Rect(button_x, button_y + (button_height + spacing) * 8, button_width, button_height), 'action': 'reset'},
            {'name': 'Random Maze', 'rect': pygame.Rect(button_x, button_y + (button_height + spacing) * 9, button_width, button_height), 'action': 'random'},
            {'name': 'Clear Path', 'rect': pygame.Rect(button_x, button_y + (button_height + spacing) * 10, button_width, button_height), 'action': 'clear'},
        ]
        
        return buttons
    
    def _draw_grid(self):
        """Draw the maze grid"""
        for row in range(self.maze.rows):
            for col in range(self.maze.cols):
                x = col * self.cell_size
                y = row * self.cell_size + self.header_height
                
                cell_value = self.maze.grid[row][col]
                
                # Determine color
                if (row, col) == self.maze.start:
                    color = COLORS['start']
                elif (row, col) == self.maze.end:
                    color = COLORS['end']
                elif cell_value == CellType.WALL.value:
                    color = COLORS['wall']
                elif cell_value == CellType.PATH.value:
                    color = COLORS['path']
                elif cell_value == CellType.VISITED.value:
                    color = COLORS['visited']
                elif cell_value == CellType.EXPLORING.value:
                    color = COLORS['exploring']
                else:
                    color = COLORS['empty']
                
                # Draw cell
                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))
                pygame.draw.rect(self.screen, COLORS['grid'], (x, y, self.cell_size, self.cell_size), 1)
    
    def _draw_header(self):
        """Draw header with title"""
        header_rect = pygame.Rect(0, 0, self.width, self.header_height)
        pygame.draw.rect(self.screen, COLORS['button'], header_rect)
        
        title = self.title_font.render("AI Maze Solver", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.width // 2, self.header_height // 2 - 10))
        self.screen.blit(title, title_rect)
        
        subtitle = self.metrics_font.render("Click cells to edit | Select algorithm to solve", True, (255, 255, 255))
        subtitle_rect = subtitle.get_rect(center=(self.width // 2, self.header_height // 2 + 20))
        self.screen.blit(subtitle, subtitle_rect)
    
    def _draw_buttons(self):
        """Draw UI buttons"""
        mouse_pos = pygame.mouse.get_pos()
        
        for button in self.buttons:
            # Check hover
            is_hover = button['rect'].collidepoint(mouse_pos)
            color = COLORS['button_hover'] if is_hover else COLORS['button']
            
            # Draw button
            pygame.draw.rect(self.screen, color, button['rect'], border_radius=5)
            pygame.draw.rect(self.screen, COLORS['text'], button['rect'], 2, border_radius=5)
            
            # Draw text
            text = self.button_font.render(button['name'], True, COLORS['text'])
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)
    
    def _draw_metrics(self):
        """Draw performance metrics"""
        if not self.current_metrics:
            return
        
        metrics_x = self.grid_width + 20
        metrics_y = self.header_height + 520
        
        m = self.current_metrics
        
        metrics_text = [
            f"Algorithm: {m.algorithm_name}",
            f"Path Found: {'✓' if m.path_found else '✗'}",
            f"Optimal: {'✓' if m.is_optimal else '✗'}",
            f"Nodes Explored: {m.nodes_explored}",
            f"Path Length: {m.path_length}",
            f"Time: {m.execution_time:.2f} ms",
            f"Memory: {m.memory_used:.2f} KB",
            f"Complexity: {m.time_complexity}",
        ]
        
        for i, text in enumerate(metrics_text):
            surface = self.metrics_font.render(text, True, COLORS['text'])
            self.screen.blit(surface, (metrics_x, metrics_y + i * 25))
    
    def _visualization_callback(self, row: int, col: int, state: str):
        """Callback for algorithm visualization"""
        if state == 'exploring':
            self.maze.grid[row][col] = CellType.EXPLORING.value
        elif state == 'visited':
            if self.maze.grid[row][col] == CellType.EMPTY.value:
                self.maze.grid[row][col] = CellType.VISITED.value
        elif state == 'path':
            self.maze.grid[row][col] = CellType.PATH.value
        
        # Update display
        self._draw()
        pygame.display.flip()
        
        # Small delay for visualization
        pygame.time.delay(self.visualization_speed)
        
        # Process events to keep UI responsive
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    
    def _run_algorithm(self, algorithm_name: str):
        """Run selected algorithm"""
        if self.algorithm_running:
            return
        
        self.algorithm_running = True
        self.maze.reset_path_visualization()
        
        # Create pathfinding instance
        pathfinder = PathfindingAlgorithms(self.maze)
        pathfinder.set_visualization_callback(self._visualization_callback)
        
        # Run algorithm
        if algorithm_name == 'dfs':
            metrics = pathfinder.dfs()
        elif algorithm_name == 'bfs':
            metrics = pathfinder.bfs()
        elif algorithm_name == 'dijkstra':
            metrics = pathfinder.dijkstra()
        elif algorithm_name == 'astar_manhattan':
            metrics = pathfinder.astar('manhattan')
        elif algorithm_name == 'astar_euclidean':
            metrics = pathfinder.astar('euclidean')
        elif algorithm_name == 'greedy':
            metrics = pathfinder.greedy_best_first('manhattan')
        elif algorithm_name == 'bidirectional':
            metrics = pathfinder.bidirectional_search()
        else:
            metrics = None
        
        self.current_metrics = metrics
        self.algorithm_running = False
        
        # Print metrics to console
        if metrics:
            print(metrics)
    
    def _handle_mouse_click(self, pos: Tuple[int, int]):
        """Handle mouse click events"""
        x, y = pos
        
        # Check button clicks
        for button in self.buttons:
            if button['rect'].collidepoint(pos):
                action = button['action']
                
                if action == 'reset':
                    self.maze.reset_path_visualization()
                    self.current_metrics = None
                elif action == 'random':
                    self.maze.generate_random_maze(wall_probability=0.3)
                    self.current_metrics = None
                elif action == 'clear':
                    self.maze.reset_path_visualization()
                    self.current_metrics = None
                else:
                    self._run_algorithm(action)
                return
        
        # Check grid clicks
        if y >= self.header_height and x < self.grid_width:
            col = x // self.cell_size
            row = (y - self.header_height) // self.cell_size
            
            if 0 <= row < self.maze.rows and 0 <= col < self.maze.cols:
                if (row, col) == self.maze.start or (row, col) == self.maze.end:
                    return
                
                # Toggle wall
                if self.maze.grid[row][col] == CellType.WALL.value:
                    self.maze.grid[row][col] = CellType.EMPTY.value
                else:
                    self.maze.grid[row][col] = CellType.WALL.value
                
                self.maze._build_adjacency_list()
    
    def _draw(self):
        """Draw everything"""
        self.screen.fill(COLORS['bg'])
        self._draw_header()
        self._draw_grid()
        self._draw_buttons()
        self._draw_metrics()
    
    def run(self):
        """Main visualization loop"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.algorithm_running:
                    self._handle_mouse_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            
            self._draw()
            pygame.display.flip()
            self.clock.tick(self.fps)
        
        pygame.quit()


def main():
    """Test visualization"""
    # Create a test maze
    maze = Maze(20, 30)
    maze.set_start(1, 1)
    maze.set_end(18, 28)
    maze.generate_random_maze(0.25)
    
    # Run visualizer
    visualizer = MazeVisualizer(maze, cell_size=25)
    visualizer.run()


if __name__ == "__main__":
    main()
