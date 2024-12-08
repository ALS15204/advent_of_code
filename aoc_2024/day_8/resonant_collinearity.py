from collections import Counter
import itertools
import string

ANTENNA_CHAR = set(string.digits + string.ascii_letters)
EMPTY_CHAR = '.'


def propagate_direction(location_pair):
    loc1_to_loc2 = (location_pair[1][0] - location_pair[0][0]), (location_pair[1][1] - location_pair[0][1])
    return loc1_to_loc2[0], loc1_to_loc2[1]


def get_antinode_locs(location_pair):
    loc1_to_loc2 = propagate_direction(location_pair)
    antinode_locs = [(location_pair[0][0] - loc1_to_loc2[0], location_pair[0][1] - loc1_to_loc2[1])]
    antinode_locs += [(location_pair[1][0] + loc1_to_loc2[0], location_pair[1][1] + loc1_to_loc2[1])]
    return antinode_locs


if __name__ == '__main__':
    map_data = {}
    with open('data/input.dat') as f:
        lines = f.readlines()
        for idx_line, line in enumerate(lines):
            line = line.strip()
            for idx_char, char in enumerate(line):
                map_data[(idx_line, idx_char)] = char

    antenna_count = Counter([c for c in map_data.values() if c in ANTENNA_CHAR])
    all_antinode_locs = set()
    for c in antenna_count:
        c_locations = [k for k, v in map_data.items() if v == c]
        for pair in itertools.combinations(c_locations, 2):
            all_antinode_locs.update(get_antinode_locs(pair))
    n_antinodes = sum(map_data.get(loc) is not None for loc in all_antinode_locs)
    print(n_antinodes)

    all_antinode_locs = set()
    for c in antenna_count:
        c_locations = [k for k, v in map_data.items() if v == c]
        for pair in itertools.combinations(c_locations, 2):
            extend_direction = propagate_direction(pair)
            for idx, loc in enumerate(pair, 1):
                search = True
                n_step = 0
                while search:
                    new_loc = (
                        loc[0] + n_step * (-1)**idx * extend_direction[0], 
                        loc[1] + n_step * (-1)**idx * extend_direction[1]
                    )
                    if new_loc in map_data:
                        all_antinode_locs.add(new_loc)
                    else:
                        search = False
                    n_step += 1
    n_antinodes = sum(map_data.get(loc) is not None for loc in all_antinode_locs)
    print(n_antinodes)
