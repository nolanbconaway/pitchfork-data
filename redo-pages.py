import requests, time, sqlite3
from bs4 import BeautifulSoup
httpheaders = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

# configure storage
conn = sqlite3.connect("raw.html.db")
cur = conn.cursor()


# enmtire pages to redo
pages = [149,202,203,204,360,361,362,411,412,413,414,415]


# -------- REDO SPECIFIC REVIEWS!!!
reviews = [
"http://pitchfork.com/reviews/albums/22490-home-ost/",
"http://pitchfork.com/reviews/albums/22411-outer/",
"http://pitchfork.com/reviews/albums/22410-there-is-no-right-time/",
"http://pitchfork.com/reviews/albums/22488-ruminations/",
"http://pitchfork.com/reviews/albums/21444-palana/",
"http://pitchfork.com/reviews/albums/21497-wait-see-ep/",
"http://pitchfork.com/reviews/albums/21441-jet-plane-and-oxbow/",
"http://pitchfork.com/reviews/albums/21814-delusions-of-grand-fur/",
"http://pitchfork.com/reviews/albums/21694-lost-themes-ii/",
"http://pitchfork.com/reviews/albums/21840-rosecrans/",
"http://pitchfork.com/reviews/albums/22121-drankin-drivin/",
"http://pitchfork.com/reviews/albums/22158-four-meditations-sound-geometries/",
"http://pitchfork.com/reviews/albums/22135-no-hard-feelings/",
"http://pitchfork.com/reviews/albums/21066-five-years-1969-1973/",
"http://pitchfork.com/reviews/albums/21094-90059/",
"http://pitchfork.com/reviews/albums/20975-the-light-in-you/",
"http://pitchfork.com/reviews/albums/21043-fetty-wap/",
"http://pitchfork.com/reviews/albums/21107-a-curious-tale-of-trials-persons/",
"http://pitchfork.com/reviews/albums/21077-collapse/",
"http://pitchfork.com/reviews/albums/20950-rub/",
"http://pitchfork.com/reviews/albums/20719-summertime-06/",
"http://pitchfork.com/reviews/albums/20733-london-oconnor-o/",
"http://pitchfork.com/reviews/albums/20760-the-beyond-where-the-giants-roam/",
"http://pitchfork.com/reviews/albums/20690-808s-and-dark-grapes-iii/",
"http://pitchfork.com/reviews/albums/20484-bully-feels-like/",
"http://pitchfork.com/reviews/albums/20376-gonzales-chambers/",
"http://pitchfork.com/reviews/albums/20029-big-krit-cadillactica/",
"http://pitchfork.com/reviews/albums/20022-at-the-gates-at-war-with-reality/",
"http://pitchfork.com/reviews/albums/19972-merzbow-full-of-hell-full-of-hell-merzbow/",
"http://pitchfork.com/reviews/albums/20017-yo-la-tengo-extra-painful/",
"http://pitchfork.com/reviews/albums/19995-trash-kit-confidence/",
"http://pitchfork.com/reviews/albums/19678-black-rain-dark-pool/",
"http://pitchfork.com/reviews/albums/19596-the-rentals-lost-in-alphaville/",
"http://pitchfork.com/reviews/albums/19585-the-gaslight-anthem-get-hurt/",
"http://pitchfork.com/reviews/albums/19648-coachwhips-get-yer-body-next-ta-mine/",
"http://pitchfork.com/reviews/albums/19531-tashi-dorji-tashi-dorji/",
"http://pitchfork.com/reviews/albums/19298-trans-am-volume-x/",
"http://pitchfork.com/reviews/albums/19335-the-pains-of-being-pure-at-heart-days-of-abandon/",
"http://pitchfork.com/reviews/albums/19030-hands-the-soul-is-quick/",
"http://pitchfork.com/reviews/albums/18996-lydia-loveless-somewhere-else/",
"http://pitchfork.com/reviews/albums/19028-neil-finn-dizzy-heights/",
"http://pitchfork.com/reviews/albums/18994-cheetahs-cheatahs/",
"http://pitchfork.com/reviews/albums/18938-band-of-horses-acoustic-at-the-ryman/",
"http://pitchfork.com/reviews/albums/19022-brigitte-fontaine-estfolle-comme-a-la-radio/",
"http://pitchfork.com/reviews/albums/19014-isaiah-rashad-cilvia/",
"http://pitchfork.com/reviews/albums/18986-nina-persson-animal-heart/",
"http://pitchfork.com/reviews/albums/18857-helms-alee-sleepwalking-sailors/",
"http://pitchfork.com/reviews/albums/18669-mutual-benefit-loves-crushing-diamond/",
"http://pitchfork.com/reviews/albums/18549-castevet-obsian/",
"http://pitchfork.com/reviews/albums/18621-special-request-soul-music/",
"http://pitchfork.com/reviews/albums/18629-doomriders-grand-blood/",
"http://pitchfork.com/reviews/albums/18343-clap-your-hands-say-yeah-little-moments-ep/",
"http://pitchfork.com/reviews/albums/17960-the-album-leaf-sun-kil-moon-perils-from-the-sea/",
"http://pitchfork.com/reviews/albums/17929-hessian-manegarmr/",
"http://pitchfork.com/reviews/albums/17992-pretty-nice-golden-rules-for-golden-people/",
"http://pitchfork.com/reviews/albums/17903-iggy-and-the-stooges-ready-to-die/",
"http://pitchfork.com/reviews/albums/17554-a-wonder-working-stone/",
"http://pitchfork.com/reviews/albums/17532-lost-sirens/",
"http://pitchfork.com/reviews/albums/17548-la-costa-perdida/",
"http://pitchfork.com/reviews/albums/16842-gentle-stream/",
"http://pitchfork.com/reviews/albums/16802-meat-mountain-ep/",
"http://pitchfork.com/reviews/albums/16751-mostly-no/",
"http://pitchfork.com/reviews/albums/16841-dreamin-wild/",
"http://pitchfork.com/reviews/albums/16823-staycations/",
"http://pitchfork.com/reviews/albums/16766-frigid-stars-barely-real-ep-the-white-birch/",
"http://pitchfork.com/reviews/albums/16718-pop-etc/",
"http://pitchfork.com/reviews/albums/16528-brendan-benson/",
"http://pitchfork.com/reviews/albums/16526-candy-salad/",
"http://pitchfork.com/reviews/albums/16529-the-dandy-warhols/",
"http://pitchfork.com/reviews/albums/16235-remixes-936-remixed-ep/",
"http://pitchfork.com/reviews/albums/16226-la-grande/",
"http://pitchfork.com/reviews/albums/16219-vacation/",
"http://pitchfork.com/reviews/albums/16224-be-strong/",
"http://pitchfork.com/reviews/albums/16220-patience-after-sebald/",
"http://pitchfork.com/reviews/albums/16218-ui/",
"http://pitchfork.com/reviews/albums/16200-wilson-semiconductors/",
"http://pitchfork.com/reviews/albums/15990-17th-street/",
"http://pitchfork.com/reviews/albums/15982-neon-dreams/",
"http://pitchfork.com/reviews/albums/15970-a-very-she-him-christmas/",
"http://pitchfork.com/reviews/albums/15981-preserved/",
"http://pitchfork.com/reviews/albums/15984-psychic-ills/",
"http://pitchfork.com/reviews/albums/15968-schlungs/",
"http://pitchfork.com/reviews/albums/15971-we-stay-together/",
"http://pitchfork.com/reviews/albums/15977-dreamchasers/",
"http://pitchfork.com/reviews/albums/15965-divine-providence/",


]

for url in reviews:
	album_link = url.split('.com/')[1]
	page = requests.get(url, headers=httpheaders)

	# check status
	if page.status_code != 200: 
		print str(page.status_code) + ' on ' + url
		continue

	# add to sqlite
	cmd = '''INSERT INTO data (page, url, html) 
			 VALUES (?,?,?);'''
	vals = (None, album_link, page.text)
	cur.execute(cmd, vals)
	conn.commit()




# -------- REDO ENTIRE PAGES!!!
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

for pagenum in pages:

	# get page reviews
	reviews = get_page_reviews(pagenum, httpheaders)
	if not reviews['all_good']: 
		page = reviews['data']
		print str(page.status_code) + ' on page ' + str(pagenum)
		continue

	
	if not reviews['data']:
		print 'Empty reviews on page ' + str(pagenum)
		continue


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
	print 'Finished page: ' + str(pagenum)


conn.close()