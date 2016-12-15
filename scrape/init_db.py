# This file creates the structure final database

dbcon = sqlite3.connect(db_destination)
dbcur = dbcon.cursor()

# ---------- DB SCHEMA ----------
# 
# reviews contains all items that are not possibly in list form.
# 	-- reviewid
# 	-- album title
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

dbcur.execute("""DROP TABLE IF EXISTS reviews""")
cmd = """ CREATE TABLE reviews (
	reviewid INTEGER,
	title TEXT,
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
dbcur.execute(cmd)

# ----------
# artists contains a reviewid-to-artist mapping
dbcur.execute("""DROP TABLE IF EXISTS artists""")
cmd = """ CREATE TABLE artists (
	reviewid INTEGER, artist TEXT);
"""
dbcur.execute(cmd)

# ----------
# genres contains a reviewid to genre mapping
dbcur.execute("""DROP TABLE IF EXISTS genres""")
cmd = """ CREATE TABLE genres (
	reviewid INTEGER, genre TEXT);
"""
dbcur.execute(cmd)

# ----------
# labels contains a reviewid to label type mapping
dbcur.execute("""DROP TABLE IF EXISTS labels""")
cmd = """ CREATE TABLE labels (
	reviewid INTEGER, label TEXT);
"""
dbcur.execute(cmd)

# ----------
# years contains a reviewid to release year mapping
dbcur.execute("""DROP TABLE IF EXISTS years""")
cmd = """ CREATE TABLE years (
	reviewid INTEGER, year INTEGER);
"""
dbcur.execute(cmd)

# ----------
# content contains a reviewid to content mapping
dbcur.execute("""DROP TABLE IF EXISTS content""")
cmd = """ CREATE TABLE content (
	reviewid INTEGER, content TEXT);
"""
dbcur.execute(cmd)

