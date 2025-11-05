"""
Main Application Entry Point
Runs the GUI-based maze solver
"""
import sys
import argparse
from src.maze import Maze
from src.visualizer import MazeVisualizer
from src.console_solver import run_console_solver, interactive_console_mode


def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(
        description='AI-Based Maze Solver - Pathfinding Algorithm Comparison',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Run GUI mode
  python main.py --console          # Run console solver with all algorithms
  python main.py --interactive      # Run interactive console mode
  python main.py --size 20 30       # Run GUI with custom maze size
        """
    )
    
    parser.add_argument('--console', action='store_true',
                       help='Run in console mode (no GUI)')
    parser.add_argument('--interactive', action='store_true',
                       help='Run interactive console mode')
    parser.add_argument('--size', nargs=2, type=int, metavar=('ROWS', 'COLS'),
                       help='Maze dimensions (default: 20x30)')
    
    args = parser.parse_args()
    
    if args.console:
        # Console mode
        print("\nStarting console mode...\n")
        run_console_solver()
    elif args.interactive:
        # Interactive console mode
        print("\nStarting interactive mode...\n")
        interactive_console_mode()
    else:
        # GUI mode
        print("\nStarting GUI mode...")
        print("Please wait while the visualization window loads...\n")
        
        # Get maze size
        rows, cols = args.size if args.size else (20, 30)
        
        # Create maze
        maze = Maze(rows, cols)
        maze.set_start(1, 1)
        maze.set_end(rows - 2, cols - 2)
        
        # Generate initial random maze
        maze.generate_random_maze(wall_probability=0.25)
        
        print(f"Maze created: {rows}x{cols}")
        print("Controls:")
        print("  - Click cells to toggle walls")
        print("  - Click algorithm buttons to solve")
        print("  - Use 'Reset Maze' to clear paths")
        print("  - Use 'Random Maze' to generate new maze")
        print("  - Press ESC to exit\n")
        
        # Create and run visualizer
        try:
            visualizer = MazeVisualizer(maze, cell_size=min(30, 800 // max(rows, cols)))
            visualizer.run()
        except Exception as e:
            print(f"\nError running visualizer: {e}")
            print("Falling back to console mode...\n")
            run_console_solver()


if __name__ == "__main__":
    main()
