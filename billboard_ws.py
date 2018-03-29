import billboard
import pandas as pd
import time

chart = billboard.ChartData('hot-100')
year = []
artist_name = []
rank = []

count = 10
while chart.date and count > 0:
	time.sleep(1)
	for song in chart:
		year.append(int(chart.date[:4]))
		artist_name.append(song.artist)
		rank.append(song.rank)
	chart = billboard.ChartData('hot-100', chart.previousDate)
	count = count - 1
	print(count)

df = pd.DataFrame({'year': year, 'artist_name': artist_name, 'rank': rank})
df.to_csv('billboard_data.csv')
print(df)

# make delay 10s, delete count limit