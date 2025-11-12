import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
import argparse
import os


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


def simulate_failures(G, failure_rate):
    """Randomly remove a percentage of links."""
    num_failures = int(len(G.edges) * failure_rate / 100)
    failed_edges = random.sample(list(G.edges), num_failures)
    G.remove_edges_from(failed_edges)
    return failed_edges


def average_path_length(G):
    """Compute average path length of the largest connected component."""
    if nx.is_connected(G):
        return nx.average_shortest_path_length(G)
    else:
        largest_cc = G.subgraph(max(nx.connected_components(G), key=len))
        return nx.average_shortest_path_length(largest_cc)


def hierarchical_pos(G):
    """Return positions for a top-down hierarchical layout."""
    layers = {"core": 3, "aggregation": 2, "edge": 1, "host": 0}
    pos = {}
    layer_nodes = {l: [n for n, d in G.nodes(data=True) if d["layer"] == l] for l in layers}
    for layer, nodes in layer_nodes.items():
        y = layers[layer]
        x_positions = np.linspace(-1, 1, len(nodes))
        for i, node in enumerate(nodes):
            pos[node] = (x_positions[i], y)
    return pos


# Experiment 1: Average path length vs. link failure rate
def experiment_failure_impact(k_values, failure_rates):
    results = {}
    for k in k_values:
        avg_lengths = []
        for fail in failure_rates:
            G = generate_fat_tree(k)
            simulate_failures(G, fail)
            avg_len = average_path_length(G)
            avg_lengths.append(avg_len)
        results[k] = avg_lengths
    return results


# Experiment 2: Hosts supported vs. switch port count
def experiment_hosts_vs_ports(k_values):
    return [(k ** 3) / 4 for k in k_values]


def main():
    # Command-line arguments
    parser = argparse.ArgumentParser(description="Fat-Tree Topology Analysis")
    parser.add_argument("--k", type=int, default=4, help="Number of ports per switch (even number)")
    parser.add_argument("--fail", type=float, default=0.0, help="Percentage of link failures (0–100)")
    parser.add_argument("--run_experiments", action="store_true", help="Run performance experiments")
    args = parser.parse_args()

    # Ensure 'plots' directory exists
    os.makedirs("plots", exist_ok=True)

    # Visualization of single topology 
    G = generate_fat_tree(args.k)
    print(f"Generated fat-tree topology (k={args.k}) with {len(G.nodes)} nodes and {len(G.edges)} edges")

    if args.fail > 0:
        simulate_failures(G, args.fail)
        print(f"Simulated {args.fail}% link failures")

    avg_len = average_path_length(G)
    print(f"Average path length: {avg_len:.3f}")

    # Hierarchical visualization
    pos = hierarchical_pos(G)
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos,
            node_size=60,
            with_labels=False,
            node_color=[{"core": "red", "aggregation": "orange", "edge": "green", "host": "skyblue"}[G.nodes[n]["layer"]] for n in G.nodes()])
    plt.title(f"Hierarchical Fat-Tree (k={args.k}, Fail={args.fail}%)")
    plt.axis("off")
    plt.savefig(f"plots/fattree_topology_k{args.k}_fail{args.fail}.png", dpi=300, bbox_inches="tight")
    plt.show()

    # Run performance experiments (optional)
    if args.run_experiments:
        print("\nRunning experiments...\n")
        k_values = [4, 6, 8, 10, 12]
        failure_rates = [0, 1, 2, 5, 10, 15, 20]

        # Experiment 1
        results = experiment_failure_impact(k_values, failure_rates)
        plt.figure(figsize=(8, 6))
        for k in k_values:
            plt.plot(failure_rates, results[k], marker="o", label=f"k={k}")
        plt.xlabel("Link Failure Rate (%)")
        plt.ylabel("Average Path Length")
        plt.title("Impact of Link Failures on Average Path Length in Fat-Tree Topology")
        plt.legend()
        plt.grid(True)
        plt.savefig("plots/failure_vs_path_length.png", dpi=300, bbox_inches="tight")
        plt.show()

        # Experiment 2
        hosts = experiment_hosts_vs_ports(k_values)
        plt.figure(figsize=(8, 6))
        plt.plot(k_values, hosts, marker="s", color="darkgreen")
        plt.xlabel("Number of Ports per Switch (k)")
        plt.ylabel("Number of Supported Hosts")
        plt.title("Hosts Supported vs. Switch Port Count in Fat-Tree Network")
        plt.grid(True)
        plt.savefig("plots/hosts_vs_ports.png", dpi=300, bbox_inches="tight")
        plt.show()


if __name__ == "__main__":
    main()
