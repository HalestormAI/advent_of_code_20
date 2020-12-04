import pathlib
import requests

INPUT_URL = 'https://adventofcode.com/2020/day/1/input'
TARGET = 2020


def load_input_data(cache_file, url, cookie_file):
    """
    Load the input data from a local file (cache_file).

    If the cache file doesn't exist, pull the input data down from the AoC server, using the session cookie created
    on login.

    To retrieve this use Chrome devtools and copy the session cookie into <cookie_file>.

    Note: The cookie file and input cache are gitignored as they're user specific.

    :param cache_file:      The file in which the input data is stored
    :param url:             The URL to the AoC page
    :param cookie_file:     The path to the cookie file (only used if the cache file isn't found
    :return: The input data as a list of ints
    """

    if not pathlib.Path(cache_file).is_file():
        with open(cookie_file) as fh:
            raw_cookies = fh.readlines()
            cookies = dict(c.strip().split("=") for c in raw_cookies)

        response = requests.get(url, cookies=cookies)
        with open(cache_file, 'w') as fh:
            raw_data = response.text
            fh.write(raw_data)
    else:
        with open(cache_file) as fh:
            raw_data = fh.read()

    return [int(r.strip()) for r in raw_data.split("\n") if r.strip() != ""]


def find_2020_sum(data):
    """
    Sort the data from largest to smallest.

    Iterate through the data. Take the biggest untested number. Then work backwards from the smallest number to find
    the right value. If the total exceeds the target (2020), then we know for sure that there is no small number in the\
    list capable of summing with the big number to reach 2020.

    :param data: List of integer inputs
    :return: The two values that sum to 2020.
    """
    data = sorted(data, reverse=True)

    for idx, item in enumerate(data):
        test_idx = range(len(data) - 1, idx + 1, -1)
        for rev_idx in test_idx:
            reverse_item = data[rev_idx]
            if item + reverse_item > TARGET:
                break

            if item + reverse_item == TARGET:
                return item, reverse_item


if __name__ == "__main__":
    input_data = load_input_data("cached_input.txt", INPUT_URL, 'session_cookie.txt')
    big, small = find_2020_sum(input_data)
    print(f"Found it: {big} + {small} = {TARGET}")
    print(f"Product:  {big} * {small} = {big * small}")
