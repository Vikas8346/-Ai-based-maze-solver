# 🚀 Quick Start Guide

Get started with the AI-Based Maze Solver in 5 minutes!

## Installation (Choose One)

### Option 1: Automated Setup (Recommended)

**Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```bash
setup.bat
```

### Option 2: Manual Setup

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

## Running the Application

### GUI Mode (Interactive)
```bash
python main.py
```
- Click cells to toggle walls
- Click algorithm buttons to solve
- Watch real-time visualization

### Console Mode (Full Analysis)
```bash
python main.py --console
```
- Runs all algorithms automatically
- Generates comparison charts
- Exports metrics to JSON/CSV

### Quick Demo
```bash
python demo.py
```
- Simple demonstration
- Compares BFS vs A*
- Generates sample chart

### Interactive Console
```bash
python main.py --interactive
```
- Custom maze size
- Choose generation method
- Select specific algorithm

## Your First Maze

### GUI Mode Steps:

1. **Start the application**
   ```bash
   python main.py
   ```

2. **Edit the maze** (optional)
   - Click cells to add/remove walls
   - Or click "Random Maze" for a new one

3. **Run an algorithm**
   - Click "A* (Manhattan)" for best results
   - Watch the visualization!

4. **View metrics**
   - See performance data on the right panel

### Console Mode Output:

```bash
python main.py --console
```

You'll get:
- ✅ Detailed metrics for each algorithm
- ✅ Comparison table
- ✅ Performance charts (saved to `results/`)
- ✅ Exported data (JSON & CSV)

## Understanding the Output

### GUI Colors:
- 🟩 **Green**: Start position
- 🔴 **Red**: End position
- ⬛ **Dark Gray**: Walls
- 🔵 **Light Blue**: Visited cells
- 💙 **Sky Blue**: Currently exploring
- 🟨 **Gold**: Solution path

### Console Metrics:
```
Algorithm: A* (Manhattan)
============================================================
Path Found: ✓           # Solution exists
Optimal: ✓              # Shortest path guaranteed
Nodes Explored: 157     # Efficiency
Path Length: 35         # Solution quality
Execution Time: 1.79 ms # Speed
Memory Used: 32.13 KB   # Space complexity
```

## Common Commands

```bash
# GUI with custom size
python main.py --size 30 40

# Console analysis
python main.py --console

# Interactive mode
python main.py --interactive

# Quick demo
python demo.py

# Run tests
python -m unittest tests.test_solver
```

## File Outputs

All results saved to `results/` folder:

- **comparison_charts.png**: Performance bar charts
- **radar_chart.png**: Multi-dimensional comparison
- **metrics.json**: Machine-readable data
- **metrics.csv**: Spreadsheet format

## Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: GUI won't start
**Solution:** Use console mode instead:
```bash
python main.py --console
```

### Issue: "No module named pygame"
**Solution:**
```bash
pip install pygame
```

### Issue: Charts not displaying
**Solution:** Charts are automatically saved to `results/` folder, even if display fails.

## Next Steps

1. ✅ **Try different algorithms**: Compare their performance
2. ✅ **Experiment with maze sizes**: See how algorithms scale
3. ✅ **Create custom mazes**: Click cells to design patterns
4. ✅ **Read the docs**: Check `docs/` for detailed explanations
5. ✅ **Modify code**: Customize algorithms or add features

## Learning Resources

- **User Guide**: `docs/USER_GUIDE.md`
- **Algorithm Details**: `docs/ALGORITHMS.md`
- **API Docs**: Comments in source code
- **Examples**: `demo.py` and `src/console_solver.py`

## Key Algorithms

| Algorithm | Best For |
|-----------|----------|
| **BFS** | Guaranteed shortest path |
| **A*** | Best balance (speed + optimal) |
| **Dijkstra** | Weighted graphs |
| **Greedy** | Fastest (approximate) |
| **DFS** | Low memory |
| **Bidirectional** | Very large mazes |

## Tips

💡 **For best visualization**: Use 20x30 maze or smaller  
💡 **For performance testing**: Use console mode  
💡 **For learning**: Start with BFS, then try A*  
💡 **For speed**: Use Greedy Best-First  
💡 **For accuracy**: Use A* or Dijkstra  

## Example Session

```bash
# 1. Start with demo
python demo.py

# 2. Try GUI mode
python main.py

# 3. Run full analysis
python main.py --console

# 4. View results
ls results/
```

## Getting Help

- **README**: Project overview
- **USER_GUIDE**: Detailed usage instructions
- **ALGORITHMS**: Algorithm explanations
- **GitHub Issues**: Report bugs or ask questions

---

**Ready to explore? Start with:**
```bash
python main.py
```

Enjoy solving mazes with AI! 🎉
