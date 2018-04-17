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


def main():
    remove_empty_cities("city_artists_file.txt", "city_artists_file2.txt", 
        "city_artists_file3.txt", "city_artists_file_cleaned.txt")


if __name__ == "__main__":
    main()
