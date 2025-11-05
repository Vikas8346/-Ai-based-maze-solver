"""
Quick Demo Script
Demonstrates basic usage of the maze solver
"""

from src.maze import Maze
from src.algorithms import PathfindingAlgorithms
from src.dashboard import AnalyticsDashboard


def quick_demo():
    """Quick demonstration of the maze solver"""
    print("=" * 80)
    print(" " * 25 + "MAZE SOLVER QUICK DEMO")
    print("=" * 80)
    print()
    
    # Create a small maze
    print("Step 1: Creating a 10x15 maze...")
    maze = Maze(10, 15)
    maze.set_start(1, 1)
    maze.set_end(8, 13)
    
    # Add some walls manually for demonstration
    walls = [
        (2, 3), (2, 4), (2, 5), (2, 6),
        (5, 2), (5, 3), (5, 4), (5, 5),
        (7, 8), (7, 9), (7, 10)
    ]
    for row, col in walls:
        maze.set_wall(row, col)
    
    print("\nMaze created:")
    print(maze)
    print()
    
    # Test BFS
    print("Step 2: Running BFS (Breadth-First Search)...")
    pathfinder = PathfindingAlgorithms(maze)
    bfs_metrics = pathfinder.bfs()
    
    print(f"\n✓ BFS Results:")
    print(f"  - Path found: {bfs_metrics.path_found}")
    print(f"  - Nodes explored: {bfs_metrics.nodes_explored}")
    print(f"  - Path length: {bfs_metrics.path_length}")
    print(f"  - Time: {bfs_metrics.execution_time:.3f} ms")
    print(f"  - Optimal: {bfs_metrics.is_optimal}")
    
    # Test A*
    print("\nStep 3: Running A* with Manhattan heuristic...")
    maze.reset_path_visualization()
    astar_metrics = pathfinder.astar('manhattan')
    
    print(f"\n✓ A* Results:")
    print(f"  - Path found: {astar_metrics.path_found}")
    print(f"  - Nodes explored: {astar_metrics.nodes_explored}")
    print(f"  - Path length: {astar_metrics.path_length}")
    print(f"  - Time: {astar_metrics.execution_time:.3f} ms")
    print(f"  - Optimal: {astar_metrics.is_optimal}")
    
    # Compare
    print("\nStep 4: Comparison...")
    print(f"\n  A* explored {bfs_metrics.nodes_explored - astar_metrics.nodes_explored} fewer nodes!")
    print(f"  A* was {(bfs_metrics.execution_time - astar_metrics.execution_time):.3f} ms faster!")
    print(f"  Both found optimal paths of length {bfs_metrics.path_length}")
    
    # Create dashboard
    print("\nStep 5: Generating comparison chart...")
    dashboard = AnalyticsDashboard()
    dashboard.add_metrics(bfs_metrics)
    dashboard.add_metrics(astar_metrics)
    
    try:
        dashboard.generate_comparison_charts('results/demo_comparison.png')
        print("✓ Chart saved to: results/demo_comparison.png")
    except Exception as e:
        print(f"✗ Could not generate chart: {e}")
    
    print("\n" + "=" * 80)
    print("Demo complete! Try running:")
    print("  - python main.py              (GUI mode)")
    print("  - python main.py --console    (Full analysis)")
    print("=" * 80)
    print()


if __name__ == "__main__":
    quick_demo()
