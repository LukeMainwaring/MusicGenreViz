import pandas as pd
import re

year = []
rank = []
name = []

billboard_df = pd.read_csv('billboard_data.csv')

artist_id_df = pd.read_csv('artists_genres_cleaned.csv')

billboard_pattern = re.compile(r'( With )|( X )|( x )|(/)|( with )|( feat. )|(\))|( featuring )|( Featuring )|( \(featuring)|( Feat. )|( \(Featuring)|(, )')
billboard_pattern_with_and = re.compile(r'( With )|( X )|( x )|(/)|( & )|( with )|( feat. )|(\))|( featuring )|( Featuring )|( \(featuring)|( Feat. )|( \(Featuring)|(, )')
bad_strings = [' With ', ' & ', ' X ', ' x ', '/', ' with ', ' feat. ', ')', ' featuring ', ' Featuring ', ' (featuring', ' Feat. ', ' (Featuring', ', ', None]

artist_list = []

for index, row in billboard_df.iterrows():
	artist = row['artist_name']
	if 'Feat' in artist:
		artist_list = [a for a in re.split(billboard_pattern_with_and, artist) if a not in bad_strings]
	else:
		artist_list = [a for a in re.split(billboard_pattern, artist) if a not in bad_strings]
	for a in artist_list:
		name.append(a)
		year.append(row['year'])
		rank.append(row['rank'])

clean_df = pd.DataFrame({'artist_name': name, 'year': year, 'rank': rank})
print('here')
clean_df = pd.merge(clean_df, artist_id_df, left_on='artist_name', right_on='found_name')
print('here')
clean_df.to_csv('clean_billboard.csv')