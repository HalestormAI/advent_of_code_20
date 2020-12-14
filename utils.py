import pathlib
import sys

import requests


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
    :return: The raw input data as a string

    TODO: This is not super efficient since it loads the whole input into memory. Probably fine for now.
    """

    if not pathlib.Path(cache_file).is_file():
        try:
            with open(cookie_file) as fh:
                raw_cookies = fh.readlines()
                cookies = dict(c.strip().split("=") for c in raw_cookies)
        except FileNotFoundError:
            print("Cookie file doesn't exist, can't pull the data. Either get the cookie, or download your input data"
                  "and store in 'cached_input.txt' in the cwd.")
            sys.exit(1)

        response = requests.get(url, cookies=cookies)
        with open(cache_file, 'w') as fh:
            raw_data = response.text
            fh.write(raw_data)
    else:
        with open(cache_file) as fh:
            raw_data = fh.read()

    return raw_data


def parse_int_data(raw_data):
    return (int(line.strip()) for line in raw_data.split("\n") if line.strip() != "")
