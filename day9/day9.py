import itertools
import operator
import pathlib
import sys
from collections import deque

sys.path.append(str(pathlib.Path(__file__).parent.parent))
import utils

INPUT_URL = 'https://adventofcode.com/2020/day/9/input'


class NumberList:
    """
    Runs through a list of numbers. If each new number is the sum of any two in recent history,
    add it to the list (keep a maximum of n items).

    If it is not, print a message and stop.

    Uses memoization to keep track of all the pairs of sums.

    Could be further optimized by removing opposite sum pairs, but this makes removal/addition
    of new numbers trickier (sum LUT deque needs to change max length as a number moves through
    history).
    """

    def __init__(self, data, preamble_length):

        self.length = preamble_length

        self.data_gen = data
        self.numbers = deque(itertools.islice(self.data_gen, self.length), maxlen=self.length)

        self._line_number = 0
        self.sums = deque(maxlen=self.length)

        self.current_max = max(self.numbers)
        self.current_min = min(self.numbers)

        self._initialise_sum_lut()
        self.times_called = 0

    def run(self):
        for n in self.data_gen:
            if not self._is_possible_with_limits(n):
                return n

            if not self._has_sum(n):
                print(f"Although it would be possible, no pair of numbers actually sum to {n}")
                return n

            self._add_number(n)
        return None

    def _initialise_sum_lut(self):
        """
        Initialise the pairwise sum LUT.

        Slice the first `preamble` elements from the data generator.
        Fill a double ended queue with the pairwise sums of all the elements in the slice. Skip
        the diagonal elements.
        """
        for i, m in enumerate(self.numbers):
            line_sums = deque(maxlen=self.length - 1)
            for j, n in enumerate(self.numbers):
                if i == j:
                    continue
                line_sums.append(m + n)
            self.sums.append(line_sums)

    def _add_number(self, n):
        """
        Take a new number, add it to the deque of numbers (the old front of the queue automatically
        gets removed).

        Then calculate the pairwise sums between the new number and all others in the deque and use
        this to append a new set of differences to the sums LUT.

        Finally, go through all the previous numbers' LUT deques and append the sum between each
        one and the new number.

        :param n: The new number
        """
        # Add new row
        self.numbers.append(n)
        self.sums.append(deque(maxlen=self.length - 1))

        for i, m in enumerate(itertools.islice(self.numbers, 0, self.length - 1)):
            self.sums[-1].append(m + n)
            self.sums[i].append(m + n)

        self.current_min = min(self.numbers)
        self.current_max = max(self.numbers)

    def _is_possible_with_limits(self, n):
        """
        Based on the max/min values stored in the numbers list, check if the new number
        is feasible.

        To be feasible, it must be at least 2*min and no more than 2*max.
        :param n: The number to test
        :return: True if the number is feasible, false otherwise
        """

        def _check_against_limit(n, lim, op):
            num_max = 1
            if n == lim * 2:
                num_max = len([c for c in self.numbers if c == lim])

            return op(n, lim * 2) or (n == lim * 2 and num_max < 2)

        if _check_against_limit(n, self.current_max, operator.gt):
            print(f"No pair of numbers can sum to {n} [numbers too small]")
            return False
        if _check_against_limit(n, self.current_min, operator.lt):
            print(f"No pair of numbers can sum to {n} [numbers too large]")
            return False
        return True

    def _has_sum(self, n):
        """
        Check through all of the sums in the LUT and see if it exists.

        :param n:
        :return: True if the sum exists
        """
        for line_sums in self.sums:
            if n in line_sums:
                return True
        return False


class ConsecutiveSum:
    """
    Search for a consecutive sub-array that sums to the invalid value from task 1.

    Slide a window along the data. If the sum of the sub-array goes greater than
    the target, remove the first element of the sub-array, and subtract from the
    total. Repeat until the sum < the target, then start to expand the sub-array
    right again.
    """

    def __init__(self, data, target):
        self.data_gen = data
        self.target = target

        self.sub_array = deque([])
        self.current_sum = 0

    def run(self):
        for d in self.data_gen:
            self.sub_array.append(d)
            self.current_sum += d

            if self.check():
                return self.output()

            while self.current_sum > self.target:
                removed = self.sub_array.popleft()
                self.current_sum -= removed

                if self.check():
                    return self.output()

    def check(self):
        if self.current_sum == self.target:
            return True
        return False

    def output(self):
        min_val = min(self.sub_array)
        max_val = max(self.sub_array)
        total = min_val + max_val
        print(f"Done: {min_val} + {max_val} = {total}")
        return total


def task_1(raw_data, preamble_length):
    data = utils.parse_int_data(raw_data)
    nn = NumberList(data, preamble_length)
    return nn.run()


def task_2(raw_data, target):
    data = utils.parse_int_data(raw_data)
    cs = ConsecutiveSum(data, target)
    return cs.run()


if __name__ == "__main__":
    input_data = utils.load_input_data("cached_input.txt", INPUT_URL, '../session_cookie.txt')
    tgt = task_1(input_data, 25)
    task_2(input_data, tgt)
