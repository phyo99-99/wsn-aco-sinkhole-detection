#!/usr/bin/env python3
"""
Network module for Wireless Sensor Network
Handles network creation, node management, and traffic simulation

This file implements the WSN simulation environment including:
- Random node placement and connectivity establishment
- Sinkhole attack injection with realistic behavior patterns
- Traffic simulation with packet transmission modeling
- Node behavior data collection for ACO analysis

Created by Phyo Theingi, 1 October 2025
"""

import numpy as np
import random
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class SensorNode:
    """Wireless sensor node in the network."""
    node_id: int
    x: float
    y: float
    is_malicious: bool = False
    energy: float = 100.0
    packets_sent: int = 0
    packets_received: int = 0
    neighbors: List[int] = None
    
    def __post_init__(self):
        if self.neighbors is None:
            self.neighbors = []

class WirelessSensorNetwork:
    """Manages the wireless sensor network and traffic simulation."""
    
    def __init__(self, num_nodes=100, network_size=(100, 100)):
        self.num_nodes = num_nodes
        self.network_size = network_size
        self.nodes = {}
        self.sinkhole_nodes = []
        self.total_packets_sent = 0
        self.total_packets_received = 0
        
        self._create_network()
        self._inject_sinkhole_attacks()
    
    def _create_network(self):
        """Create a wireless sensor network with random node placement."""
        print("Creating Wireless Sensor Network...")
        
        for i in range(self.num_nodes):
            x = random.uniform(0, self.network_size[0])
            y = random.uniform(0, self.network_size[1])
            
            self.nodes[i] = SensorNode(
                node_id=i,
                x=x,
                y=y,
                energy=random.uniform(80, 100)
            )
        
        communication_range = 20
        for i in range(self.num_nodes):
            for j in range(i+1, self.num_nodes):
                distance = np.sqrt((self.nodes[i].x - self.nodes[j].x)**2 + 
                                 (self.nodes[i].y - self.nodes[j].y)**2)
                if distance <= communication_range:
                    self.nodes[i].neighbors.append(j)
                    self.nodes[j].neighbors.append(i)
        
        print(f"Network created with {self.num_nodes} nodes")
        print(f"Average neighbors per node: {np.mean([len(n.neighbors) for n in self.nodes.values()]):.1f}")
    
    def _inject_sinkhole_attacks(self):
        """Inject sinkhole attacks into the network (5-10% of nodes)."""
        num_attacks = random.randint(5, 10)
        self.sinkhole_nodes = random.sample(range(self.num_nodes), num_attacks)
        
        for node_id in self.sinkhole_nodes:
            self.nodes[node_id].is_malicious = True
            self.nodes[node_id].packets_sent = random.randint(80, 120)
            self.nodes[node_id].packets_received = random.randint(5, 25)
            self.nodes[node_id].energy = random.uniform(20, 40)
        
        print(f"Injected {len(self.sinkhole_nodes)} sinkhole attacks")
        print(f"Malicious nodes: {self.sinkhole_nodes}")
    
    def simulate_traffic(self):
        """Simulate realistic network traffic with sinkhole behavior."""
        print("Simulating network traffic...")
        
        for _ in range(2000):
            source = random.randint(0, self.num_nodes - 1)
            destination = random.randint(0, self.num_nodes - 1)
            
            if source != destination:
                self.nodes[source].packets_sent += 1
                self.total_packets_sent += 1
                
                if self.nodes[source].is_malicious:
                    if random.random() < 0.45:
                        self.nodes[destination].packets_received += 1
                        self.total_packets_received += 1
                else:
                    if random.random() < 0.85:
                        self.nodes[destination].packets_received += 1
                        self.total_packets_received += 1
        
        for node_id in self.sinkhole_nodes:
            extra_packets = random.randint(20, 50)
            self.nodes[node_id].packets_sent += extra_packets
            self.total_packets_sent += extra_packets
    
    def get_node_behavior(self, node_id):
        node = self.nodes[node_id]
        delivery_ratio = node.packets_received / max(node.packets_sent, 1)
        return {
            'delivery_ratio': delivery_ratio,
            'packets_sent': node.packets_sent,
            'packets_received': node.packets_received,
            'is_malicious': node.is_malicious
        }
