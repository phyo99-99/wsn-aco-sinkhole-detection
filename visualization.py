#!/usr/bin/env python3
"""
Visualization module for WSN security results
Creates network graphs and performance charts

This file handles visualization of ACO sinkhole detection results:
- Network topology plotting with attack detection overlay
- Performance metrics bar charts (detection rate, false alarm rate, etc.)
- Research paper comparison charts
- High-resolution PNG output for presentations
- Color-coded node classification (normal, malicious, detected, false alarm)

Created by Phyo Theingi, 1 October 2025
"""

import matplotlib.pyplot as plt
import numpy as np

class WSNVisualizer:
    """Creates visualizations for WSN security analysis."""
    
    def __init__(self, network, detected_attacks, metrics):
        self.network = network
        self.detected_attacks = detected_attacks
        self.metrics = metrics
    
    def visualize_network(self):
        """Create network visualization with attack detection results."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Network visualization
        ax1.set_title('Wireless Sensor Network with ACO Detection', fontsize=14)
        
        # Plot all nodes
        for node_id, node in self.network.nodes.items():
            if node.is_malicious:
                ax1.scatter(node.x, node.y, c='red', s=100, marker='X', 
                           label='Sinkhole Attack' if node_id == self.network.sinkhole_nodes[0] else "")
            else:
                ax1.scatter(node.x, node.y, c='blue', s=50, alpha=0.6)
        
        # Highlight detected attacks
        for node_id in self.detected_attacks:
            node = self.network.nodes[node_id]
            if node_id in self.network.sinkhole_nodes:
                ax1.scatter(node.x, node.y, c='green', s=150, marker='o', 
                           edgecolors='black', linewidth=2, 
                           label='Correctly Detected' if node_id == self.detected_attacks[0] else "")
            else:
                ax1.scatter(node.x, node.y, c='orange', s=150, marker='s', 
                           edgecolors='black', linewidth=2, 
                           label='False Alarm' if node_id == self.detected_attacks[0] else "")
        
        ax1.set_xlabel('X Coordinate')
        ax1.set_ylabel('Y Coordinate')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Performance metrics
        ax2.set_title('ACO Performance Metrics', fontsize=14)
        metric_names = ['Detection Rate', 'False Alarm Rate', 'Packet Delivery Ratio', 'Message Drop']
        metric_values = [self.metrics['detection_rate'], self.metrics['false_alarm_rate'], 
                        self.metrics['packet_delivery_ratio'], self.metrics['message_drop']]
        
        bars = ax2.bar(metric_names, metric_values, color=['green', 'red', 'blue', 'orange'])
        ax2.set_ylabel('Percentage (%)')
        ax2.set_ylim(0, 100)
        
        for bar, value in zip(bars, metric_values):
            ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                    f'{value:.1f}%', ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig('wsn_aco_detection_results.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"Visualization saved as 'wsn_aco_detection_results.png'")
    
    def compare_with_research(self):
        """Compare results with research paper benchmarks."""
        print(f"\nCOMPARISON WITH RESEARCH PAPER:")
        print(f"Paper ACO Detection Rate: 87.06%")
        print(f"Our ACO Detection Rate: {self.metrics['detection_rate']:.2f}%")
        print(f"Paper ACO False Alarm Rate: 10.65%")
        print(f"Our ACO False Alarm Rate: {self.metrics['false_alarm_rate']:.2f}%")
        
        detection_diff = self.metrics['detection_rate'] - 87.06
        false_alarm_diff = self.metrics['false_alarm_rate'] - 10.65
        
        print(f"\nPERFORMANCE COMPARISON:")
        if detection_diff > 0:
            print(f"Detection Rate: {detection_diff:.2f}% better than research")
        else:
            print(f"Detection Rate: {abs(detection_diff):.2f}% worse than research")
            
        if false_alarm_diff < 0:
            print(f"False Alarm Rate: {abs(false_alarm_diff):.2f}% better than research")
        else:
            print(f"False Alarm Rate: {false_alarm_diff:.2f}% worse than research")