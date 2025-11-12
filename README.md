# FatTree Network Topology Generation and Analysis

## Overview-

This project implements a three-tier fat-tree network topology following the design principles described in paper [1] https://dl.acm.org/doi/pdf/10.1145/1402946.1402967 

The script allows generate, analyze, and visualize fat-tree architectures for data center networks. It supports fault simulation through link failure modeling and provides tools to analyze the resulting network performance metrics (such as average path length) under various failure rates.

## Topology Structure-

For a fat-tree with port count k:

| Layer | Number of Devices |
|--------|--------------------|
| Core Switches | (k/2)<sup>2</sup> |
| Aggregation Switches | k<sup>2</sup> / 2 |
| Edge Switches | k<sup>2</sup> / 2 |
| Hosts | k<sup>3</sup> / 4 |

Each pod has k/2 edge + k/2 aggregation switches.

## Requirements-
In order to run this code, you will need ti install the folowing dependencies:

```pip install networkx matplotlib numpy```

## How to run this code-

### Input parameters- 
The script accepts the following command-line arguments:

| Parameter | Type | Default | Description |
|------------|------|----------|-------------|
| `--k` | Integer | 4 | Number of ports per switch (must be even). Controls network size. |
| `--fail` | Float | 0.0 | Percentage of link failures to simulate (0–100). |
| `--run_experiments` | Flag (Boolean) | False | When included, runs two experiments: (1) average path length vs. link failure rate, and (2) number of supported hosts vs. switch port count. |

To run the script, run for example:

```python fattree.py --k 4 --fail 1```

This command builds a 3-tier fat-tree with k=4 and randomly removes 1% of its links before computing metrics.

## Metric Analysis and Results

#### Experiment 1: Impact of Link Failures on Average Path Length

This experiment evaluates how the average path length in a three-tier fat-tree topology changes as a function of link failure rate.
Simulations were conducted for three network sizes — k = 4, 6, and 8, where k represents the number of ports per switch.
For each configuration we introduced random link failures at the discrete rates \{0, 1, 2, 5, 10\}\% of the total links and then computed the mean shortest path length across all reachable hosts.

The results show that the average path length remains almost constant as the failure rate increases, demonstrating the high resilience and redundancy of the fat-tree topology. 
Due to the multiple equal-cost paths characteristic of fat-tree topologies, this topology ensure that even when several links fail, connectivity and performance are only minimally affected.
Larger configurations (higher k) exhibit slightly higher path lengths due to deeper hierarchical depth but also demonstrate stronger robustness against link losses.

A plot demonstrating this experiment can be found at plots/failure_vs_path_length.png.

### Experiment 2: Hosts Supported vs. Switch Port Count

This experiment analyzes how the number of supported hosts scales with the switch port count (k).
For each value of k = 4, 6, 8, the theoretical maximum number of hosts in a three-tier fat-tree was computed using the formula: k<sup>3</sup> / 4 .
This metric captures the scalability potential of the network.

The number of supported hosts increases cubically with the switch port count.
For example, increasing k from 4 to 8 results in an eightfold increase in host capacity, demonstrating the excellent scalability of the fat-tree design.
This behavior highlights why fat-tree topologies are widely adopted in large-scale data centers — they allow significant expansion without redesigning the network architecture.

[1] M. Al-Fares, A. Loukissas, and A. Vahdat, “A scalable, commodity data center network architecture,” SIGCOMM Comput. Commun. Rev., vol. 38, no. 4, pp. 63–74, 2008.
