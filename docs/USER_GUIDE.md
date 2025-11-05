# User Guide

## Table of Contents

1. [Getting Started](#getting-started)
2. [GUI Mode](#gui-mode)
3. [Console Mode](#console-mode)
4. [Understanding the Output](#understanding-the-output)
5. [Advanced Usage](#advanced-usage)

---

## Getting Started

### Quick Start

```bash
# Run GUI mode
python main.py

# Run console analysis
python main.py --console

# Interactive mode
python main.py --interactive
```

---

## GUI Mode

### Interface Overview

The GUI is divided into three main sections:

1. **Header Bar** (Top)
   - Application title
   - Quick instructions

2. **Maze Grid** (Left)
   - Visual representation of the maze
   - Interactive editing area

3. **Control Panel** (Right)
   - Algorithm buttons
   - Utility buttons
   - Performance metrics display

### Color Legend

- **White**: Empty cell (walkable)
- **Dark Gray**: Wall (obstacle)
- **Green**: Start position
- **Red**: End position
- **Light Blue**: Visited cells
- **Sky Blue**: Currently exploring
- **Gold**: Solution path

### Controls

#### Mouse Controls

- **Left Click on Cell**: Toggle wall on/off
- **Left Click on Button**: Execute action

#### Keyboard Controls

- **ESC**: Exit application

### Editing the Maze

1. **Add/Remove Walls**
   - Click any empty cell to add a wall
   - Click a wall to remove it

2. **Reset Maze**
   - Click "Reset Maze" to clear all paths
   - Walls and structure remain intact

3. **Generate New Maze**
   - Click "Random Maze" for random wall placement
   - Start and end positions are preserved

### Running Algorithms

1. **Select an Algorithm**
   - Click any algorithm button to start

2. **Watch the Visualization**
   - See cells being explored in real-time
   - Light blue: Visited cells
   - Sky blue: Currently exploring
   - Gold: Final path

3. **View Metrics**
   - Metrics appear on the right panel
   - Shows performance data for the last run

### Algorithm Buttons

- **DFS**: Depth-First Search (fast, not optimal)
- **BFS**: Breadth-First Search (optimal, exhaustive)
- **Dijkstra**: Weighted shortest path (optimal)
- **A* (Manhattan)**: Heuristic search with Manhattan distance
- **A* (Euclidean)**: Heuristic search with Euclidean distance
- **Greedy Best-First**: Fastest, but not optimal
- **Bidirectional BFS**: Searches from both ends

### Utility Buttons

- **Reset Maze**: Clear visualization, keep structure
- **Random Maze**: Generate new random maze
- **Clear Path**: Remove all paths and visited markers

---

## Console Mode

### Running Console Mode

```bash
python main.py --console
```

### What Happens

1. **Maze Generation**: Creates a random 15x25 maze
2. **Algorithm Execution**: Runs all 7 algorithms sequentially
3. **Performance Metrics**: Displays detailed metrics for each
4. **Comparison Table**: Shows side-by-side comparison
5. **Chart Generation**: Creates visual comparison charts
6. **Data Export**: Saves results to JSON and CSV

### Output Files

All output is saved to the `results/` folder:

- `comparison_charts.png`: Bar charts comparing algorithms
- `radar_chart.png`: Multi-dimensional performance comparison
- `metrics.json`: Machine-readable metrics data
- `metrics.csv`: Spreadsheet-friendly format

### Sample Console Output

```
================================================================================
                        AI-BASED MAZE SOLVER
                 Console Mode - Algorithm Testing
================================================================================

Creating maze...
Generating random maze...

Initial Maze:
S . . . # . . . . .
. . # . . . # . . .
...

================================================================================
RUNNING ALL ALGORITHMS...
================================================================================

────────────────────────────────────────────────────────────────────────────────
Testing: DFS
────────────────────────────────────────────────────────────────────────────────

============================================================
Algorithm: DFS (Stack)
============================================================
Path Found: ✓
Optimal: ✗
Nodes Explored: 324
Path Length: 89
Execution Time: 9.874 ms
Memory Used: 19.53 KB
...
```

---

## Interactive Console Mode

### Running Interactive Mode

```bash
python main.py --interactive
```

### Workflow

1. **Set Maze Dimensions**
   ```
   Enter number of rows (10-50): 20
   Enter number of columns (10-50): 30
   ```

2. **Choose Maze Type**
   ```
   Maze Generation:
   1. Random walls
   2. DFS-generated perfect maze
   3. Empty maze (manual wall placement)
   Choose option (1-3): 1
   ```

3. **Select Algorithm**
   ```
   Select Algorithm:
   1. DFS
   2. BFS
   3. Dijkstra
   4. A* (Manhattan)
   5. A* (Euclidean)
   6. Greedy Best-First
   7. Bidirectional BFS
   8. Run All Algorithms
   Choose option (1-8): 4
   ```

4. **View Results**
   - Maze is displayed in console
   - Solution path is marked with `*`
   - Metrics are printed

---

## Understanding the Output

### Performance Metrics

#### Nodes Explored
- **What it means**: Number of cells examined by the algorithm
- **Lower is better**: More efficient search
- **Example**: BFS might explore 500 nodes, A* only 150

#### Path Length
- **What it means**: Number of steps in the solution
- **Lower is better**: Shorter path
- **Optimal algorithms**: Always find shortest path

#### Execution Time
- **What it means**: Time taken to find solution (milliseconds)
- **Lower is better**: Faster algorithm
- **Note**: May vary between runs

#### Memory Usage
- **What it means**: RAM consumed during execution (KB)
- **Lower is better**: More memory-efficient
- **Note**: Approximate measurement

#### Optimality
- **✓ Optimal**: Guaranteed to find shortest path
- **✗ Not Optimal**: May find longer path

### Comparison Charts

#### Bar Charts
- **Nodes Explored**: Compares search efficiency
- **Execution Time**: Speed comparison
- **Memory Usage**: Space complexity
- **Path Length**: Solution quality
- **Efficiency Score**: Overall performance (composite)

#### Pie Chart
- **Solution Quality**: Distribution of optimal vs. suboptimal solutions

#### Radar Chart
- **Multi-dimensional**: Compares algorithms across 4 metrics simultaneously
- **Larger area**: Better overall performance

---

## Advanced Usage

### Custom Maze Sizes

```bash
# Create a 30x40 maze
python main.py --size 30 40
```

### Parallel Execution

```python
from src.maze import Maze
from src.advanced_features import ParallelAlgorithmRunner

maze = Maze(20, 30)
maze.generate_random_maze(0.3)

runner = ParallelAlgorithmRunner(maze)
results = runner.run_all_parallel()

# All algorithms run simultaneously
for name, metrics in results.items():
    print(f"{name}: {metrics.execution_time:.2f} ms")
```

### Dynamic Obstacles

```python
from src.advanced_features import DynamicMazeSolver

solver = DynamicMazeSolver(maze)
solver.add_random_obstacles(count=10)
# Obstacles added while algorithm runs
```

### Export Data

```python
from src.dashboard import AnalyticsDashboard

dashboard = AnalyticsDashboard()
# ... add metrics ...

# Export to different formats
dashboard.export_to_json('results/data.json')
dashboard.export_to_csv('results/data.csv')
```

### Custom Heuristics

Modify `src/algorithms.py` to add your own heuristic:

```python
@staticmethod
def custom_heuristic(pos1, pos2):
    # Your custom distance calculation
    return your_distance_function(pos1, pos2)
```

Then use it:
```python
metrics = pathfinder.astar(heuristic='custom')
```

---

## Tips and Tricks

### For Best Visualization

1. **Adjust Speed**: Modify `visualization_speed` in `visualizer.py`
   ```python
   self.visualization_speed = 10  # Faster (10ms per step)
   self.visualization_speed = 100  # Slower (100ms per step)
   ```

2. **Larger Mazes**: Use smaller cell size
   ```bash
   python main.py --size 50 50
   ```

3. **Performance Testing**: Use console mode for accurate benchmarks
   ```bash
   python main.py --console
   ```

### For Algorithm Comparison

1. **Use Same Maze**: Save maze state before testing multiple algorithms
2. **Multiple Runs**: Run several times and average results
3. **Different Complexities**: Test on various maze sizes and densities

### For Learning

1. **Start Simple**: Begin with small mazes (10x10)
2. **Compare Two**: Run BFS vs A* to see heuristic impact
3. **Read Code**: Each algorithm is well-documented
4. **Modify**: Try changing heuristics or adding features

---

## Troubleshooting

### Maze Has No Solution

- **Symptom**: Algorithm shows "Path Found: ✗"
- **Cause**: Start and end are disconnected
- **Solution**: Click "Random Maze" to regenerate

### Visualization is Too Fast/Slow

- **Edit**: Modify `visualization_speed` in `src/visualizer.py`
- **Line**: Around line 37
- **Values**: 1-100ms recommended

### GUI Won't Start

- **Check**: Pygame installation
- **Try**: Console mode instead
- **Fix**: Reinstall pygame: `pip install pygame --upgrade`

### Charts Don't Display

- **Check**: Matplotlib backend
- **Fix**: Install tkinter (see Installation Guide)
- **Alternative**: View saved images in `results/` folder

---

## Keyboard Shortcuts Summary

| Key | Action |
|-----|--------|
| ESC | Exit application |
| Mouse Click | Toggle walls / Click buttons |

---

## FAQ

**Q: Can I create my own maze patterns?**  
A: Yes! Click cells in GUI mode to create custom patterns.

**Q: Which algorithm is fastest?**  
A: Greedy Best-First is usually fastest, but not optimal.

**Q: Which algorithm is best?**  
A: A* provides best balance of speed and optimality.

**Q: Can I use this for pathfinding in games?**  
A: Yes! The algorithms are production-ready for game development.

**Q: How do I save a maze?**  
A: Currently not implemented. Future feature!

---

## Next Steps

- Read [Algorithm Details](ALGORITHMS.md) for deep dive
- Check [API Documentation](API.md) for programming interface
- See [Examples](EXAMPLES.md) for code samples
- Contribute via [GitHub](https://github.com/Vikas8346/-Ai-based-maze-solver)
