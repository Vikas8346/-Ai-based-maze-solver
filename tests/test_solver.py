"""
Unit Tests for Maze Solver
"""
import unittest
from src.maze import Maze, CellType
from src.algorithms import PathfindingAlgorithms
from src.metrics import MetricsTracker


class TestMaze(unittest.TestCase):
    """Test maze functionality"""
    
    def setUp(self):
        """Set up test maze"""
        self.maze = Maze(10, 10)
    
    def test_maze_creation(self):
        """Test maze initialization"""
        self.assertEqual(self.maze.rows, 10)
        self.assertEqual(self.maze.cols, 10)
        self.assertEqual(self.maze.start, (0, 0))
        self.assertEqual(self.maze.end, (9, 9))
    
    def test_set_wall(self):
        """Test setting walls"""
        self.maze.set_wall(5, 5)
        self.assertEqual(self.maze.grid[5][5], CellType.WALL.value)
    
    def test_get_neighbors(self):
        """Test neighbor retrieval"""
        neighbors = self.maze.get_neighbors(5, 5)
        self.assertEqual(len(neighbors), 4)  # 4-directional
    
    def test_adjacency_list(self):
        """Test adjacency list building"""
        self.assertIn((0, 0), self.maze.adjacency_list)
        self.assertTrue(len(self.maze.adjacency_list) > 0)


class TestAlgorithms(unittest.TestCase):
    """Test pathfinding algorithms"""
    
    def setUp(self):
        """Set up test maze"""
        self.maze = Maze(5, 5)
        self.maze.set_start(0, 0)
        self.maze.set_end(4, 4)
        self.pathfinder = PathfindingAlgorithms(self.maze)
    
    def test_bfs_finds_path(self):
        """Test BFS finds path"""
        metrics = self.pathfinder.bfs()
        self.assertTrue(metrics.path_found)
        self.assertTrue(len(metrics.path) > 0)
    
    def test_dfs_finds_path(self):
        """Test DFS finds path"""
        metrics = self.pathfinder.dfs()
        self.assertTrue(metrics.path_found)
        self.assertTrue(len(metrics.path) > 0)
    
    def test_astar_finds_path(self):
        """Test A* finds path"""
        metrics = self.pathfinder.astar('manhattan')
        self.assertTrue(metrics.path_found)
        self.assertTrue(len(metrics.path) > 0)
    
    def test_dijkstra_finds_path(self):
        """Test Dijkstra finds path"""
        metrics = self.pathfinder.dijkstra()
        self.assertTrue(metrics.path_found)
        self.assertTrue(len(metrics.path) > 0)
    
    def test_bfs_optimal(self):
        """Test BFS finds optimal path"""
        metrics = self.pathfinder.bfs()
        self.assertTrue(metrics.is_optimal)
    
    def test_manhattan_heuristic(self):
        """Test Manhattan distance calculation"""
        dist = PathfindingAlgorithms.manhattan_distance((0, 0), (3, 4))
        self.assertEqual(dist, 7)
    
    def test_euclidean_heuristic(self):
        """Test Euclidean distance calculation"""
        dist = PathfindingAlgorithms.euclidean_distance((0, 0), (3, 4))
        self.assertEqual(dist, 5.0)


class TestMetrics(unittest.TestCase):
    """Test metrics tracking"""
    
    def test_metrics_tracker(self):
        """Test metrics tracker functionality"""
        tracker = MetricsTracker()
        tracker.start_tracking()
        tracker.increment_nodes()
        tracker.increment_nodes()
        tracker.update_frontier_size(5)
        
        metrics = tracker.create_metrics(
            algorithm_name="Test",
            path=[(0, 0), (1, 1)],
            time_complexity="O(n)",
            space_complexity="O(n)",
            is_optimal=True
        )
        
        self.assertEqual(metrics.algorithm_name, "Test")
        self.assertEqual(metrics.nodes_explored, 2)
        self.assertEqual(metrics.path_length, 2)
        self.assertTrue(metrics.is_optimal)


def run_tests():
    """Run all tests"""
    unittest.main()


if __name__ == '__main__':
    run_tests()
