import os, sqlite3, datetime
import pandas as pd
from bs4 import BeautifulSoup

def sf(s):
	""" sf = string format. Ascii and lower-ize a string. """
	return s.encode('ascii', 'ignore').lower()


# initialize database
db_destination = '../pitchfork.db'
execfile('init_db.py')

dbfiles = [f for f in os.listdir('raw-html') if ".db" in f]

reviewid = -1
for dbfile in dbfiles:

	# get data
	path = os.path.join('raw-html', dbfile)
	with sqlite3.connect(path) as tmpcon:
		db = pd.read_sql('SELECT * FROM data', tmpcon)
	tmpcon.close()

	# open up storage-- these will later be turned into a dataframe
	artists_rows = []
	content_rows = []
	genres_rows = []
	labels_rows = []
	review_rows = []
	years_rows = []

	for i, row in db.iterrows():
		reviewid += 1
		print '\tprocessing ' +  str(reviewid)
		
		# cook up the soup
		soup =  BeautifulSoup(row.html, "lxml")
		
		# then dig through the soup...

		album_title = soup.find("h1", { "class" : "review-title" })
		album_title = sf(album_title.get_text())

		artist_list = soup.find("ul", { "class" : ["artist-links", "artist-list"] })
		artist_list = [sf(li.get_text()) for li in  artist_list.findAll('li')]

		author = soup.find("a", { "class" : "display-name" }).get_text()
		author_type = soup.find("span", { "class" : "title" })
		if author_type is not None:
			author_type = sf(author_type.get_text())

		best_new_music = soup.find("p", { "class" : "bnm-txt" }) is not None
		# How to determine if review is a reissue?

		content = soup.find("div", { "class" : "article-content" })
		content = sf(content.get_text())

		genre_list = soup.find("ul", { "class" : "genre-list" })
		if genre_list is not None:
			genre_list = [sf(li.get_text()) for li in genre_list.findAll('li')]

		labels_list = soup.find("ul", { "class" : "label-list" })
		labels_list =  [sf(li.get_text()) for li in labels_list.findAll('li')]

		pub_datetime = soup.find("span", { "class" : "pub-date" })['title']
		pub_datetime = datetime.datetime.strptime(pub_datetime, "%a %b %d %Y %X GMT+0000 (%Z)")

		score = soup.find("span", { "class" : "score" })
		score = float(score.contents[0])

		url = "http://pitchfork.com" + row.url

		years_list = soup.find("span", { "class" : "year" })
		years_list = [int(y) for y in years_list.get_text()[3:].split('/')]

		#  create rows for the table
		review_rows.append(dict(
			reviewid = reviewid,
			title = album_title,
			url = url,
			score = score,
			best_new_music = best_new_music,
			author = author,
			author_type = author_type,
			pub_date = str(pub_datetime.date()),
			pub_weekday = pub_datetime.weekday(),
			pub_day = pub_datetime.day,
			pub_month = pub_datetime.month,
			pub_year = pub_datetime.year,
		))

		for el in artist_list:
			artists_rows.append(dict(
				reviewid = reviewid,
				artist = el
			))


		if genre_list is None:
			genres_rows += [dict(reviewid = reviewid, genre = None)]
		else:
			for el in genre_list:
				genres_rows.append(dict(
					reviewid = reviewid,
					genre = el
				))

		for el in labels_list:
			labels_rows.append(dict(
				reviewid = reviewid,
				label = el
			))

		for el in years_list:
			years_rows.append(dict(
				reviewid = reviewid,
				year = el
			))
		
		content_rows.append(dict(
			reviewid = reviewid,
			content = content
		))
	
	# convert data into pandas
	artists_rows = pd.DataFrame(artists_rows)
	content_rows = pd.DataFrame(content_rows)
	genres_rows = pd.DataFrame(genres_rows)
	labels_rows = pd.DataFrame(labels_rows)
	review_rows = pd.DataFrame(review_rows)
	years_rows = pd.DataFrame(years_rows)

	# append pandas to sqlite
	artists_rows.to_sql('artists', dbcon, if_exists = 'append', index = False)
	content_rows.to_sql('content', dbcon, if_exists = 'append', index = False)
	genres_rows.to_sql('genres', dbcon, if_exists = 'append', index = False)
	labels_rows.to_sql('labels', dbcon, if_exists = 'append', index = False)
	review_rows.to_sql('reviews', dbcon, if_exists = 'append', index = False)
	years_rows.to_sql('years', dbcon, if_exists = 'append', index = False)

	print 'Finished: ' + dbfile

dbcon.close()
