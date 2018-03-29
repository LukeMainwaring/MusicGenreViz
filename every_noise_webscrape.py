import requests
from bs4 import BeautifulSoup
import os


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
    print(artists)

    return artists


def main():
    city_urls = get_cities()
    
    test_city_url = city_urls[1]
    get_city_songs(test_city_url)


if __name__ == "__main__":
    main()
