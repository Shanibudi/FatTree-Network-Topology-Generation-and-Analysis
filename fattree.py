import networkx as nx
import matplotlib.pyplot as plt
import random
import argparse
import numpy as np

def generate_fat_tree(k):
    """Generate a three-tier fat-tree topology as per Al-Fares et al. (2008)."""
    G = nx.Graph()

    num_pods = k
    num_core_switches = (k // 2) ** 2
    num_agg_switches = k * (k // 2)
    num_edge_switches = k * (k // 2)
    num_hosts = (k ** 3) // 4

    core_switches = [f"C{i}" for i in range(num_core_switches)]
    agg_switches = [f"A{i}" for i in range(num_agg_switches)]
    edge_switches = [f"E{i}" for i in range(num_edge_switches)]
    hosts = [f"H{i}" for i in range(num_hosts)]

    G.add_nodes_from(core_switches, layer="core")
    G.add_nodes_from(agg_switches, layer="aggregation")
    G.add_nodes_from(edge_switches, layer="edge")
    G.add_nodes_from(hosts, layer="host")

    # Connect core to aggregation
    for i, core in enumerate(core_switches):
        for j in range(num_pods):
            agg_index = j * (k // 2) + (i // (k // 2))
            G.add_edge(core, agg_switches[agg_index])

    # Connect aggregation to edge within each pod
    for pod in range(num_pods):
        agg_range = range(pod * (k // 2), (pod + 1) * (k // 2))
        edge_range = range(pod * (k // 2), (pod + 1) * (k // 2))
        for agg in agg_range:
            for edge in edge_range:
                G.add_edge(agg_switches[agg], edge_switches[edge])

    # Connect edge switches to hosts
    host_id = 0
    for edge in edge_switches:
        for _ in range(k // 2):
            G.add_edge(edge, hosts[host_id])
            host_id += 1

    return G
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, default=4, help="Port count (even number)")
    parser.add_argument("--fail", type=float, default=0.0, help="Percentage of link failures")
    args = parser.parse_args()

    G = generate_fat_tree(args.k)
    print(f"Generated fat-tree with {len(G.nodes)} nodes and {len(G.edges)} edges")
if __name__ == "__main__":
    main()
