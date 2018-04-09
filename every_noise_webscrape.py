import requests
from bs4 import BeautifulSoup
import os
import pandas as pd


def get_cities():

    USA_URL = 'http://everynoise.com/everyplace.cgi?vector=city&scope=United%20States'
    r = requests.get(USA_URL)
    
    soup = BeautifulSoup(r.text, 'html.parser')
    all_cities = [link.get('href') for link in soup.find_all('a') if link.get('href').startswith('?root=')]

    return all_cities


def get_city_songs(city_url):
    
    BASE_URL = 'http://everynoise.com/everyplace.cgi'
    CITY_URL = BASE_URL + city_url
    r = requests.get(CITY_URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    spotify_table_url = soup.find('iframe').get('src')
    r2 = requests.get(spotify_table_url)
    soup2 = BeautifulSoup(r2.text, 'html.parser')

    artists = [artist_div.text for artist_div in soup2.find_all("div", class_="track-artist")]
    # print(artists)

    return artists


def main():
    city_urls = get_cities()
    city_urls = city_urls[1:]
    # remove duplicate city names
    # del city_urls[35, 6, 4]
    del city_urls[35]
    del city_urls[6]
    del city_urls[4]
    # city_urls_test = city_urls[:5]
    city_state_to_artists = {}
    # for city_url in city_urls_test:
    for city_url in city_urls:
        city_name = city_url.split('=')[1].split('&')[0][:-2].split('%20')
        city_name = ' '.join(city_name).rstrip()
        # print(city_name)
        city_state_to_artists[city_name] = get_city_songs(city_url)


    # separate city_state to city and state
    states = {'Alabama', 'Alaska', 'Arizona', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida','Georgia', 'Hawaii', 'Idaho', 'Illinois', 
    'Indiana', 'Iowa', 'Kentucky', 'Kansas', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 
    'Mississippi', 'Missouri', 'Nebraska', 'Nevada', 'New Jersey' ,'New Mexico', 'New York', 'North Carolina', 'Ohio', 
    'Oklahoma', 'Oregon', 'Pennsylvania', 'Puerto Rico','Rhode Island', 'South Carolina', 'Tennessee', 'Texas', 'Utah', 'Virginia', 'Washington', 'Wisconsin', 'Wyoming'}

    city_to_state = {}
    for city_state in city_state_to_artists.keys():
        city_info = city_state.split(' ')
        # state with two words
        if len(city_info) > 1 and city_info[-2] + ' ' +  city_info[-1] in states:
            state = city_info[-2] + ' ' +  city_info[-1]
            city = ' '.join(city_info[:-2])
            city_to_state[city] = state
        # state with one word
        elif city_info[-1] in states:
            city = ' '.join(city_info[:-1])
            city_to_state[city] = city_info[-1]
        else:
            city = ' '.join(city_info)
            city_to_state[city] = 'N/A'     


    # convert to pandas dataframe
    rows_list = []
    for city in city_to_state:
        for city_state in city_state_to_artists.keys():
            if city_state.startswith(city):
                d = {'City': city, 'State': city_to_state[city], 'Artists': city_state_to_artists[city_state]}
                rows_list.append(d)

    df = pd.DataFrame(rows_list)
    print(df)
    df.to_csv("city_artists_file3.txt", index=False)


if __name__ == "__main__":
    main()
