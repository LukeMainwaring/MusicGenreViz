import requests
from bs4 import BeautifulSoup
import os
import pandas as pd


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

def map_city_to_genres(artists_genres_file, city_state_artists_file, outfile):

    # create mapping from artist to artist's genres
    artist_to_genres = {}
    artist_to_id = {}
    with open(artists_genres_file, 'r') as f:
        next(f) # skip column titles
        for line in f:
            # map from artist to id
            artist_info = line.split(',')
            spotify_id = artist_info[-1].strip('\n')
            name = artist_info[-2]
            artist_to_id[name] = spotify_id
    
            # map from artist to genres
            # UNNECESSARY for now
            genre_info1 = line.split('[')[1]
            genre_info2 = genre_info1.split(']')[0]
            genre_info2 = genre_info2.replace("'", "")
            genres = genre_info2.split(',')
            genres = [word.lstrip() for word in genres]
            artist_to_genres[name] = genres

    # print(artist_to_genres)
    # print(artist_to_id)

    # create mapping from city to all artist ids
    # city_to_genres = {}
    city_to_artists = {}
    artist_ids_to_city = {}

    state_codes = {v: k for k, v in states.items()}

    with open(city_state_artists_file, 'r') as f:
        next(f)
        for line in f:
            city_info = line.split(',')
            state = city_info[-1].strip('\n')
            if state != 'N/A':
                state = state_codes[state]
            city = city_info[-2]
            # print('city:', city, 'state:', state)
            artists_info = line.split('[')[1].split(']')[0]
            artists_info = artists_info.replace("'", "")
            artists = artists_info.split(',')
            artists = [word.lstrip() for word in artists]
            city_to_artists[(city,state)] = artists
    # print(city_to_artists)

    for city in city_to_artists.keys():
        city_artists = city_to_artists[city]
        # print(city_artists)
        for artist in city_artists:
            if artist in artist_to_id:
                artist_id = artist_to_id[artist]
                if artist_id not in artist_ids_to_city:
                    artist_ids_to_city[artist_id] = [city]
                else:
                    artist_ids_to_city[artist_id].append(city)
                # print(artist_id)
            # if artist_to_genres[artist]:
            #    print()
    # print(artist_ids_to_city)

    # for artist_id in artist_ids_to_city.keys():
        # print(artist_id, ': ', artist_ids_to_city[artist_id])
        # print(artist_id, ': ', list(enumerate(artist_ids_to_city[artist_id])))
    
    # print(artist_ids_to_city)

    # write out results to a file
    with open(outfile, 'w') as f:
        f.write('Artist_ID,City,State\n')
        for artist_id in artist_ids_to_city.keys():
            for city_state in artist_ids_to_city[artist_id]:
                city, state = city_state[0], city_state[1]
                # print(city, state)
                f.write(artist_id + ',' + city + ',' + state + '\n')
            # print(artist_id, ',', artist_ids_to_city[artist_id])
            # artist_mapping = artist_id + ',' + str(artist_ids_to_city[artist_id])
            # f.write(artist_mapping + '\n')
            # print(artist_mapping)


def main():
    # remove_empty_cities("city_artists_file.txt", "city_artists_file2.txt", 
    #    "city_artists_file3.txt", "city_artists_file_cleaned.txt")
    
    # create_city_state_list('city_artists_file_cleaned.txt', 'city_states.txt', 'zip_codes_states.csv')

    # clean_spotify_artists_genres('artists_genres_test.csv', 'artists_genres_cleaned.csv')

    map_city_to_genres("artists_genres_cleaned.csv", "city_artists_file_cleaned.txt", "artists_to_cities.txt")

if __name__ == "__main__":
    main()
