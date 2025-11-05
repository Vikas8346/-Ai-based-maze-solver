"""
Dashboard Module
Comparative analysis with charts and tables
"""
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for headless environments
import matplotlib.pyplot as plt
import numpy as np
from typing import List
from src.metrics import AlgorithmMetrics, PerformanceComparator
import json


class AnalyticsDashboard:
    """
    Analytics dashboard for comparing algorithm performance
    """
    
    def __init__(self):
        """Initialize dashboard"""
        self.comparator = PerformanceComparator()
    
    def add_metrics(self, metrics: AlgorithmMetrics):
        """Add algorithm metrics"""
        self.comparator.add_metrics(metrics)
    
    def generate_comparison_charts(self, save_path: str = "results/comparison_charts.png"):
        """
        Generate comprehensive comparison charts
        
        Args:
            save_path: Path to save the chart image
        """
        if not self.comparator.all_metrics:
            print("No metrics to display")
            return
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle('Pathfinding Algorithms Comparison', fontsize=16, fontweight='bold')
        
        metrics = self.comparator.all_metrics
        algorithms = [m.algorithm_name for m in metrics]
        
        # 1. Nodes Explored
        ax1 = axes[0, 0]
        nodes = [m.nodes_explored for m in metrics]
        colors = plt.cm.viridis(np.linspace(0, 1, len(algorithms)))
        bars1 = ax1.bar(range(len(algorithms)), nodes, color=colors)
        ax1.set_xlabel('Algorithm')
        ax1.set_ylabel('Nodes Explored')
        ax1.set_title('Nodes Explored Comparison')
        ax1.set_xticks(range(len(algorithms)))
        ax1.set_xticklabels(algorithms, rotation=45, ha='right', fontsize=8)
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(height)}',
                    ha='center', va='bottom', fontsize=8)
        
        # 2. Execution Time
        ax2 = axes[0, 1]
        times = [m.execution_time for m in metrics]
        bars2 = ax2.bar(range(len(algorithms)), times, color=colors)
        ax2.set_xlabel('Algorithm')
        ax2.set_ylabel('Time (ms)')
        ax2.set_title('Execution Time Comparison')
        ax2.set_xticks(range(len(algorithms)))
        ax2.set_xticklabels(algorithms, rotation=45, ha='right', fontsize=8)
        ax2.grid(axis='y', alpha=0.3)
        
        for bar in bars2:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom', fontsize=8)
        
        # 3. Memory Usage
        ax3 = axes[0, 2]
        memory = [m.memory_used for m in metrics]
        bars3 = ax3.bar(range(len(algorithms)), memory, color=colors)
        ax3.set_xlabel('Algorithm')
        ax3.set_ylabel('Memory (KB)')
        ax3.set_title('Memory Usage Comparison')
        ax3.set_xticks(range(len(algorithms)))
        ax3.set_xticklabels(algorithms, rotation=45, ha='right', fontsize=8)
        ax3.grid(axis='y', alpha=0.3)
        
        for bar in bars3:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}',
                    ha='center', va='bottom', fontsize=8)
        
        # 4. Path Length
        ax4 = axes[1, 0]
        path_lengths = [m.path_length if m.path_found else 0 for m in metrics]
        bars4 = ax4.bar(range(len(algorithms)), path_lengths, color=colors)
        ax4.set_xlabel('Algorithm')
        ax4.set_ylabel('Path Length')
        ax4.set_title('Solution Path Length')
        ax4.set_xticks(range(len(algorithms)))
        ax4.set_xticklabels(algorithms, rotation=45, ha='right', fontsize=8)
        ax4.grid(axis='y', alpha=0.3)
        
        for bar in bars4:
            height = bar.get_height()
            if height > 0:
                ax4.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', fontsize=8)
        
        # 5. Efficiency Score (composite metric)
        ax5 = axes[1, 1]
        # Normalize metrics and calculate efficiency score
        max_nodes = max(nodes) if max(nodes) > 0 else 1
        max_time = max(times) if max(times) > 0 else 1
        
        efficiency_scores = []
        for m in metrics:
            if m.path_found:
                # Lower is better: combine normalized time and nodes
                score = (1 - m.nodes_explored / max_nodes) * 0.5 + (1 - m.execution_time / max_time) * 0.5
                efficiency_scores.append(score * 100)
            else:
                efficiency_scores.append(0)
        
        bars5 = ax5.bar(range(len(algorithms)), efficiency_scores, color=colors)
        ax5.set_xlabel('Algorithm')
        ax5.set_ylabel('Efficiency Score (%)')
        ax5.set_title('Overall Efficiency Score')
        ax5.set_xticks(range(len(algorithms)))
        ax5.set_xticklabels(algorithms, rotation=45, ha='right', fontsize=8)
        ax5.grid(axis='y', alpha=0.3)
        ax5.set_ylim(0, 100)
        
        for bar in bars5:
            height = bar.get_height()
            ax5.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}',
                    ha='center', va='bottom', fontsize=8)
        
        # 6. Optimality & Success Rate
        ax6 = axes[1, 2]
        optimal_count = sum(1 for m in metrics if m.is_optimal and m.path_found)
        suboptimal_count = sum(1 for m in metrics if not m.is_optimal and m.path_found)
        failed_count = sum(1 for m in metrics if not m.path_found)
        
        pie_data = [optimal_count, suboptimal_count, failed_count]
        pie_labels = [f'Optimal\n({optimal_count})', 
                     f'Suboptimal\n({suboptimal_count})', 
                     f'Failed\n({failed_count})']
        pie_colors = ['#2ecc71', '#f39c12', '#e74c3c']
        
        # Only show non-zero slices
        pie_data_filtered = [d for d in pie_data if d > 0]
        pie_labels_filtered = [l for i, l in enumerate(pie_labels) if pie_data[i] > 0]
        pie_colors_filtered = [c for i, c in enumerate(pie_colors) if pie_data[i] > 0]
        
        if pie_data_filtered:
            ax6.pie(pie_data_filtered, labels=pie_labels_filtered, colors=pie_colors_filtered,
                   autopct='%1.1f%%', startangle=90)
            ax6.set_title('Solution Quality Distribution')
        else:
            ax6.text(0.5, 0.5, 'No Data', ha='center', va='center')
            ax6.set_title('Solution Quality Distribution')
        
        plt.tight_layout()
        
        # Save figure
        import os
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Charts saved to: {save_path}")
        
        # Don't show in headless mode
        # plt.show()
    
    def generate_detailed_table(self):
        """Generate detailed comparison table"""
        print("\n" + "=" * 100)
        print("DETAILED ALGORITHM COMPARISON TABLE")
        print("=" * 100)
        print(self.comparator.get_comparison_table())
        
        # Additional analysis
        print("\n" + "=" * 100)
        print("BEST PERFORMING ALGORITHMS")
        print("=" * 100)
        
        best_time = self.comparator.get_best_algorithm('execution_time')
        if best_time:
            print(f"⚡ Fastest: {best_time.algorithm_name} ({best_time.execution_time:.3f} ms)")
        
        best_nodes = self.comparator.get_best_algorithm('nodes_explored')
        if best_nodes:
            print(f"🎯 Most Efficient: {best_nodes.algorithm_name} ({best_nodes.nodes_explored} nodes)")
        
        best_memory = self.comparator.get_best_algorithm('memory_used')
        if best_memory:
            print(f"💾 Least Memory: {best_memory.algorithm_name} ({best_memory.memory_used:.2f} KB)")
        
        optimal_algos = [m for m in self.comparator.all_metrics if m.is_optimal and m.path_found]
        if optimal_algos:
            print(f"✓ Optimal Solutions: {', '.join(m.algorithm_name for m in optimal_algos)}")
        
        print("=" * 100 + "\n")
    
    def export_to_json(self, filepath: str = "results/metrics.json"):
        """
        Export metrics to JSON file
        
        Args:
            filepath: Path to save JSON file
        """
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        data = {
            'metrics': [m.to_dict() for m in self.comparator.all_metrics],
            'summary': {
                'total_algorithms': len(self.comparator.all_metrics),
                'successful': sum(1 for m in self.comparator.all_metrics if m.path_found),
                'optimal': sum(1 for m in self.comparator.all_metrics if m.is_optimal and m.path_found)
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Metrics exported to: {filepath}")
    
    def export_to_csv(self, filepath: str = "results/metrics.csv"):
        """
        Export metrics to CSV file
        
        Args:
            filepath: Path to save CSV file
        """
        import os
        import csv
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        if not self.comparator.all_metrics:
            print("No metrics to export")
            return
        
        # Get fieldnames from first metric
        fieldnames = list(self.comparator.all_metrics[0].to_dict().keys())
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for m in self.comparator.all_metrics:
                writer.writerow(m.to_dict())
        
        print(f"Metrics exported to: {filepath}")
    
    def generate_radar_chart(self, save_path: str = "results/radar_chart.png"):
        """
        Generate radar chart comparing algorithms across multiple dimensions
        
        Args:
            save_path: Path to save the chart image
        """
        if not self.comparator.all_metrics:
            print("No metrics to display")
            return
        
        metrics = self.comparator.all_metrics
        
        # Only include algorithms that found a path
        valid_metrics = [m for m in metrics if m.path_found]
        
        if not valid_metrics:
            print("No valid solutions to compare")
            return
        
        # Normalize metrics (0-1 scale, higher is better)
        max_nodes = max(m.nodes_explored for m in valid_metrics)
        max_time = max(m.execution_time for m in valid_metrics)
        max_memory = max(m.memory_used for m in valid_metrics)
        max_path = max(m.path_length for m in valid_metrics)
        
        categories = ['Speed\n(Time)', 'Efficiency\n(Nodes)', 'Memory', 'Path Quality']
        num_vars = len(categories)
        
        # Compute angle for each axis
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        colors = plt.cm.tab10(np.linspace(0, 1, len(valid_metrics)))
        
        for idx, m in enumerate(valid_metrics):
            # Normalize values (invert so higher is better)
            values = [
                1 - (m.execution_time / max_time) if max_time > 0 else 0,
                1 - (m.nodes_explored / max_nodes) if max_nodes > 0 else 0,
                1 - (m.memory_used / max_memory) if max_memory > 0 else 0,
                1 - (m.path_length / max_path) if max_path > 0 and m.is_optimal else 0.5,
            ]
            values += values[:1]
            
            ax.plot(angles, values, 'o-', linewidth=2, label=m.algorithm_name, color=colors[idx])
            ax.fill(angles, values, alpha=0.15, color=colors[idx])
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, size=10)
        ax.set_ylim(0, 1)
        ax.set_yticks([0.25, 0.5, 0.75, 1.0])
        ax.set_yticklabels(['25%', '50%', '75%', '100%'])
        ax.grid(True)
        ax.set_title('Algorithm Performance Radar Chart', size=16, fontweight='bold', pad=20)
        
        plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        plt.tight_layout()
        
        import os
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Radar chart saved to: {save_path}")
        
        # Don't show in headless mode
        # plt.show()
    
    def clear(self):
        """Clear all metrics"""
        self.comparator.clear()
