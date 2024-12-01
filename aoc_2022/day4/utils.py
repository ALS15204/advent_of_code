
RANGE_SEPARATOR = "-"


class CleanRange:
    def __init__(self, range_str: str):
        self.start, self.end = list(map(int, range_str.split(RANGE_SEPARATOR)))
        self.coverage = set(range(self.start, self.end + 1))

    def contains(self, another_range: "CleanRange"):
        return another_range.coverage.issubset(self.coverage)

    def is_subset(self, another_range: "CleanRange"):
        return self.coverage.issubset(another_range.coverage)

    def overlap(self, another_range: "CleanRange"):
        return self.coverage.intersection(another_range.coverage)