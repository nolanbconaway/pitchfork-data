from bs4 import BeautifulSoup
import requests, time



class Scraper(object):
	"""
		Class for interacting with Pitchfork
	"""

	def __init__(self):
		# global params
		self.httpheaders = {
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
			}
		self.reviews_pageroot = "http://pitchfork.com/reviews/albums/"
		self.timeout = 0.5
		self.num_retrys = 20


	def get_review_urls(self, pagenum):
		"""
			Return list of reviews urls from a page number.
			Return false if request fails
		"""
		
		for i in range(self.num_retrys):
			page = requests.get(self.reviews_pageroot, 
				headers = self.httpheaders, 
				params = dict(page = pagenum)
			)
			time.sleep(self.timeout)
			if page.status_code == 200:	break
		
		# return false if request failed
		if page.status_code != 200: 
			print 'Failed page ' + str(pagenum) + '. Error: ' + str(page.status_code)
			return False

		# process reviews
		soup = BeautifulSoup(page.content, "lxml")
		reviews = soup.findAll("div", { "class" : "review" })

		urls = []
		for i in reviews:
			album_link = i.find('a',{'class': 'album-link'}).attrs['href']
			urls.append( "http://pitchfork.com" + album_link)

		return urls


	def get_review_html(self, url):
		"""
			Return review HTML from a given URL
			Return false if request fails
		"""

		for i in range(self.num_retrys):
			page = requests.get(url, headers=self.httpheaders)
			time.sleep(self.timeout)
			if page.status_code == 200:	break

		# return false if request failed
		if page.status_code != 200: 
			print 'Error ' + str(page.status_code) + 'on: ' + url 
			return False

		return page.text
		

