import requests
from bs4 import BeautifulSoup
import os
import pandas as pd


def remove_empty_cities(filename1, filename2, filename3, clean_filename):

    with open(clean_filename, 'w') as f1, open(filename1, 'r') as f2, open(filename2, 'r') as f3, open(filename3, 'r') as f4:
            visited = set()
            for line in f2:
                if line.startswith('[]', 0, 2):
                    continue
                else:
                    city_info = line.split(',')
                    city_state = (city_info[-2], city_info[-1])
                    if city_state not in visited:
                        visited.add(city_state)
                        f1.write(line)
            for line in f3:
                if line.startswith('[]', 0, 2):
                    continue
                else:
                    city_info = line.split(',')
                    city_state = (city_info[-2], city_info[-1])
                    if city_state not in visited:
                        visited.add(city_state)
                        f1.write(line)
            for line in f4:
                if line.startswith('[]', 0, 2):
                    continue
                else:
                    city_info = line.split(',')
                    city_state = (city_info[-2], city_info[-1])
                    if city_state not in visited:
                        visited.add(city_state)
                        f1.write(line)

def create_city_state_list(filename, city_state_file, geodata_file):

    states = {
            'AK': 'Alaska',
            'AL': 'Alabama',
            'AR': 'Arkansas',
            'AS': 'American Samoa',
            'AZ': 'Arizona',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DC': 'District of Columbia',
            'DE': 'Delaware',
            'FL': 'Florida',
            'GA': 'Georgia',
            'GU': 'Guam',
            'HI': 'Hawaii',
            'IA': 'Iowa',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'MA': 'Massachusetts',
            'MD': 'Maryland',
            'ME': 'Maine',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MO': 'Missouri',
            'MP': 'Northern Mariana Islands',
            'MS': 'Mississippi',
            'MT': 'Montana',
            'NA': 'National',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'NE': 'Nebraska',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NV': 'Nevada',
            'NY': 'New York',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'PR': 'Puerto Rico',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VA': 'Virginia',
            'VI': 'Virgin Islands',
            'VT': 'Vermont',
            'WA': 'Washington',
            'WI': 'Wisconsin',
            'WV': 'West Virginia',
            'WY': 'Wyoming'
    }

    state_codes = {v: k for k, v in states.items()}
    # print(state_codes)
    city_states = set()
    visited = set()
    
    with open(city_state_file, 'w') as f1, open(filename, 'r') as f2, open(geodata_file, 'r') as f3:
        for line in f2:
            city_info = line.split(',')
            if city_info[-1] != 'State\n' and city_info[-1] != 'N/A\n':
                city_state = city_info[-2] + ',' + state_codes[city_info[-1].strip('\n')]
                city_states.add(city_state)

        for line in f3:
            city_data = line.split(',')
            lat, lon = city_data[1], city_data[2][1:-1]
            city_name, state_name = city_data[3][1:-1], city_data[4][1:-1]
            city_state = city_name + ',' + state_name
            if city_state in city_states and city_state not in visited:
                visited.add(city_state)
                f1.write(city_state + ',' + lat + ',' + lon + '\n')

    

def clean_spotify_artists_genres(filename, clean_filename):
    
    visited = set()

    with open(filename, 'r') as f1, open(clean_filename, 'w') as f2:

        for line in f1:
            artists_data = line.split(',')
            artist_id = artists_data[-1]
            if artists_data[1] == '[]':
                # print(line)
                continue
            else:
                if artist_id not in visited:
                    visited.add(artist_id)
                    # print(line)
                    f2.write(line)
                # print(line)
            # print(artists_data[-1])

def main():
    # remove_empty_cities("city_artists_file.txt", "city_artists_file2.txt", 
    #    "city_artists_file3.txt", "city_artists_file_cleaned.txt")
    
    # create_city_state_list('city_artists_file_cleaned.txt', 'city_states.txt', 'zip_codes_states.csv')

    clean_spotify_artists_genres('artists_genres_test.csv', 'artists_genres_cleaned.csv')

if __name__ == "__main__":
    main()
