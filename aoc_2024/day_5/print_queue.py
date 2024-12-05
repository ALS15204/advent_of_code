from typing import List


def is_correct(queue: List[int], rules: List[List[int]]) -> bool:
    return all(is_right_order(queue, rule) for rule in rules)


def is_right_order(queue: List[int], rule: List[int]) -> bool:
    if all(num in queue for num in rule):
        return queue.index(rule[0]) < queue.index(rule[1])
    return True


def get_middle_number(queue: List[int]) -> int:
    return queue[len(queue) // 2]


def fix_order(queue: List[int], rules: List[List[int]]) -> List[int]:
    for rule in rules:
        if not is_right_order(queue, rule):
            index_1, index_2 = queue.index(rule[0]), queue.index(rule[1])
            queue[index_1], queue[index_2] = queue[index_2], queue[index_1]
    return queue if is_correct(queue, rules) else fix_order(queue, rules)


if __name__ == '__main__':
    with open('data/input.dat') as f:
        data = f.read()
        rules, queues = data.split('\n\n')
        rules = [[int(num) for num in rule.split('|')] for rule in rules.split('\n')]
        queues = [[int(num) for num in queue.split(',')] for queue in queues.split('\n') if queue]
        
    correct_queues = [queue for queue in queues if is_correct(queue, rules)]
    print(sum(get_middle_number(queue) for queue in correct_queues))

    incorrect_queues = [queue for queue in queues if not is_correct(queue, rules)]
    fixed_queues = [fix_order(queue, rules) for queue in incorrect_queues]
    print(sum(get_middle_number(queue) for queue in fixed_queues))
