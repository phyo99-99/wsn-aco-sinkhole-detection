#!/usr/bin/env python3
"""
Evaluation module for ACO performance metrics
Calculates detection rate, false alarm rate, and other performance measures

This file implements performance evaluation for the ACO sinkhole detection system:
- Detection rate calculation (true positives / total attacks)
- False alarm rate computation (false positives / total detections)
- Packet delivery ratio and message drop rate analysis
- Comparison with research paper benchmarks
- Statistical validation of algorithm effectiveness

Created by Phyo Theingi, 1 October 2025
"""

class PerformanceEvaluator:
    """Evaluates ACO algorithm performance for sinkhole attack detection."""
    
    def __init__(self, network, detected_attacks):
        self.network = network
        self.detected_attacks = detected_attacks
        self.true_detections = 0
        self.false_alarms = 0
        
        self._calculate_metrics()
    
    def _calculate_metrics(self):
        self.true_detections = len([node for node in self.detected_attacks 
                                   if node in self.network.sinkhole_nodes])
        
        self.false_alarms = len([node for node in self.detected_attacks 
                                if node not in self.network.sinkhole_nodes])
    
    def calculate_detection_rate(self):
        if len(self.network.sinkhole_nodes) == 0:
            return 0.0
        return (self.true_detections / len(self.network.sinkhole_nodes)) * 100
    
    def calculate_false_alarm_rate(self):
        if len(self.detected_attacks) == 0:
            return 0.0
        return (self.false_alarms / len(self.detected_attacks)) * 100
    
    def calculate_packet_delivery_ratio(self):
        if self.network.total_packets_sent == 0:
            return 0.0
        return (self.network.total_packets_received / self.network.total_packets_sent) * 100
    
    def calculate_message_drop(self):
        if self.network.total_packets_sent == 0:
            return 0.0
        return ((self.network.total_packets_sent - self.network.total_packets_received) / 
                self.network.total_packets_sent) * 100
    
    def get_all_metrics(self):
        return {
            'detection_rate': self.calculate_detection_rate(),
            'false_alarm_rate': self.calculate_false_alarm_rate(),
            'packet_delivery_ratio': self.calculate_packet_delivery_ratio(),
            'message_drop': self.calculate_message_drop(),
            'true_detections': self.true_detections,
            'false_alarms': self.false_alarms,
            'total_attacks': len(self.network.sinkhole_nodes),
            'detected_attacks': len(self.detected_attacks)
        }
    
    def print_results(self):
        """Print formatted results."""
        metrics = self.get_all_metrics()
        
        print(f"\nDETECTION RESULTS:")
        print(f"Actual sinkhole attacks: {metrics['total_attacks']}")
        print(f"Attacks detected by ACO: {metrics['detected_attacks']}")
        print(f"True detections: {metrics['true_detections']}")
        print(f"False alarms: {metrics['false_alarms']}")
        
        print(f"\nPERFORMANCE METRICS:")
        print(f"Detection Rate: {metrics['detection_rate']:.2f}%")
        print(f"False Alarm Rate: {metrics['false_alarm_rate']:.2f}%")
        print(f"Packet Delivery Ratio: {metrics['packet_delivery_ratio']:.2f}%")
        print(f"Message Drop: {metrics['message_drop']:.2f}%")
        
        return metrics
