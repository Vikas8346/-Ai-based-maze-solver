# Algorithm Deep Dive

## Overview

This document provides detailed explanations of all implemented pathfinding algorithms, including theoretical foundations, implementation details, and performance characteristics.

---

## Table of Contents

1. [Depth-First Search (DFS)](#depth-first-search-dfs)
2. [Breadth-First Search (BFS)](#breadth-first-search-bfs)
3. [Dijkstra's Algorithm](#dijkstras-algorithm)
4. [A* Search](#a-search)
5. [Greedy Best-First Search](#greedy-best-first-search)
6. [Bidirectional Search](#bidirectional-search)
7. [Heuristic Functions](#heuristic-functions)
8. [Performance Comparison](#performance-comparison)

---

## Depth-First Search (DFS)

### Overview

DFS is an **uninformed search algorithm** that explores as far as possible along each branch before backtracking.

### Implementation

- **Data Structure**: Stack (LIFO - Last In, First Out)
- **Approach**: Recursive-style exploration using explicit stack
- **Visited Tracking**: Set of explored nodes

### Algorithm Steps

```
1. Initialize stack with start node
2. Mark start as visited
3. While stack is not empty:
   a. Pop node from stack
   b. If node is goal, return path
   c. For each unvisited neighbor:
      - Mark as visited
      - Add to stack
      - Record parent for path reconstruction
4. Return failure if stack empties
```

### Pseudocode

```python
def dfs(start, goal):
    stack = [start]
    visited = {start}
    parent = {}
    
    while stack:
        current = stack.pop()
        
        if current == goal:
            return reconstruct_path(parent, goal)
        
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
                parent[neighbor] = current
    
    return None  # No path found
```

### Complexity Analysis

- **Time Complexity**: O(V + E)
  - V = number of vertices (cells)
  - E = number of edges (connections)
  - Visits each vertex once, explores each edge once

- **Space Complexity**: O(V)
  - Stack can contain up to V nodes
  - Visited set stores V nodes
  - Parent dictionary stores V entries

### Characteristics

✅ **Advantages**:
- Memory efficient (only stores current path)
- Good for deep mazes
- Simple implementation

❌ **Disadvantages**:
- **NOT optimal** - may find very long paths
- Can get stuck in deep branches
- Unpredictable path quality

### When to Use

- Memory is limited
- Any solution is acceptable
- Maze is very deep
- Exploring all possibilities

---

## Breadth-First Search (BFS)

### Overview

BFS is an **uninformed search algorithm** that explores level by level, guaranteeing the shortest path in unweighted graphs.

### Implementation

- **Data Structure**: Queue (FIFO - First In, First Out)
- **Approach**: Level-order exploration
- **Visited Tracking**: Set of explored nodes

### Algorithm Steps

```
1. Initialize queue with start node
2. Mark start as visited
3. While queue is not empty:
   a. Dequeue node from front
   b. If node is goal, return path
   c. For each unvisited neighbor:
      - Mark as visited
      - Add to queue
      - Record parent
4. Return failure if queue empties
```

### Pseudocode

```python
def bfs(start, goal):
    queue = deque([start])
    visited = {start}
    parent = {}
    
    while queue:
        current = queue.popleft()
        
        if current == goal:
            return reconstruct_path(parent, goal)
        
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                parent[neighbor] = current
    
    return None
```

### Complexity Analysis

- **Time Complexity**: O(V + E)
  - Same as DFS
  - Visits each vertex once

- **Space Complexity**: O(V)
  - Queue can contain entire level
  - Worst case: O(b^d) where b=branching factor, d=depth

### Characteristics

✅ **Advantages**:
- **Optimal** - guarantees shortest path
- Complete - finds solution if it exists
- Systematic exploration

❌ **Disadvantages**:
- High memory usage for wide mazes
- No heuristic guidance
- Explores unnecessary areas

### When to Use

- Optimal solution required
- Uniform cost environment
- Maze is wide and shallow
- Guaranteed completeness needed

---

## Dijkstra's Algorithm

### Overview

Dijkstra's algorithm is a **weighted graph** shortest path algorithm, generalizing BFS to handle different edge costs.

### Implementation

- **Data Structure**: Priority Queue (Min-Heap)
- **Approach**: Always expand lowest-cost node
- **Cost Tracking**: Distance from start to each node

### Algorithm Steps

```
1. Initialize priority queue with (0, start)
2. Set distance[start] = 0, all others = ∞
3. While priority queue not empty:
   a. Pop node with minimum distance
   b. If already visited, skip
   c. If node is goal, return path
   d. For each neighbor:
      - Calculate new distance
      - If better than known, update
      - Add to priority queue
```

### Pseudocode

```python
def dijkstra(start, goal):
    pq = [(0, start)]  # (cost, node)
    visited = set()
    cost = {start: 0}
    parent = {}
    
    while pq:
        current_cost, current = heappop(pq)
        
        if current in visited:
            continue
        
        visited.add(current)
        
        if current == goal:
            return reconstruct_path(parent, goal)
        
        for neighbor in get_neighbors(current):
            new_cost = current_cost + edge_weight(current, neighbor)
            
            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                heappush(pq, (new_cost, neighbor))
                parent[neighbor] = current
    
    return None
```

### Complexity Analysis

- **Time Complexity**: O((V + E) log V)
  - Each vertex added/removed from heap: O(V log V)
  - Each edge relaxed: O(E log V)

- **Space Complexity**: O(V)
  - Priority queue: O(V)
  - Cost and parent dictionaries: O(V)

### Characteristics

✅ **Advantages**:
- **Optimal** for weighted graphs
- Handles varying edge costs
- Systematic and complete

❌ **Disadvantages**:
- No heuristic guidance
- Explores uniformly in all directions
- Slower than A* for goal-directed search

### When to Use

- Different terrain costs
- Need optimal weighted path
- No good heuristic available
- Graph is not too large

---

## A* Search

### Overview

A* is an **informed search algorithm** that combines actual cost (like Dijkstra) with heuristic estimate (goal direction).

### Key Concept

**f(n) = g(n) + h(n)**

- **g(n)**: Actual cost from start to node n
- **h(n)**: Heuristic estimate from n to goal
- **f(n)**: Total estimated cost of path through n

### Implementation

- **Data Structure**: Priority Queue ordered by f-score
- **Heuristic**: Distance estimate to goal
- **Admissibility**: h(n) must never overestimate

### Algorithm Steps

```
1. Initialize priority queue with (h(start), 0, start)
2. Set g_score[start] = 0
3. While priority queue not empty:
   a. Pop node with minimum f-score
   b. If already visited, skip
   c. If node is goal, return path
   d. For each neighbor:
      - Calculate g_score (actual cost)
      - Calculate h_score (heuristic)
      - Calculate f_score = g + h
      - If better than known, update
      - Add to priority queue
```

### Pseudocode

```python
def astar(start, goal, heuristic):
    pq = [(heuristic(start, goal), 0, start)]  # (f, g, node)
    visited = set()
    g_score = {start: 0}
    parent = {}
    
    while pq:
        f, g, current = heappop(pq)
        
        if current in visited:
            continue
        
        visited.add(current)
        
        if current == goal:
            return reconstruct_path(parent, goal)
        
        for neighbor in get_neighbors(current):
            new_g = g + edge_weight(current, neighbor)
            
            if neighbor not in g_score or new_g < g_score[neighbor]:
                g_score[neighbor] = new_g
                h = heuristic(neighbor, goal)
                f_score = new_g + h
                heappush(pq, (f_score, new_g, neighbor))
                parent[neighbor] = current
    
    return None
```

### Complexity Analysis

- **Time Complexity**: O(b^d) average case
  - b = branching factor
  - d = solution depth
  - With good heuristic: much better than Dijkstra

- **Space Complexity**: O(b^d)
  - Must store all generated nodes

### Heuristic Properties

**Admissible**: Never overestimates actual cost
- Guarantees optimal solution
- h(n) ≤ actual_cost(n, goal)

**Consistent** (Monotonic): h(n) ≤ cost(n, n') + h(n')
- Stronger than admissible
- Ensures nodes expanded in cost order

### Characteristics

✅ **Advantages**:
- **Optimal** with admissible heuristic
- Much faster than Dijkstra for goal-directed search
- Balances cost and heuristic
- Industry standard for pathfinding

❌ **Disadvantages**:
- Requires good heuristic
- More memory than Greedy
- Implementation complexity

### When to Use

- Need optimal solution
- Have good heuristic
- Goal-directed search
- Standard for games and robotics

---

## Greedy Best-First Search

### Overview

Greedy Best-First Search uses **only the heuristic** (ignores actual cost), always moving toward the goal.

### Key Concept

**f(n) = h(n)** (no g component)

Selects node that appears closest to goal.

### Implementation

- **Data Structure**: Priority Queue ordered by h-score only
- **Approach**: Purely heuristic-driven
- **Trade-off**: Speed over optimality

### Pseudocode

```python
def greedy_best_first(start, goal, heuristic):
    pq = [(heuristic(start, goal), start)]  # (h, node)
    visited = set()
    parent = {}
    
    while pq:
        h, current = heappop(pq)
        
        if current in visited:
            continue
        
        visited.add(current)
        
        if current == goal:
            return reconstruct_path(parent, goal)
        
        for neighbor in get_neighbors(current):
            if neighbor not in visited:
                h_score = heuristic(neighbor, goal)
                heappush(pq, (h_score, neighbor))
                if neighbor not in parent:
                    parent[neighbor] = current
    
    return None
```

### Complexity Analysis

- **Time Complexity**: O(b^m)
  - m = maximum depth
  - Can be much faster than A* in practice

- **Space Complexity**: O(b^m)

### Characteristics

✅ **Advantages**:
- **Fastest** in many cases
- Low memory if heuristic is good
- Simple implementation
- Good for approximate solutions

❌ **Disadvantages**:
- **NOT optimal** - can find suboptimal paths
- Can be misled by heuristic
- Not complete (can get stuck)
- May explore unnecessary nodes

### When to Use

- Speed more important than optimality
- Good heuristic available
- Approximate solution acceptable
- Real-time constraints

---

## Bidirectional Search

### Overview

Bidirectional Search runs **two simultaneous searches**: one from start, one from goal, meeting in the middle.

### Key Concept

**Reduces search space**: O(b^(d/2)) instead of O(b^d)

### Implementation

- **Data Structures**: Two queues (forward and backward)
- **Meeting Condition**: When searches intersect
- **Path Reconstruction**: Combine both paths

### Algorithm Steps

```
1. Initialize forward queue with start
2. Initialize backward queue with goal
3. While both queues not empty:
   a. Expand forward search one level
   b. Check if meets backward search
   c. Expand backward search one level
   d. Check if meets forward search
   e. If meeting found, reconstruct path
```

### Pseudocode

```python
def bidirectional_search(start, goal):
    forward_queue = deque([start])
    backward_queue = deque([goal])
    
    forward_visited = {start: None}
    backward_visited = {goal: None}
    
    while forward_queue and backward_queue:
        # Forward search
        current = forward_queue.popleft()
        if current in backward_visited:
            return merge_paths(forward_visited, backward_visited, current)
        
        for neighbor in get_neighbors(current):
            if neighbor not in forward_visited:
                forward_visited[neighbor] = current
                forward_queue.append(neighbor)
        
        # Backward search
        current = backward_queue.popleft()
        if current in forward_visited:
            return merge_paths(forward_visited, backward_visited, current)
        
        for neighbor in get_neighbors(current):
            if neighbor not in backward_visited:
                backward_visited[neighbor] = current
                backward_queue.append(neighbor)
    
    return None
```

### Complexity Analysis

- **Time Complexity**: O(b^(d/2))
  - Significantly better than O(b^d)
  - Example: b=10, d=6: 10^3 + 10^3 = 2,000 vs 10^6 = 1,000,000

- **Space Complexity**: O(b^(d/2))

### Characteristics

✅ **Advantages**:
- **Much faster** for large search spaces
- Optimal (with BFS)
- Dramatic speedup for deep searches

❌ **Disadvantages**:
- More complex implementation
- Requires goal to be known
- Path reconstruction more complex
- Two search frontiers in memory

### When to Use

- Large or deep search space
- Both start and goal known
- Optimal solution required
- Can afford complexity

---

## Heuristic Functions

### Manhattan Distance

**Formula**: `h(n) = |x₁ - x₂| + |y₁ - y₂|`

**Properties**:
- Admissible for 4-directional movement
- Exact for grid with no obstacles
- Most common for grid-based pathfinding

**When to Use**:
- Grid-based movement
- 4-directional (up, down, left, right)
- Standard maze solving

### Euclidean Distance

**Formula**: `h(n) = √((x₁ - x₂)² + (y₁ - y₂)²)`

**Properties**:
- Straight-line distance
- Admissible for any movement
- Lower estimates than Manhattan

**When to Use**:
- Any-angle movement
- Continuous spaces
- More relaxed estimates

### Chebyshev Distance

**Formula**: `h(n) = max(|x₁ - x₂|, |y₁ - y₂|)`

**Properties**:
- Admissible for 8-directional movement
- Accounts for diagonal moves
- Higher estimates than Euclidean

**When to Use**:
- 8-directional movement
- Diagonal moves allowed
- Chess-like movement

### Heuristic Quality

**Good Heuristic**:
- Admissible (never overestimates)
- Close to actual cost
- Fast to compute
- Guides search effectively

**Bad Heuristic**:
- Inadmissible (loses optimality)
- Poor estimate (too low or high)
- Expensive to compute
- Misleads search

---

## Performance Comparison

### Efficiency Ranking (Typical)

**For Optimal Paths**:
1. A* (Manhattan) - Best balance
2. A* (Euclidean) - Close second
3. Bidirectional BFS - Good for deep searches
4. Dijkstra - No heuristic penalty
5. BFS - Uniform expansion

**For Speed (Any Path)**:
1. Greedy Best-First - Fastest
2. A* - Fast and optimal
3. Bidirectional - Good middle ground
4. BFS - Systematic but slow
5. DFS - Unpredictable
6. Dijkstra - Slowest for goal search

### Memory Usage Ranking

1. DFS - Lowest (current path only)
2. Greedy - Low with good heuristic
3. A* - Moderate
4. BFS - High for wide mazes
5. Dijkstra - High uniform exploration
6. Bidirectional - Highest (two frontiers)

### Use Case Matrix

| Scenario | Best Algorithm | Why |
|----------|---------------|-----|
| Need optimal, have heuristic | A* | Best of both worlds |
| Need optimal, no heuristic | BFS/Dijkstra | Guaranteed optimal |
| Need fast, approximate OK | Greedy | Fastest |
| Very deep search | Bidirectional | Exponential speedup |
| Memory constrained | DFS | Lowest memory |
| Weighted graph | Dijkstra/A* | Handle costs |
| Real-time game | A* or Greedy | Fast and effective |

---

## Implementation Details

### Path Reconstruction

All algorithms use a parent dictionary to reconstruct the path:

```python
def reconstruct_path(parent, goal):
    path = [goal]
    current = goal
    
    while current in parent:
        current = parent[current]
        path.append(current)
    
    path.reverse()
    return path
```

### Tie-Breaking

When multiple nodes have the same priority:

```python
# Add secondary key for consistent ordering
heappush(pq, (f_score, node_id, node))
```

### Early Exit Optimization

Stop as soon as goal is dequeued (not when added):

```python
if current == goal:
    return path  # Optimal due to priority queue
```

---

## Further Reading

- **Introduction to Algorithms** (CLRS)
- **Artificial Intelligence: A Modern Approach** (Russell & Norvig)
- **Amit's A* Pages** (theory.stanford.edu/~amitp)
- **Red Blob Games** (www.redblobgames.com)

---

## Summary Table

| Algorithm | Type | Optimal | Complete | Time | Space | Best For |
|-----------|------|---------|----------|------|-------|----------|
| DFS | Uninformed | ❌ | ❌ | O(V+E) | O(V) | Deep search, low memory |
| BFS | Uninformed | ✅ | ✅ | O(V+E) | O(V) | Unweighted shortest path |
| Dijkstra | Weighted | ✅ | ✅ | O((V+E)logV) | O(V) | Weighted shortest path |
| A* | Informed | ✅* | ✅ | O(b^d) | O(b^d) | Goal-directed optimal |
| Greedy | Informed | ❌ | ❌ | O(b^m) | O(b^m) | Fast approximate |
| Bidirectional | Uninformed | ✅ | ✅ | O(b^(d/2)) | O(b^(d/2)) | Large search spaces |

*With admissible heuristic
