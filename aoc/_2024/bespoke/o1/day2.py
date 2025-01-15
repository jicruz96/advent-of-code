def solve_part2():
    def is_safe(seq: list[int]) -> bool:
        """
        Checks if a sequence is safe according to the rules:
        - The sequence must be strictly increasing OR strictly decreasing.
        - The absolute difference between adjacent elements must be between 1 and 3 (inclusive).

        Returns True if safe, False otherwise.
        """
        if len(seq) < 2:
            # A sequence of length 0 or 1 is trivially safe.
            return True

        # Determine the trend (increasing or decreasing) from the first non-equal pair
        direction = None  # +1 for increasing, -1 for decreasing
        for i in range(len(seq) - 1):
            diff = seq[i + 1] - seq[i]
            if diff > 0:
                direction = 1
                break
            elif diff < 0:
                direction = -1
                break
        if direction is None:
            # This means all elements are equal, which is not strictly increasing or decreasing
            return False

        # Verify that all differences follow the chosen direction and are within [1, 3]
        for i in range(len(seq) - 1):
            diff = seq[i + 1] - seq[i]
            if direction == 1:
                # Must be strictly increasing: diff > 0
                if diff <= 0 or diff > 3:
                    return False
            else:
                # Must be strictly decreasing: diff < 0
                if diff >= 0 or diff < -3:
                    return False

        return True

    def can_be_safe_with_one_removal(seq: list[int]) -> bool:
        """
        Checks if removing exactly one element from seq can make it safe,
        if it isn't already safe.

        Returns True if removing one element can fix the sequence, False otherwise.
        """
        for i in range(len(seq)):
            new_seq = seq[:i] + seq[i + 1 :]
            if is_safe(new_seq):
                return True
        return False

    safe_count = 0
    with open("data/day2.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            levels = list(map(int, line.split()))

            # Check if already safe
            if is_safe(levels):
                safe_count += 1
            else:
                # Check if one removal can make it safe
                if can_be_safe_with_one_removal(levels):
                    safe_count += 1

    print(safe_count)


if __name__ == "__main__":
    solve_part2()
