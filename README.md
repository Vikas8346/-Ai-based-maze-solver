# 🧠 AI-Based Maze Solver

An advanced **AI-powered Maze Solving System** that compares classical pathfinding algorithms with heuristic-based artificial intelligence techniques. Features real-time visualization, comprehensive performance analysis, and interactive GUI.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Complete-success.svg)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Algorithms Implemented](#algorithms-implemented)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technical Details](#technical-details)
- [Performance Metrics](#performance-metrics)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This project implements and compares **7 different pathfinding algorithms** with real-time visualization, performance metrics, and comprehensive analysis. It demonstrates the application of Data Structures and Algorithms (DSA) principles in AI-based problem solving.

### Key Objectives

✅ Compare classical vs. AI-based pathfinding algorithms  
✅ Visualize algorithm exploration patterns in real-time  
✅ Analyze performance using DAA principles  
✅ Evaluate effectiveness of different heuristics  
✅ Generate comparative analytics and charts  

---

## ✨ Features

### Core Features

- **7 Pathfinding Algorithms**: DFS, BFS, Dijkstra, A*, Greedy Best-First, Bidirectional BFS
- **Real-time Visualization**: Watch algorithms explore the maze step-by-step
- **Interactive GUI**: Click to edit maze, run algorithms, and see results instantly
- **Performance Metrics**: Track time, space, nodes explored, path optimality
- **Comparative Analysis**: Side-by-side comparison with charts and tables
- **Multiple Maze Types**: Random, DFS-generated perfect mazes, custom patterns

### Advanced Features

- **Dynamic Obstacles**: Add obstacles during pathfinding
- **Parallel Execution**: Run all algorithms simultaneously
- **Multiple Heuristics**: Manhattan, Euclidean, Chebyshev distances
- **Export Results**: JSON and CSV export of metrics
- **Console Mode**: Run without GUI for batch testing
- **Interactive Mode**: Custom maze creation and testing

---

## 🤖 Algorithms Implemented

| Algorithm | Type | Optimal | Time Complexity | Space Complexity |
|-----------|------|---------|-----------------|------------------|
| **DFS** | Uninformed | ❌ | O(V + E) | O(V) |
| **BFS** | Uninformed | ✅ | O(V + E) | O(V) |
| **Dijkstra** | Weighted | ✅ | O((V + E) log V) | O(V) |
| **A*** | Informed | ✅ | O(b^d) | O(V) |
| **Greedy Best-First** | Informed | ❌ | O(b^m) | O(V) |
| **Bidirectional BFS** | Uninformed | ✅ | O(b^(d/2)) | O(b^(d/2)) |

### Data Structures Used

- **2D Arrays/Grids**: Maze representation
- **Stacks**: DFS implementation
- **Queues (Deque)**: BFS implementation
- **Priority Queues (Min-Heap)**: Dijkstra, A*, Greedy Best-First
- **Hash Maps/Sets**: Visited nodes tracking
- **Adjacency Lists**: Graph representation

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository

```bash
git clone https://github.com/Vikas8346/-Ai-based-maze-solver.git
cd -Ai-based-maze-solver
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

**Required Packages:**
- `pygame` - GUI visualization
- `matplotlib` - Charts and graphs
- `numpy` - Numerical computations

---

## 💻 Usage

### GUI Mode (Default)

Run the interactive visualization:

```bash
python main.py
```

**Controls:**
- Click cells to toggle walls
- Click algorithm buttons to solve
- Use "Reset Maze" to clear paths
- Use "Random Maze" to generate new maze
- Press ESC to exit

### Console Mode

Run all algorithms and generate reports:

```bash
python main.py --console
```

This will:
- Run all 7 algorithms on a random maze
- Display performance metrics
- Generate comparison charts
- Export results to `results/` folder

### Interactive Console Mode

Custom maze creation and testing:

```bash
python main.py --interactive
```

### Custom Maze Size

```bash
python main.py --size 30 40
```

### Run Individual Modules

```bash
# Run visualizer directly
python src/visualizer.py

# Run console solver
python src/console_solver.py

# Demo parallel execution
python src/advanced_features.py

# Run tests
python -m pytest tests/
```

---

## 📁 Project Structure

```
-Ai-based-maze-solver/
│
├── src/
│   ├── __init__.py              # Package initialization
│   ├── maze.py                  # Maze representation (2D grid + adjacency list)
│   ├── algorithms.py            # All pathfinding algorithms
│   ├── metrics.py               # Performance tracking and metrics
│   ├── visualizer.py            # Pygame GUI visualization
│   ├── dashboard.py             # Analytics and comparison charts
│   ├── console_solver.py        # Console-based solver
│   └── advanced_features.py     # Dynamic obstacles, parallel execution
│
├── tests/
│   └── test_solver.py           # Unit tests
│
├── results/                     # Generated output (auto-created)
│   ├── comparison_charts.png    # Performance comparison charts
│   ├── radar_chart.png          # Algorithm radar chart
│   ├── metrics.json             # Exported metrics (JSON)
│   └── metrics.csv              # Exported metrics (CSV)
│
├── main.py                      # Main entry point
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## 🔧 Technical Details

### Graph Representation

The maze uses a **hybrid representation**:
1. **2D Grid**: Direct cell access for visualization
2. **Adjacency List**: Efficient neighbor lookup for pathfinding

```python
# Example maze structure
maze.grid[row][col]              # Direct access
maze.adjacency_list[(row, col)]  # Neighbor list
```

### Heuristic Functions

**Manhattan Distance** (4-directional movement):
```
h(n) = |x₁ - x₂| + |y₁ - y₂|
```

**Euclidean Distance** (straight-line):
```
h(n) = √((x₁ - x₂)² + (y₁ - y₂)²)
```

**Chebyshev Distance** (8-directional):
```
h(n) = max(|x₁ - x₂|, |y₁ - y₂|)
```

### Performance Tracking

Metrics tracked for each algorithm:
- **Execution Time**: Using `time.perf_counter()`
- **Memory Usage**: Using `tracemalloc`
- **Nodes Explored**: Custom counter
- **Path Length**: Number of steps in solution
- **Frontier Size**: Maximum queue/stack size
- **Optimality**: Theoretical guarantee

---

## 📊 Performance Metrics

### Sample Results (20x30 Maze)

| Algorithm | Nodes | Path | Time (ms) | Memory (KB) | Optimal |
|-----------|-------|------|-----------|-------------|---------|
| BFS | 487 | 47 | 12.45 | 23.4 | ✓ |
| A* (Manhattan) | 142 | 47 | 8.32 | 18.7 | ✓ |
| Dijkstra | 489 | 47 | 15.67 | 24.1 | ✓ |
| Greedy | 78 | 51 | 5.21 | 12.3 | ✗ |
| DFS | 324 | 89 | 9.87 | 19.5 | ✗ |
| Bidirectional | 256 | 47 | 10.12 | 21.8 | ✓ |

### Key Insights

- **A*** is fastest for optimal paths (best balance)
- **Greedy** is fastest overall but not optimal
- **BFS/Dijkstra** explore most nodes (exhaustive)
- **DFS** can find very suboptimal paths
- **Bidirectional** reduces search space significantly

---

## 📸 Screenshots

### GUI Visualization
*Interactive maze solver with real-time algorithm visualization*

### Performance Charts
*Comparative analysis across all algorithms*

### Console Output
*Detailed metrics and performance tables*

---

## 🧪 Testing

Run unit tests:

```bash
python -m pytest tests/ -v
```

Test coverage includes:
- Maze creation and manipulation
- Algorithm correctness
- Path validation
- Metrics accuracy

---

## 📚 Educational Value

This project demonstrates:

1. **Algorithm Analysis**: Compare theoretical vs. actual performance
2. **Data Structures**: Practical application of queues, stacks, heaps
3. **Heuristics**: Impact of different heuristic functions
4. **Graph Theory**: Graph representation and traversal
5. **AI Techniques**: Informed vs. uninformed search
6. **Software Engineering**: Modular design, testing, documentation

---

## 🛣️ Roadmap / Future Enhancements

- [ ] **Weighted graphs**: Different terrain costs
- [ ] **Jump Point Search**: Optimized A* for grid maps
- [ ] **Theta***: Any-angle pathfinding
- [ ] **3D mazes**: Extend to 3D visualization
- [ ] **Web interface**: Browser-based visualization
- [ ] **Algorithm animation speed control**
- [ ] **Save/load mazes**
- [ ] **More maze generation algorithms**

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/NewFeature`)
3. Commit changes (`git commit -m 'Add NewFeature'`)
4. Push to branch (`git push origin feature/NewFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Vikas**
- GitHub: [@Vikas8346](https://github.com/Vikas8346)

---

## 🙏 Acknowledgments

- Pathfinding algorithms based on classical computer science literature
- Pygame community for visualization framework
- Matplotlib for data visualization
- Python scientific computing community

---

## 📖 References

1. **Dijkstra, E. W.** (1959). "A note on two problems in connexion with graphs"
2. **Hart, P. E., et al.** (1968). "A Formal Basis for the Heuristic Determination of Minimum Cost Paths"
3. **Russell, S., Norvig, P.** (2020). "Artificial Intelligence: A Modern Approach"
4. **Cormen, T. H., et al.** (2009). "Introduction to Algorithms"

---

<div align="center">

**⭐ Star this repository if you find it helpful! ⭐**

Made with ❤️ for learning and education

</div>