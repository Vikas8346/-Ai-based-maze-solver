"""
Performance Metrics Module
Tracks and analyzes algorithm performance
"""
import time
import tracemalloc
from typing import List, Tuple, Optional
from dataclasses import dataclass, field


@dataclass
class AlgorithmMetrics:
    """
    Data structure to store algorithm performance metrics
    """
    algorithm_name: str
    nodes_explored: int = 0
    path_length: int = 0
    execution_time: float = 0.0  # in milliseconds
    memory_used: float = 0.0  # in KB
    is_optimal: bool = False
    path_found: bool = False
    path: List[Tuple[int, int]] = field(default_factory=list)
    
    # Time complexity (theoretical)
    time_complexity: str = ""
    # Space complexity (theoretical)
    space_complexity: str = ""
    
    # Additional metrics
    max_frontier_size: int = 0
    heuristic_used: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert metrics to dictionary for easy export"""
        return {
            'algorithm': self.algorithm_name,
            'nodes_explored': self.nodes_explored,
            'path_length': self.path_length,
            'execution_time_ms': round(self.execution_time, 3),
            'memory_kb': round(self.memory_used, 2),
            'is_optimal': self.is_optimal,
            'path_found': self.path_found,
            'time_complexity': self.time_complexity,
            'space_complexity': self.space_complexity,
            'max_frontier_size': self.max_frontier_size,
            'heuristic': self.heuristic_used if self.heuristic_used else 'N/A'
        }
    
    def __str__(self) -> str:
        """String representation of metrics"""
        return (
            f"\n{'=' * 60}\n"
            f"Algorithm: {self.algorithm_name}\n"
            f"{'=' * 60}\n"
            f"Path Found: {'✓' if self.path_found else '✗'}\n"
            f"Optimal: {'✓' if self.is_optimal else '✗'}\n"
            f"Nodes Explored: {self.nodes_explored}\n"
            f"Path Length: {self.path_length}\n"
            f"Execution Time: {self.execution_time:.3f} ms\n"
            f"Memory Used: {self.memory_used:.2f} KB\n"
            f"Max Frontier Size: {self.max_frontier_size}\n"
            f"Time Complexity: {self.time_complexity}\n"
            f"Space Complexity: {self.space_complexity}\n"
            f"Heuristic: {self.heuristic_used if self.heuristic_used else 'N/A'}\n"
            f"{'=' * 60}\n"
        )


class MetricsTracker:
    """
    Tracks performance metrics for pathfinding algorithms
    """
    
    def __init__(self):
        self.start_time: float = 0.0
        self.nodes_explored: int = 0
        self.max_frontier_size: int = 0
        self.memory_snapshot = None
    
    def start_tracking(self):
        """Start tracking metrics"""
        self.start_time = time.perf_counter()
        self.nodes_explored = 0
        self.max_frontier_size = 0
        tracemalloc.start()
        self.memory_snapshot = tracemalloc.take_snapshot()
    
    def increment_nodes(self):
        """Increment nodes explored counter"""
        self.nodes_explored += 1
    
    def update_frontier_size(self, size: int):
        """Update maximum frontier size"""
        if size > self.max_frontier_size:
            self.max_frontier_size = size
    
    def stop_tracking(self) -> Tuple[float, float]:
        """
        Stop tracking and return metrics
        
        Returns:
            Tuple of (execution_time_ms, memory_kb)
        """
        execution_time = (time.perf_counter() - self.start_time) * 1000  # Convert to ms
        
        # Get memory usage
        current_snapshot = tracemalloc.take_snapshot()
        tracemalloc.stop()
        
        # Calculate memory difference
        stats = current_snapshot.compare_to(self.memory_snapshot, 'lineno')
        memory_used = sum(stat.size_diff for stat in stats) / 1024  # Convert to KB
        
        return execution_time, max(memory_used, 0.01)  # Ensure at least some memory is reported
    
    def create_metrics(self, 
                      algorithm_name: str,
                      path: List[Tuple[int, int]],
                      time_complexity: str,
                      space_complexity: str,
                      is_optimal: bool = False,
                      heuristic: Optional[str] = None) -> AlgorithmMetrics:
        """
        Create metrics object from tracked data
        
        Args:
            algorithm_name: Name of the algorithm
            path: Solution path found
            time_complexity: Theoretical time complexity
            space_complexity: Theoretical space complexity
            is_optimal: Whether the algorithm guarantees optimal path
            heuristic: Heuristic function used (if any)
            
        Returns:
            AlgorithmMetrics object
        """
        execution_time, memory_used = self.stop_tracking()
        
        return AlgorithmMetrics(
            algorithm_name=algorithm_name,
            nodes_explored=self.nodes_explored,
            path_length=len(path) if path else 0,
            execution_time=execution_time,
            memory_used=memory_used,
            is_optimal=is_optimal,
            path_found=len(path) > 0,
            path=path,
            time_complexity=time_complexity,
            space_complexity=space_complexity,
            max_frontier_size=self.max_frontier_size,
            heuristic_used=heuristic
        )


class PerformanceComparator:
    """
    Compares performance metrics across multiple algorithms
    """
    
    def __init__(self):
        self.all_metrics: List[AlgorithmMetrics] = []
    
    def add_metrics(self, metrics: AlgorithmMetrics):
        """Add metrics for comparison"""
        self.all_metrics.append(metrics)
    
    def get_comparison_table(self) -> str:
        """Generate comparison table"""
        if not self.all_metrics:
            return "No metrics to compare"
        
        header = f"{'Algorithm':<25} {'Nodes':<10} {'Path':<8} {'Time(ms)':<12} {'Memory(KB)':<12} {'Optimal':<8}"
        separator = "=" * 85
        
        rows = [separator, header, separator]
        
        for m in self.all_metrics:
            row = (
                f"{m.algorithm_name:<25} "
                f"{m.nodes_explored:<10} "
                f"{m.path_length:<8} "
                f"{m.execution_time:<12.3f} "
                f"{m.memory_used:<12.2f} "
                f"{'✓' if m.is_optimal else '✗':<8}"
            )
            rows.append(row)
        
        rows.append(separator)
        return "\n".join(rows)
    
    def get_best_algorithm(self, metric: str = 'execution_time') -> Optional[AlgorithmMetrics]:
        """
        Get the best performing algorithm based on a specific metric
        
        Args:
            metric: Metric to compare ('execution_time', 'nodes_explored', 'memory_used')
            
        Returns:
            Best performing AlgorithmMetrics or None
        """
        if not self.all_metrics:
            return None
        
        # Only consider algorithms that found a path
        valid_metrics = [m for m in self.all_metrics if m.path_found]
        
        if not valid_metrics:
            return None
        
        if metric == 'execution_time':
            return min(valid_metrics, key=lambda m: m.execution_time)
        elif metric == 'nodes_explored':
            return min(valid_metrics, key=lambda m: m.nodes_explored)
        elif metric == 'memory_used':
            return min(valid_metrics, key=lambda m: m.memory_used)
        else:
            return valid_metrics[0]
    
    def clear(self):
        """Clear all stored metrics"""
        self.all_metrics.clear()
