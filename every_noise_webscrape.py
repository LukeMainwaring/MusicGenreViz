import requests
from bs4 import BeautifulSoup
import os


def get_cities():

    USA_URL = 'http://everynoise.com/everyplace.cgi?vector=city&scope=United%20States'
    r = requests.get(USA_URL)
    
    soup = BeautifulSoup(r.text, 'html.parser')
    # print(soup.prettify())
    # print(soup.find_all('a'))
    all_cities = [link.get('href') for link in soup.find_all('a') if link.get('href').startswith('?root=')]
    # print(len(all_cities))
    # print(all_cities)

    return all_cities


def get_city_songs(city_url):
    BASE_URL = 'http://everynoise.com/everyplace.cgi'
    CITY_URL = BASE_URL + city_url
    r = requests.get(CITY_URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    # print(soup.prettify())
    # spotify_table = soup.find_all("table",{"class":"d c2 a1"})
    spotify_table_url = soup.find('iframe').get('src')
    # print(spotify_table_url)
    r2 = requests.get(spotify_table_url)
    # print(r2)
    soup2 = BeautifulSoup(r2.text, 'html.parser')
    # print(soup2.prettify())


    artists = soup2.find_all("div", class_="m cd cc a1 aq al ar c6")
    # print(artists)

    return None


def music_recs(artist):
    ''' Search ifyoudig.net for the specified artist. Do some searches yourself
    to see how this works. You only have to support artists that appear here:
    http://ifyoudig.net/autocomplete.php.
    If any other input is given, throw an exception with the message:
    "Artist not found.".

    You should convert the artist name to the specified hyphenated slug, and
    then query the appropriate url. Return a list of the top 10
    recommended artists.

    Note that most of the artist names are links, but some aren't;
    e.g. see http://ifyoudig.net/laura-marling. You should be able to handle
    either case.

    Assume that the artist will have correct capitalization if a valid artist.
    '''
    ALL_ARTISTS = "http://ifyoudig.net/autocomplete.php"
    BASE_URL = "http://ifyoudig.net/"

    # create a dictionary to match all supported artists with hyphenated slug
    d = {}
    r = requests.get(ALL_ARTISTS)
    artists = r.text.split("\n")
    for s in artists:
        artist_split = s.split("|")
        # only add to dictionary if valid match between artist/query parameter
        if len(artist_split) == 2:
            d[artist_split[0]] = artist_split[1]

    if d[artist] is None:
        raise Exception("Artist Not Found")

    url = BASE_URL + d[artist]
    r2 = requests.get(url)
    soup = BeautifulSoup(r2.text, "html.parser")

    l = []
    index = 0
    # all artists listed have a spotify play anchor tag, using this tag allows
    # us to find recommended artists whether or not they have links
    anchor_tag = soup.find_all("a")
    for a in anchor_tag:
        if index > 10:
            break
        if str(a.get("class")) == "['spotify-play']" and index <= 10:
            # first artist is queried artist, so ignore
            if index > 0:
                l.append(str(a.get("data-artist-name")))
            index += 1
    return l


def xkcd(comic_num):
    ''' Pull up the comic_num-th xkcd comic on http://xkcd.com/
        For example: comic_num = 1488 --> http://xkcd.com/1488/
    Return a dictionary with the keys:
        'image_path', 'comic_title', and 'title_text'
    The values should be:
        'image_path' -> a relative file path to a downloaded image of the comic
                    Store the file in a directory called imgs, and do not
                    assume that directory already exists. The os module may be
                    helpful here.
        'comic_title' -> The string that is the title of the comic
        'title_text' -> The string that is the title attribute of the image
    If comic_num is beyond the range of valid comics at the time of the query,
    raise a ValueError with the message:
        '[comic_num] is an invalid xkcd comic.'
    You should raise this error only if the request results in
    a "Not Found" status code (see `requests.codes.not_found`).
    '''
    comic_dict = {}
    url = "http://xkcd.com/" + str(comic_num) + "/"
    r = requests.get(url)

    if str(r.status_code) == "404":
        raise ValueError(str(comic_num) + ' is an invalid xkcd comic.')

    # create image directory if doesn't already exist
    if not os.path.isdir('imgs'):
        os.mkdir('imgs')

    soup = BeautifulSoup(r.text, "html.parser")

    # comic title and title text
    div_tag = soup.find_all("div")
    for d in div_tag:
        if d.get("id") is not None:
            if str(d["id"]) == "ctitle":
                comic_title = d.string
                comic_dict['comic_title'] = comic_title
            elif str(d["id"]) == "transcript":
                transcript = d.string.split("Title text: ")
                title_text = transcript[1].strip("}}")
                comic_dict['title_text'] = title_text

    # image file
    img_tag = soup.find_all("img")
    for img_link in img_tag:
        if str(img_link.get("alt")) == comic_title:
            img_url = img_link.get("src")
            img_url = "http:" + img_url
            img_url_split = img_url.split("/")
            img_name = img_url_split[-1]

            # referenced the website https://www.codementor.io/tips/3443978201
            # /how-to-download-image-using-requests-in-python
            # to learn how to download images from requests
            img_request = requests.get(img_url, stream=True)
            # current working directory is where we call python program, within
            # this directory we add the downloaded images to imgs directory
            path = "imgs/" + img_name
            with open(path, 'wb') as f:
                for chunk in img_request:
                    f.write(chunk)
            path = "~/Desktop/cis192/" + path
            comic_dict['image_path'] = path

    return comic_dict


def main():
    city_urls = get_cities()
    
    test_city_url = city_urls[1]
    get_city_songs(test_city_url)


if __name__ == "__main__":
    main()
