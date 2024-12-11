from dataclasses import dataclass

EMPTY = "."


@dataclass
class DiskFile:
    id: int
    start_idx: int
    size: int

    @property
    def end_idx(self):
        return self.start_idx + self.size - 1

    def __eq__(self, other):
        return self.id == other.id


@dataclass
class EmptyDisk:
    start_idx: int
    size: int

    @property
    def end_idx(self):
        return self.start_idx + self.size - 1

    def can_fit(self, disk_file):
        return self.size >= disk_file.size

    def is_contiguous(self, other):
        return self.end_idx + 1 == other.start_idx

    def merge(self, other):
        return EmptyDisk(self.start_idx, self.size + other.size)

    def __eq__(self, other):
        return self.start_idx == other.start_idx and self.size == other.size


def diskmap_tuple_to_str(idx, disk_map_tuple: tuple):
    return str(idx)*disk_map_tuple[0] + '.'*disk_map_tuple[1]
    

def get_disk_map_dict(disk_map_str: str):
    disk_map_dict = {
        idx: (int(disk_map_str[idx * 2]), int(disk_map_str[idx * 2 + 1]))
        for idx in range(len(disk_map_str) // 2)
    }
    if len(disk_map_str) % 2 != 0:
        disk_map_dict[len(disk_map_dict)] = (int(disk_map_str[-1]), 0)
    return disk_map_dict


def represent_disk_map(disk_map_dict: dict):
    disk_map = []
    for idx in sorted(disk_map_dict.keys()):
        disk_map.extend([idx] * disk_map_dict[idx][0])
        disk_map.extend([EMPTY] * disk_map_dict[idx][1])
    return disk_map


def fragment_disk_by_block(disk_repr_list: list):
    n_empty_spaces = disk_repr_list.count(EMPTY)
    empty_indices = [idx for idx, char in enumerate(disk_repr_list) if char == EMPTY]
    reversed_numbers = [(idx, num) for idx, num in enumerate(disk_repr_list) if num != EMPTY][::-1]
    for idx in empty_indices:
        last_number_idx, last_number = reversed_numbers.pop(0)
        disk_repr_list[idx] = last_number
        disk_repr_list[last_number_idx] = EMPTY
        disk_repr_str = "".join(map(str, disk_repr_list))
        if disk_repr_str.find(EMPTY) == len(disk_repr_str) - n_empty_spaces:
            break
    return disk_repr_list


def fragment_disk_by_file(disk_repr_dict: dict):
    all_files = []
    empty_space = []
    current_idx = 0
    for file_id, (size, n_empty_blocks) in sorted(disk_repr_dict.items(), key=lambda x: x[0]):
        all_files.append(DiskFile(file_id, current_idx, size))
        empty_space.append(EmptyDisk(all_files[-1].end_idx + 1, n_empty_blocks))
        current_idx = empty_space[-1].end_idx + 1
    for file in all_files[::-1]:
        for idx, space in enumerate(sorted(empty_space, key=lambda x: x.start_idx)):
            if space.can_fit(file):
                empty_space.append(EmptyDisk(file.start_idx, file.size))
                file.start_idx = space.start_idx
                if space.size == file.size:
                    empty_space.pop(idx)
                else:
                    space.start_idx += file.size
                    space.size -= file.size
                break
        empty_space = sorted(empty_space, key=lambda x: x.start_idx)
        for idx, space in enumerate(empty_space[:-1]):
            if space.is_contiguous(empty_space[idx + 1]):
                space.merge(empty_space.pop(idx + 1))
    return sorted(all_files, key=lambda x: x.start_idx)


def get_checksum(disk_repr_list: list):
    return sum(idx * int(num) for idx, num in enumerate(disk_repr_list) if num != EMPTY)


if __name__ == "__main__":
    with open("data/example.dat") as f:
        disk_map_str = f.read().strip()
    disk_repr_str_dict = get_disk_map_dict(disk_map_str)
    disk_repr_list = represent_disk_map(disk_repr_str_dict)
    # frag_disk_repr_list = fragment_disk_by_block(disk_repr_list)
    # print(get_checksum(frag_disk_repr_list))

    frag_disk_files = fragment_disk_by_file(disk_repr_str_dict)
    frag_disk_repr_list = [EMPTY] * len(disk_repr_list)
    for file in frag_disk_files:
        frag_disk_repr_list[file.start_idx:file.end_idx + 1] = [file.id] * file.size
    print(get_checksum(frag_disk_repr_list))
