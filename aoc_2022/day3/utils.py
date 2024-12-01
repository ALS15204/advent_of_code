from typing import Set


def letter_to_priority(letter: str):
    letter_ord = ord(letter)
    return letter_ord - 96 if letter_ord >= 97 else letter_ord - 64 + 26


class RuckSack:
    def __init__(self, items: str):
        self.total_num_items = len(items)
        self.num_items_per_pocket = self.total_num_items // 2
        self.all_items_types = set(items)
        self.item_types_in_pocket_1 = set(items[:self.num_items_per_pocket])
        self.item_types_in_pocket_2 = set(items[self.num_items_per_pocket:])

    @property
    def num_items_is_even(self) -> bool:
        return self.total_num_items % 2 == 0

    @property
    def only_one_type_misplaced(self) -> bool:
        return len(self.misplaced_item_types) == 1

    @property
    def misplaced_item_types(self) -> Set[str]:
        return self.item_types_in_pocket_1.intersection(self.item_types_in_pocket_2)

    @property
    def misplaced_items_priority(self) -> Set[int]:
        return {letter_to_priority(type) for type in self.misplaced_item_types}

    def matching_items(self, another_sack: "RuckSack"):
        return set(self.all_items_types).intersection(another_sack.all_items_types)