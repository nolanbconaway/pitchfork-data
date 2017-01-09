from bs4 import BeautifulSoup
import datetime, json


def sf(s):
	""" 
		sf = string format. 
		Ascii and lower-ize a string. 
	"""
	return s.encode('ascii', 'ignore').lower()


class Review(object):
	"""
		Class representing reviews
	"""

	def __init__(self, html):
		self.html = html
		self.soup = BeautifulSoup(html, "lxml")

		# process soup for relevant info
		self._set_meta()
		self._set_title()
		self._set_artist()
		self._set_author()
		self._set_score()
		self._set_review_content()
		self._set_genres()
		self._set_record_label()
		self._set_years()
		self._set_pub_datetime()


	def compile(self):
		"""
			Compile data fields into useful rows for sqlite
		"""

		data = dict(
			reviews = dict(),
			artists = [],
			genres = [],
			labels = [],
			years = [],
			content = dict(reviewid = self.reviewid, content = self.review_content),
		)

		#  create rows for the table
		data['reviews'] = dict(
			reviewid = self.reviewid,
			artist = self.artist_str,
			title = self.title,
			url = self.url,
			score = self.score,
			best_new_music = self.best_new_music,
			author = self.author,
			author_type = self.author_type,
			pub_date = str(self.pub_datetime.date()),
			pub_weekday = self.pub_datetime.weekday(),
			pub_day = self.pub_datetime.day,
			pub_month = self.pub_datetime.month,
			pub_year = self.pub_datetime.year,
		)

		for el in self.artist_list:
			data['artists'].append(dict(
				reviewid = self.reviewid,
				artist = el
			))

		if self.genre_list is None:
			data['genres'] = [dict(reviewid = self.reviewid, genre = None)]
		else:
			for el in self.genre_list:
				data['genres'].append(dict(
					reviewid = self.reviewid,
					genre = el
				))

		for el in self.record_labels_list:
			data['labels'].append(dict(
				reviewid = self.reviewid,
				label = el
			))

		for el in self.years_list:
			data['years'].append(dict(
				reviewid = self.reviewid,
				year = el
			))

		self.data = data
		return data
		
	# below are various functions obtaining data from the soup
	def _set_meta(self):
		reviewid = self.soup.find("article")['id']
		self.reviewid = int(reviewid.split('-')[-1])
		url = self.soup.find("script").string
		self.url = json.loads(url)['url']

	def _set_title(self):
		album_title = self.soup.find("h1", { "class" : "review-title" })
		self.title = sf(album_title.get_text())

	def _set_artist(self):
		artist_list = self.soup.find("ul", { "class" : ["artist-links", "artist-list"] })
		self.artist_list = [sf(li.get_text()) for li in  artist_list.findAll('li')]
		self.artist_str = ', '.join(self.artist_list)

	def _set_author(self):
		author = self.soup.find("a", { "class" : "display-name" }).get_text()
		self.author = sf(author)

		self.author_type = self.soup.find("span", { "class" : "title" })
		if self.author_type is not None:
			self.author_type = sf(self.author_type.get_text())

	def _set_score(self):
		score = self.soup.find("span", { "class" : "score" })
		self.score = float(score.contents[0])
		self.best_new_music = self.soup.find("p", { "class" : "bnm-txt" }) is not None

	def _set_review_content(self):
		review_content = self.soup.find("div", { "class" : "review-text" })
		review_content = review_content.findAll('p')
		review_content = [i.get_text() for i in review_content]
		review_content = ''.join(review_content)
		self.review_content = review_content

	def _set_genres(self):
		self.genre_list = self.soup.find("ul", { "class" : "genre-list" })
		if self.genre_list is not None:
			self.genre_list = [sf(li.get_text()) for li in self.genre_list.findAll('li')]
		else:
			self.genre_list = [None]

	def _set_record_label(self):
		record_labels_list = self.soup.find("ul", { "class" : "label-list" })
		self.record_labels_list =  [sf(li.get_text()) for li in record_labels_list.findAll('li')]
		if not self.record_labels_list:
			self.record_labels_list = [None]

	def _set_years(self):
		years_list = self.soup.find("span", { "class" : "year" })
		years_list = sf(years_list.get_text().strip())
		if not years_list: 
			years_list = [None]
		else:
			years_list = [int(y) for y in years_list.split('/')]
		self.years_list = years_list

	def _set_pub_datetime(self):
		dt = self.soup.find("span", { "class" : "pub-date" })['title']
		self.pub_datetime = datetime.datetime.strptime(dt, "%a %b %d %Y %X GMT+0000 (%Z)")


		

