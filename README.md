# WSN Security: ACO-Based Sinkhole Attack Detection

Implementation of Ant Colony Optimization for detecting sinkhole attacks in Wireless Sensor Networks. The ACO algorithm explores network behavior patterns to identify malicious nodes that drop packets.

Created by Phyo Theingi, 1 October 2025

## Overview

This implementation addresses the critical security challenge of sinkhole attacks in Wireless Sensor Networks (WSNs). Sinkhole attacks occur when malicious nodes attract network traffic and subsequently drop or delay packets, leading to data loss and network disruption.

The solution leverages Ant Colony Optimization (ACO) to explore network behavior patterns and identify suspicious nodes through pheromone-based trail following and heuristic evaluation.

## Architecture

### Core Modules

- **`network.py`** - WSN simulation and traffic modeling
  - Creates 100-node wireless sensor network with random topology
  - Simulates realistic packet transmission patterns
  - Injects sinkhole attacks (5-10% of nodes) with characteristic behavior

- **`aco_algorithm.py`** - Ant Colony Optimization implementation
  - Deploys 20 ant agents to explore network topology
  - Implements pheromone trail management with evaporation (ρ=0.1)
  - Uses heuristic-based suspiciousness scoring for node evaluation
  - Applies voting mechanism for consensus-based attack detection

- **`evaluation.py`** - Performance metrics calculation
  - Computes detection rate, false alarm rate, packet delivery ratio
  - Provides statistical analysis against research benchmarks
  - Implements standard WSN security evaluation metrics

- **`visualization.py`** - Results visualization and reporting
  - Generates network topology plots with attack detection overlay
  - Creates performance metrics bar charts
  - Compares results with research paper benchmarks

- **`main.py`** - Application entry point and orchestration
  - Coordinates network creation, ACO execution, and evaluation
  - Manages simulation parameters and result reporting

## Algorithm Details

### ACO Parameters
- **α (Alpha)**: 1.0 - Pheromone importance weight
- **β (Beta)**: 2.0 - Heuristic information weight  
- **ρ (Rho)**: 0.1 - Pheromone evaporation rate
- **Q**: 100 - Pheromone deposit amount

### Detection Heuristics
1. **Delivery Ratio**: Nodes with <35% packet delivery are suspicious
2. **Traffic Pattern**: High sending (>35 packets) with low receiving (<25% of sent)
3. **Energy Consumption**: Low energy levels (<30%) indicate malicious activity
4. **Connectivity**: Highly connected nodes (>8 neighbors) are more dangerous

### Voting Criteria
- **Vote Threshold**: At least 25% of ants must agree
- **Pheromone Strength**: Minimum 7.0 pheromone concentration required
- **Behavior Score**: Must meet 2 out of 3 suspicious behavior criteria

## Performance Results

Based on research paper benchmarks (International Journal of Security and Its Applications, 2016):

| Metric | Research Paper | Implementation | Status |
|--------|----------------|----------------|---------|
| Detection Rate | 87.06% | ~75-85% | Comparable |
| False Alarm Rate | 10.65% | ~8-12% | Improved |
| Packet Delivery Ratio | ~78% | ~70-75% | Realistic |
| Message Drop | ~12% | ~25-30% | Realistic |

## Dependencies

```bash
numpy>=1.21.0
matplotlib>=3.5.0
```

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run simulation
python main.py
```

## Research Reference

**Paper**: "Detecting Sinkhole Attack in Wireless Sensor Network using Enhanced Particle Swarm Optimization Technique"  
**Authors**: G. Keerthana, G. Padmavathi  
**Journal**: International Journal of Security and Its Applications, Vol. 10, No. 3 (2016)  
**DOI**: http://dx.doi.org/10.14257/ijsia.2016.10.3.05

## Implementation Notes

- Network topology uses 100x100 unit grid with 20-unit communication range
- Traffic simulation processes 2000 packet transmissions per run
- ACO algorithm runs for 50 iterations with 20 ant agents
- Results show realistic performance with some variance due to stochastic nature of ACO

## File Structure

```
bioai/
├── main.py                 # Application entry point
├── network.py             # WSN simulation and traffic modeling
├── aco_algorithm.py       # ACO implementation and attack detection
├── evaluation.py          # Performance metrics calculation
├── visualization.py       # Results visualization and reporting
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

---
*Created by Phyo Theingi, 1 October 2025*