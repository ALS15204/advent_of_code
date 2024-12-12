import numpy as np
from scipy import ndimage

HORIZONTAL = [(0, 1), (0, -1)]
VERTICAL = [(1, 0), (-1, 0)]


def compute_perimeters(garden_plot_per_patch):
    return abs(np.diff(garden_plot_per_patch, axis=0)).sum() + abs(np.diff(garden_plot_per_patch, axis=1)).sum()


def compute_number_of_sides(garden_plot_per_patch):
    indices = np.argwhere(garden_plot_per_patch)
    n_corners = 0
    for idx in indices:
        neighbors = {
            'N': garden_plot_per_patch[tuple(idx + np.array(HORIZONTAL[0]))],
            'E': garden_plot_per_patch[tuple(idx + np.array(VERTICAL[0]))],
            'S': garden_plot_per_patch[tuple(idx + np.array(HORIZONTAL[1]))],
            'W': garden_plot_per_patch[tuple(idx + np.array(VERTICAL[1]))],
            'NE': garden_plot_per_patch[tuple(idx + np.array(HORIZONTAL[0]) + np.array(VERTICAL[0]))],
            'SE': garden_plot_per_patch[tuple(idx + np.array(HORIZONTAL[1]) + np.array(VERTICAL[0]))],
            'NW': garden_plot_per_patch[tuple(idx + np.array(HORIZONTAL[0]) + np.array(VERTICAL[1]))],
            'SW': garden_plot_per_patch[tuple(idx + np.array(HORIZONTAL[1]) + np.array(VERTICAL[1]))]
        }

        if not any(neighbors.values()): n_corners += 4
        if neighbors['N'] and not any(neighbors[k] for k in ['E', 'S', 'W']): n_corners += 2
        if neighbors['E'] and not any(neighbors[k] for k in ['S', 'W', 'N']): n_corners += 2
        if neighbors['S'] and not any(neighbors[k] for k in ['W', 'N', 'E']): n_corners += 2
        if neighbors['W'] and not any(neighbors[k] for k in ['N', 'E', 'S']): n_corners += 2
        if neighbors['S'] and neighbors['E'] and not neighbors['N'] and not neighbors['W']: n_corners += 1
        if neighbors['S'] and neighbors['W'] and not neighbors['N'] and not neighbors['E']: n_corners += 1
        if neighbors['N'] and neighbors['E'] and not neighbors['S'] and not neighbors['W']: n_corners += 1
        if neighbors['N'] and neighbors['W'] and not neighbors['S'] and not neighbors['E']: n_corners += 1
        if neighbors['E'] and neighbors['N'] and not neighbors['NE']: n_corners += 1
        if neighbors['E'] and neighbors['S'] and not neighbors['SE']: n_corners += 1
        if neighbors['W'] and neighbors['N'] and not neighbors['NW']: n_corners += 1
        if neighbors['W'] and neighbors['S'] and not neighbors['SW']: n_corners += 1
    return n_corners


def find_clusters(array):
    clustered = np.empty_like(array, dtype=int)
    unique_vals = np.unique(array)
    cluster_count = 0
    for val in unique_vals:
        labelling, label_count = ndimage.label(array == val)
        for k in range(1, label_count + 1):
            clustered[labelling == k] = str(cluster_count)
            cluster_count += 1
    return clustered, cluster_count


if __name__ == "__main__":
    with open("data/input.dat") as file:
        garden_plot = np.array([list(line.strip()) for line in file.readlines()])
    garden_plot, n_cluster = find_clusters(garden_plot)
    new_garden_plot = np.zeros((garden_plot.shape[0] + 2, garden_plot.shape[1] + 2), dtype=int)
    new_garden_plot[:, :] = -1
    new_garden_plot[1:-1, 1:-1] = garden_plot

    total_cost = 0
    for cluster_idx in range(n_cluster):
        internal_area = new_garden_plot == cluster_idx
        total_cost += (internal_area.sum() * compute_perimeters(internal_area))
    print(total_cost)

    total_cost = 0
    for cluster_idx in range(n_cluster):
        internal_area = new_garden_plot == cluster_idx
        total_cost += (internal_area.sum() * compute_number_of_sides(internal_area))
    print(total_cost)