import sqlite3
import pandas as pd

import P4K

# configure storage of scraping events
status_conn = sqlite3.connect("scrape.results.db")
status_cur = status_conn.cursor()
status_conn.execute('''DROP TABLE IF EXISTS pages;''')
status_conn.execute('''CREATE TABLE pages (page INTEGER, success TEXT);''')
status_conn.execute('''DROP TABLE IF EXISTS reviews;''')
status_conn.execute('''CREATE TABLE reviews (page INTEGER, url TEXT, success TEXT);''')

# configure storage of review data
db_conn = sqlite3.connect('../pitchfork.db')
db_cur = db_conn.cursor()
execfile('init_db.py')

# iterate over pages
scraper = P4K.Scraper()
for pagenum in range(1, 1540):

	# open up storage for the page
	page_data = dict(
		reviews = pd.DataFrame(),
		artists = pd.DataFrame(),
		genres = pd.DataFrame(),
		labels = pd.DataFrame(),
		years = pd.DataFrame(),
		content = pd.DataFrame(),
	)

	# get page reviews
	urls = scraper.get_review_urls(pagenum)
	
	# log the event
	cmd = '''INSERT INTO pages (page, success) VALUES (?,?);'''
	vals = (pagenum, len(urls) > 0)
	status_cur.execute(cmd, vals)
	status_conn.commit()

	if not urls: continue

	for url in urls:

		# get review html
		review_html = scraper.get_review_html(url)

		# log event
		cmd = '''INSERT INTO reviews (page, url, success) VALUES (?,?,?);'''
		vals = (pagenum, url, review_html != False)
		status_cur.execute(cmd, vals)
		status_conn.commit()

		if not review_html: continue

		# process the html
		review = P4K.Review(review_html)
		data = review.compile()

		# add fields to page data
		for k, v in data.items():
			# print k, v
			page_data[k] = page_data[k].append(v, ignore_index = True)

	# append page dataframes to sqlite
	for k, v in page_data.items():
		page_data[k].to_sql(k, db_conn, if_exists = 'append', index = False)

	print 'Finished page: ' + str(pagenum)

status_conn.close()
db_conn.close()