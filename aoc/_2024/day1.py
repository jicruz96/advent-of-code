from aoc.helpers import get_input_text


def part1() -> None:
    text = get_input_text(1)
    # convert text to the right data structure
    left_list: list[int] = []
    right_list: list[int] = []

    for line in text.splitlines():
        left_number_str, right_number_str = line.split()
        left_list.append(int(left_number_str))
        right_list.append(int(right_number_str))

    # now let's sort the lists
    left_list.sort()
    right_list.sort()

    # calculate total distance
    total_distance: int = 0

    for i in range(len(left_list)):
        left_number = left_list[i]
        right_number = right_list[i]
        distance = abs(left_number - right_number)
        total_distance += distance

    print("Total distance is", total_distance)


def part2() -> None:
    text = get_input_text(1, test_input=True)
    # convert text to the right data structure
    left_list: list[int] = []
    right_list: list[int] = []

    for line in text.splitlines():
        left_number_str, right_number_str = line.split()
        left_list.append(int(left_number_str))
        right_list.append(int(right_number_str))

    # we should now the answer to the question:
    # "how many times does x number appear in right_list"?
    number_frequency_dict: dict[int, int] = {}
    for n in right_list:
        if n not in number_frequency_dict:
            number_frequency_dict[n] = 1
        else:
            number_frequency_dict[n] += 1

    # calculate similarity score
    similarity_score: int = 0

    for i in range(len(left_list)):
        n = left_list[i]
        frequency: int = number_frequency_dict.get(n, 0)
        similarity_score += n * frequency

    print("Similarity score is", similarity_score)


if __name__ == "__main__":
    part1()
    part2()
