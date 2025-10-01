#!/usr/bin/env python3
"""
ACO Algorithm module for sinkhole attack detection
Implements the core Ant Colony Optimization algorithm

This file contains the main ACO implementation including:
- Ant colony creation and movement with pheromone-based path selection
- Heuristic-based suspiciousness detection using multiple criteria
- Pheromone trail management with evaporation and deposition
- Voting mechanism for consensus-based attack detection
- Integration with research paper parameters (α=1.0, β=2.0, ρ=0.1)

Created by Phyo Theingi, 1 October 2025
"""

import numpy as np          # For math operations and arrays
import random              # For random choices
from dataclasses import dataclass  # For easy data structures
from typing import List, Dict      # Type hints

@dataclass
class Ant:
    """Ant agent for ACO-based attack detection."""
    current_node: int              # Which node the ant is currently at
    visited_nodes: List[int] = None    # List of nodes this ant has visited
    suspicious_nodes: List[int] = None # List of nodes this ant thinks are suspicious
    
    def __post_init__(self):
        # Initialize empty lists if they're None
        if self.visited_nodes is None:
            self.visited_nodes = []
        if self.suspicious_nodes is None:
            self.suspicious_nodes = []

class ACOAlgorithm:
    """Ant Colony Optimization algorithm for sinkhole attack detection."""
    
    def __init__(self, network, num_ants=30):
        self.network = network
        self.num_ants = num_ants
        self.ants = []
        self.pheromone_matrix = np.ones((network.num_nodes, network.num_nodes)) * 0.5
        self.detected_attacks = []
        
        # ACO parameters from research paper
        self.alpha = 1.0  # pheromone importance
        self.beta = 2.0   # heuristic importance
        self.rho = 0.1    # evaporation rate
        self.Q = 100      # pheromone deposit constant
        
    def create_ant_colony(self):
        self.ants = []
        for _ in range(self.num_ants):
            start_node = random.randint(0, self.network.num_nodes - 1)
            self.ants.append(Ant(current_node=start_node))
    
    def ant_movement(self, ant):
        current_node = ant.current_node
        ant.visited_nodes.append(current_node)
        
        node_behavior = self.network.get_node_behavior(current_node)
        delivery_ratio = node_behavior['delivery_ratio']
        packets_sent = node_behavior['packets_sent']
        
        # Calculate suspiciousness using heuristics
        suspiciousness_score = 0
        
        if delivery_ratio < 0.38:
            suspiciousness_score += 0.4
        
        if packets_sent > 35 and delivery_ratio < 0.28:
            suspiciousness_score += 0.3
        
        if hasattr(self.network.nodes[current_node], 'energy'):
            energy = self.network.nodes[current_node].energy
            if energy < 40:
                suspiciousness_score += 0.2
                
        current_node_obj = self.network.nodes[current_node]
        if len(current_node_obj.neighbors) > 6:
            suspiciousness_score += 0.1
        
        if suspiciousness_score > 0.7:
            ant.suspicious_nodes.append(current_node)
        
        # Select next node using ACO probability
        current_node_obj = self.network.nodes[current_node]
        available_nodes = [n for n in current_node_obj.neighbors 
                          if n not in ant.visited_nodes[-3:]]
        
        if available_nodes:
            probabilities = []
            for next_node in available_nodes:
                pheromone = self.pheromone_matrix[current_node][next_node]
                distance = 1.0
                next_behavior = self.network.get_node_behavior(next_node)
                heuristic = 1.0 / (distance + 0.1)
                
                if next_behavior['delivery_ratio'] < 0.4:
                    heuristic *= 2.0
                
                probability = (pheromone ** self.alpha) * (heuristic ** self.beta)
                probabilities.append(probability)
            
            if probabilities and sum(probabilities) > 0:
                total_prob = sum(probabilities)
                probabilities = [p/total_prob for p in probabilities]
                next_node = np.random.choice(available_nodes, p=probabilities)
                ant.current_node = next_node
    
    def update_pheromones(self):
        # Evaporation
        self.pheromone_matrix *= (1 - self.rho)
        
        # Deposition
        for ant in self.ants:
            if ant.suspicious_nodes:
                pheromone_amount = self.Q * len(ant.suspicious_nodes)
                
                for i in range(len(ant.visited_nodes) - 1):
                    current = ant.visited_nodes[i]
                    next_node = ant.visited_nodes[i + 1]
                    if next_node in ant.suspicious_nodes:
                        self.pheromone_matrix[current][next_node] += pheromone_amount
                        
                for suspicious_node in ant.suspicious_nodes:
                    suspicious_obj = self.network.nodes[suspicious_node]
                    for neighbor in suspicious_obj.neighbors:
                        self.pheromone_matrix[suspicious_node][neighbor] += pheromone_amount * 0.5
    
    def detect_attacks(self):
        print("Detecting sinkhole attacks using ACO...")
        
        # Collect votes from all ants
        all_suspicious = []
        for ant in self.ants:
            all_suspicious.extend(ant.suspicious_nodes)
        
        vote_count = {}
        for node_id in all_suspicious:
            vote_count[node_id] = vote_count.get(node_id, 0) + 1
        
        self.detected_attacks = []
        
        for node_id, votes in vote_count.items():
            vote_threshold = max(2, len(self.ants) // 5)
            max_pheromone = np.max(self.pheromone_matrix[node_id])
            pheromone_threshold = 7.0
            
            node_behavior = self.network.get_node_behavior(node_id)
            behavior_score = 0
            if node_behavior['delivery_ratio'] < 0.4:
                behavior_score += 1
            if node_behavior['packets_sent'] > 30:
                behavior_score += 1
            if node_behavior['packets_received'] < node_behavior['packets_sent'] * 0.3:
                behavior_score += 1
                
            if (votes >= vote_threshold and 
                max_pheromone >= pheromone_threshold and 
                behavior_score >= 2):
                self.detected_attacks.append(node_id)
        
        return self.detected_attacks
    
    def run_aco(self, iterations=100):
        print("Running ACO Algorithm...")
        print(f"Parameters: {self.num_ants} ants, {iterations} iterations")
        print(f"Alpha={self.alpha}, Beta={self.beta}, Rho={self.rho}")
        
        self.create_ant_colony()
        
        for iteration in range(iterations):
            for ant in self.ants:
                self.ant_movement(ant)
            
            self.update_pheromones()
            
            if iteration % 20 == 0:
                current_suspicious = len(set([node for ant in self.ants for node in ant.suspicious_nodes]))
                print(f"Iteration {iteration}: {current_suspicious} suspicious nodes found")
        
        detected = self.detect_attacks()
        
        print(f"ACO completed: {len(detected)} attacks detected")
        return detected
