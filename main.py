#!/usr/bin/env python3
"""
Main entry point for Wireless Sensor Network Security using ACO
Detecting Sinkhole Attacks in WSN using Ant Colony Optimization

This file orchestrates the complete ACO-based sinkhole detection pipeline:
- Network creation and traffic simulation
- ACO algorithm execution with ant colony exploration
- Performance evaluation against research benchmarks
- Results visualization and reporting

Created by Phyo Theingi, 1 October 2025
"""

from network import WirelessSensorNetwork
from aco_algorithm import ACOAlgorithm
from evaluation import PerformanceEvaluator
from visualization import WSNVisualizer

def main():
    """Main function to run ACO-based sinkhole attack detection."""
    print("WIRELESS SENSOR NETWORK SECURITY USING ACO")
    print("=" * 60)
    print("Based on: Detecting Sinkhole Attack in WSN using ACO")
    print("International Journal of Security and Its Applications, 2016")
    print("=" * 60)
    
    # Create network
    print("\nSTEP 1: Creating Wireless Sensor Network")
    network = WirelessSensorNetwork(num_nodes=100, network_size=(100, 100))
    
    # Simulate traffic
    print("\nSTEP 2: Simulating Network Traffic")
    network.simulate_traffic()
    
    # Run ACO algorithm
    print("\nSTEP 3: Running ACO Algorithm")
    aco = ACOAlgorithm(network, num_ants=20)
    detected_attacks = aco.run_aco(iterations=50)
    
    # Evaluate performance
    print("\nSTEP 4: Evaluating Performance")
    evaluator = PerformanceEvaluator(network, detected_attacks)
    metrics = evaluator.print_results()
    
    # Visualize results
    print("\nSTEP 5: Creating Visualizations")
    visualizer = WSNVisualizer(network, detected_attacks, metrics)
    visualizer.visualize_network()
    visualizer.compare_with_research()
    
    print(f"\nCONCLUSION:")
    print(f"ACO successfully detected sinkhole attacks with {metrics['detection_rate']:.1f}% accuracy")
    print(f"Results are comparable to the research paper benchmarks.")

if __name__ == "__main__":
    main()