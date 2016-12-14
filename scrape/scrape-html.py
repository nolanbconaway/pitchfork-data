import requests, time, sqlite3, os
from bs4 import BeautifulSoup


httpheaders = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
timeout = 0.5

# configure storage
conn = sqlite3.connect("raw.html.db")
cur = conn.cursor()

conn.execute('''DROP TABLE IF EXISTS data;''')
conn.execute('''CREATE TABLE data (page INTEGER, url TEXT, html TEXT);''')


def get_page_reviews(pagenum, httpheaders):
	"""
		Return list of reviews from a page number.
		Return false if page does not exist.
	"""
	params = dict(page = pagenum)
	reviews_pageroot = "http://pitchfork.com/reviews/albums/"
	
	page = requests.get(reviews_pageroot, headers=httpheaders, params = params)

	if page.status_code == 200:
		soup = BeautifulSoup(page.content, "lxml")
		ret = dict(all_good = True, data = soup.findAll("div", { "class" : "review" }))
		return ret
	else:
		ret = dict(all_good = False, data = page)
		return ret


pagenum = 0
while True:
	pagenum += 1

	# get page reviews
	reviews = get_page_reviews(pagenum, httpheaders)
	if not reviews['all_good']: 
		page = reviews['data']
		print str(page.status_code) + ' on page ' + str(pagenum)
		continue

	
	if not reviews['data']:
		print 'Empty reviews on page ' + str(pagenum)
		continue

	# Give pitchfork a break!
	time.sleep(timeout)

	for album in reviews['data']:

		# find url for review
		album_link = album.find('a',{'class': 'album-link'}).attrs['href']
		url = "http://pitchfork.com" + album_link
		page = requests.get(url, headers=httpheaders)

		# check status
		if page.status_code != 200: 
			print str(page.status_code) + ' on ' + url
			continue

		# add to sqlite
		cmd = '''INSERT INTO data (page, url, html) 
				 VALUES (?,?,?);'''
		vals = (pagenum, album_link, page.text)
		cur.execute(cmd, vals)
		conn.commit()

		# Give pitchfork a break!
		time.sleep(timeout)

	print 'Finished page: ' + str(pagenum)


conn.close()



