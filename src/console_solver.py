"""
Console-based Maze Solver
For testing and basic visualization without GUI
"""
from src.maze import Maze
from src.algorithms import PathfindingAlgorithms
from src.metrics import PerformanceComparator
from src.dashboard import AnalyticsDashboard
import time


def print_maze_with_path(maze: Maze):
    """Print maze in console"""
    print(maze)
    print()


def run_console_solver():
    """Run console-based maze solver with all algorithms"""
    print("=" * 80)
    print(" " * 25 + "AI-BASED MAZE SOLVER")
    print(" " * 20 + "Console Mode - Algorithm Testing")
    print("=" * 80)
    print()
    
    # Create maze
    print("Creating maze...")
    maze = Maze(15, 25)
    maze.set_start(1, 1)
    maze.set_end(13, 23)
    
    # Generate random maze
    print("Generating random maze...")
    maze.generate_random_maze(wall_probability=0.25)
    
    print("\nInitial Maze:")
    print_maze_with_path(maze)
    
    # Initialize dashboard
    dashboard = AnalyticsDashboard()
    
    # Test all algorithms
    algorithms_to_test = [
        ('DFS', lambda p: p.dfs()),
        ('BFS', lambda p: p.bfs()),
        ('Dijkstra', lambda p: p.dijkstra()),
        ('A* (Manhattan)', lambda p: p.astar('manhattan')),
        ('A* (Euclidean)', lambda p: p.astar('euclidean')),
        ('Greedy Best-First', lambda p: p.greedy_best_first('manhattan')),
        ('Bidirectional BFS', lambda p: p.bidirectional_search()),
    ]
    
    print("\n" + "=" * 80)
    print("RUNNING ALL ALGORITHMS...")
    print("=" * 80)
    
    for algo_name, algo_func in algorithms_to_test:
        print(f"\n{'─' * 80}")
        print(f"Testing: {algo_name}")
        print(f"{'─' * 80}")
        
        # Reset maze visualization
        maze.reset_path_visualization()
        
        # Create pathfinder
        pathfinder = PathfindingAlgorithms(maze)
        
        # Run algorithm
        metrics = algo_func(pathfinder)
        
        # Add to dashboard
        dashboard.add_metrics(metrics)
        
        # Print results
        print(metrics)
        
        # Show maze with path (optional, can be commented out for cleaner output)
        if metrics.path_found and len(metrics.path) > 0:
            # Mark path on maze
            for row, col in metrics.path:
                if (row, col) != maze.start and (row, col) != maze.end:
                    from src.maze import CellType
                    maze.grid[row][col] = CellType.PATH.value
            
            # print("Solution Path:")
            # print_maze_with_path(maze)
        
        time.sleep(0.1)  # Small delay between algorithms
    
    # Generate comparison reports
    print("\n" + "=" * 80)
    print("GENERATING ANALYTICS...")
    print("=" * 80)
    
    dashboard.generate_detailed_table()
    
    # Export results
    try:
        dashboard.export_to_json()
        dashboard.export_to_csv()
        print("\n✓ Results exported successfully!")
    except Exception as e:
        print(f"\n✗ Error exporting results: {e}")
    
    # Generate charts
    print("\n" + "=" * 80)
    print("GENERATING VISUALIZATION CHARTS...")
    print("=" * 80)
    
    try:
        dashboard.generate_comparison_charts()
        dashboard.generate_radar_chart()
        print("\n✓ Charts generated successfully!")
    except Exception as e:
        print(f"\n✗ Error generating charts: {e}")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE!")
    print("=" * 80)
    print("\nCheck the 'results' folder for exported data and charts.")
    print()


def interactive_console_mode():
    """Interactive console mode for custom testing"""
    print("=" * 80)
    print(" " * 25 + "INTERACTIVE MAZE SOLVER")
    print("=" * 80)
    print()
    
    # Get maze dimensions
    while True:
        try:
            rows = int(input("Enter number of rows (10-50): "))
            cols = int(input("Enter number of columns (10-50): "))
            if 10 <= rows <= 50 and 10 <= cols <= 50:
                break
            else:
                print("Please enter values between 10 and 50")
        except ValueError:
            print("Please enter valid integers")
    
    # Create maze
    maze = Maze(rows, cols)
    maze.set_start(1, 1)
    maze.set_end(rows - 2, cols - 2)
    
    # Maze generation choice
    print("\nMaze Generation:")
    print("1. Random walls")
    print("2. DFS-generated perfect maze")
    print("3. Empty maze (manual wall placement)")
    
    choice = input("Choose option (1-3): ").strip()
    
    if choice == '1':
        wall_prob = float(input("Enter wall probability (0.0-0.5): ") or "0.3")
        maze.generate_random_maze(wall_probability=wall_prob)
    elif choice == '2':
        maze.generate_maze_dfs()
    
    print("\nMaze generated:")
    print_maze_with_path(maze)
    
    # Algorithm selection
    print("\nSelect Algorithm:")
    print("1. DFS")
    print("2. BFS")
    print("3. Dijkstra")
    print("4. A* (Manhattan)")
    print("5. A* (Euclidean)")
    print("6. Greedy Best-First")
    print("7. Bidirectional BFS")
    print("8. Run All Algorithms")
    
    algo_choice = input("Choose option (1-8): ").strip()
    
    pathfinder = PathfindingAlgorithms(maze)
    dashboard = AnalyticsDashboard()
    
    if algo_choice == '8':
        # Run all
        algorithms = [
            pathfinder.dfs(),
            pathfinder.bfs(),
            pathfinder.dijkstra(),
            pathfinder.astar('manhattan'),
            pathfinder.astar('euclidean'),
            pathfinder.greedy_best_first('manhattan'),
            pathfinder.bidirectional_search(),
        ]
        
        for metrics in algorithms:
            dashboard.add_metrics(metrics)
            maze.reset_path_visualization()
        
        dashboard.generate_detailed_table()
        
        try:
            dashboard.generate_comparison_charts()
        except:
            pass
    else:
        # Run single algorithm
        algo_map = {
            '1': pathfinder.dfs,
            '2': pathfinder.bfs,
            '3': pathfinder.dijkstra,
            '4': lambda: pathfinder.astar('manhattan'),
            '5': lambda: pathfinder.astar('euclidean'),
            '6': lambda: pathfinder.greedy_best_first('manhattan'),
            '7': pathfinder.bidirectional_search,
        }
        
        if algo_choice in algo_map:
            metrics = algo_map[algo_choice]()
            print(metrics)
            
            if metrics.path_found:
                print("\nSolution found! Marking path...")
                from src.maze import CellType
                for row, col in metrics.path:
                    if (row, col) != maze.start and (row, col) != maze.end:
                        maze.grid[row][col] = CellType.PATH.value
                
                print_maze_with_path(maze)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
        interactive_console_mode()
    else:
        run_console_solver()
