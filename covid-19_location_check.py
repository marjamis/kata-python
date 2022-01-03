import hashlib
import requests
import json
import os
from util_modules import formatting

DATA_SET = 'https://data.nsw.gov.au/data/api/3/action/package_show?id=0a52e6c1-bc0b-48af-8b45-d791a6d8e289'
ALREADY_SEEN = f"{os.environ['HOME']}/.covid_locations_already_seen"


def download():
    data_set_json = requests.get(DATA_SET)
    location_data_url = json.loads(data_set_json.text)['result']['resources'][1]['url']
    location_data_json = requests.get(location_data_url)
    return json.loads(location_data_json.text)


def analyse(data):
    show = []
    write_to_file = []
    search = {}

    # For each location returned in the data generate a md5 hash of the data for determining if this location is new or has been seen before
    for location in data['data']['monitor']:
        md5 = hashlib.md5(u",".join(location.values()).encode('utf-8')).hexdigest()
        search[md5] = location

    # Checks if this file exists and if it doesn't it creates it as it's needed later
    if not os.path.exists(ALREADY_SEEN):
        with open(ALREADY_SEEN, 'w'):
            pass

    # For each generated md5 hash check the cache of hashes to determine if it's been seen before
    for md5 in search.keys():
        with open(ALREADY_SEEN, 'r') as seen:
            # If the hash hasn't been seen the data is retained for viewing and stores the hash for later saving
            if seen.read().find(md5) == -1:
                show.append(search[md5])
                write_to_file.append(md5)

    # If there are hashes to be saved to the cache this is done
    if write_to_file:
        with open(ALREADY_SEEN, 'a+') as seen:
            for i in write_to_file:
                seen.write(f'{i}\n')

    print('New sites:')
    # If there are new locations that haven't previously been seen, based on the hash, the list of locations is passed into a table formatter for the CLI to output
    if show:
        print(formatting.list_of_dictionaries_to_table(
                show,
                excluded_headers=['Lon', 'Lat', 'Alert', 'HealthAdviceHTML'],
                sort_key='Suburb'
        ))


if __name__ == '__main__':
    analyse(download())
