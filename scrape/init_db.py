# This file creates the structure of the final database

# ---------- DB SCHEMA ----------
# 
# reviews contains all items that are not possibly in list form.
# 	-- reviewid
# 	-- album title
#   -- Artists (as a string)
#   -- score (float)
#   -- author name
#   -- author type
#   -- best new music (boolean)
# 	-- publication timestamp string
# 	-- publication day of week
# 	-- publication day of month
#   -- publication day of year
#   -- publication month
#   -- publication year
#   -- publication unix timestamp

db_cur.execute("""DROP TABLE IF EXISTS reviews""")
cmd = """ CREATE TABLE reviews (
	reviewid INTEGER,
	title TEXT,
	artist TEXT,
	url TEXT,
	score REAL,
	best_new_music INTEGER,
	author TEXT,
	author_type TEXT,
	pub_date TEXT,
	pub_weekday INTEGER,
	pub_day INTEGER,
	pub_month INTEGER,
	pub_year INTEGER);
"""
db_cur.execute(cmd)

# ----------
# artists contains a reviewid-to-artist mapping
db_cur.execute("""DROP TABLE IF EXISTS artists""")
cmd = """ CREATE TABLE artists (
	reviewid INTEGER, artist TEXT);
"""
db_cur.execute(cmd)

# ----------
# genres contains a reviewid to genre mapping
db_cur.execute("""DROP TABLE IF EXISTS genres""")
cmd = """ CREATE TABLE genres (
	reviewid INTEGER, genre TEXT);
"""
db_cur.execute(cmd)

# ----------
# labels contains a reviewid to label type mapping
db_cur.execute("""DROP TABLE IF EXISTS labels""")
cmd = """ CREATE TABLE labels (
	reviewid INTEGER, label TEXT);
"""
db_cur.execute(cmd)

# ----------
# years contains a reviewid to release year mapping
db_cur.execute("""DROP TABLE IF EXISTS years""")
cmd = """ CREATE TABLE years (
	reviewid INTEGER, year INTEGER);
"""
db_cur.execute(cmd)

# ----------
# content contains a reviewid to content mapping
db_cur.execute("""DROP TABLE IF EXISTS content""")
cmd = """ CREATE TABLE content (
	reviewid INTEGER, content TEXT);
"""
db_cur.execute(cmd)

