# FatTree Network Topology Generation and Analysis

## Overview-

This project implements a three-tier fat-tree network topology following the design principles described in paper [1] https://dl.acm.org/doi/pdf/10.1145/1402946.1402967 

The script allows generate, analyze, and visualize fat-tree architectures for data center networks. It supports fault simulation through link failure modeling and provides tools to analyze the resulting network performance metrics (such as average path length) under various failure rates.

All generated visualizations and experimental results are automatically saved under the `plots/` directory.  
This includes:
- The fat-tree topology before and after link failures, illustrating how the network structure changes following link disruptions.  
- The experimental result plots, showing how key metrics evolve with different topology sizes and link failure percentages.  

All figures can be found inside the `plots/` folder within this repository.

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
In order to run this code, you will need to install the following dependencies:

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

This experiment analyzes how the average path length in a three-tier fat-tree topology changes as a function of the link failure rate.
Simulations were conducted for five network sizes — k = 4, 6, 8, 10, and 12, where k represents the number of ports per switch.
For each configuration, random link failures were introduced at discrete rates of \{0, 1, 2, 5, 10, 20, 30, 40\}\% of the total links, and the mean shortest-path distance was computed across all reachable hosts.

The results show that smaller networks (e.g., k=4) exhibit higher variability in the average path length as the failure rate increases.
This instability occurs because in smaller topologies, each failed link represents a larger fraction of the total connectivity, making the network more sensitive to random failures.
In contrast, larger fat-tree configurations (k \geq 8) remain remarkably stable, showing only minor or gradual increases in path length as the failure percentage grows.
This demonstrates the strong fault tolerance and inherent redundancy of the fat-tree architecture — as k increases, the number of alternative equal-cost paths grows, maintaining stable connectivity and nearly constant average path lengths even under significant link failures.

A plot demonstrating this experiment shown below:

<img width="2072" height="1634" alt="image" src="https://github.com/user-attachments/assets/7bd1d886-7f39-472b-862a-0f7ec53aaf7e" />


### Experiment 2: Hosts Supported vs. Switch Port Count

This experiment analyzes how the number of supported hosts scales with the switch port count (k).
For each value of k = 4, 6, 8, 10 and 12 , the theoretical maximum number of hosts in a three-tier fat-tree was computed using the formula: k<sup>3</sup> / 4 .
This metric represents the scalability potential of the fat-tree architecture.

The results clearly show that the number of supported hosts increases cubically with the port count.
For instance, increasing k from 4 to 12 results in a dramatic rise from 16 hosts to 432 hosts, emphasizing the excellent scalability of the fat-tree design.
This property demonstrates why fat-tree topologies are widely adopted in large-scale data centers — they allow the network to expand significantly without fundamental architectural changes, maintaining balance, symmetry, and performance efficiency even as the system grows.

A plot demonstrating this experiment shown below:

<img width="2085" height="1634" alt="image" src="https://github.com/user-attachments/assets/c8ff41a1-e14f-419b-ae11-88290537bfb0" />


## References

[1] M. Al-Fares, A. Loukissas, and A. Vahdat, “A scalable, commodity data center network architecture,” SIGCOMM Comput. Commun. Rev., vol. 38, no. 4, pp. 63–74, 2008.
