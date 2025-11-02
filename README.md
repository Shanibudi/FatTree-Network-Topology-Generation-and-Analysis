# FatTree Network Topology Generation and Analysis

## Overview-

This project implements a three-tier fat-tree network topology following the design principles described in https://dl.acm.org/doi/pdf/10.1145/1402946.1402967 

The script allows generate, analyze, and visualize fat-tree architectures for data center networks. It supports fault simulation through link failure modeling and provides tools to analyze the resulting network performance metrics (such as average path length) under various failure rates.

## How to run this code-
The script accepts the following command-line arguments:
Parameter  Type     Default   Description
--k        Integer  4         Number of ports per switch (must be even). Controls network size.
--fail     Float    0.0       Percentage of link failures to simulate (0–100).

To run the script, run for example:

```python fattree.py --k 4 --fail 1```

This command builds a 3-tier fat-tree with k=4 and randomly removes 1% of its links before computing metrics.


[1] M. Al-Fares, A. Loukissas, and A. Vahdat, “A scalable, commodity data center network architecture,” SIGCOMM Comput. Commun. Rev., vol. 38, no. 4, pp. 63–74, 2008.
