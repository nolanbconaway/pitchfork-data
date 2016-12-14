I initially stored the raw HTML in one big sqlite database (`raw.html.db`). But Github has a 100mb file size limit, so i split the thing up manually into chunks less than 50mb.

For my reference, these were the commands (one applied to each database file, which was initially the full data):

```
DELETE from data WHERE page > 50 OR page is null
DELETE from data WHERE page < 101 OR page > 150 OR page is null
DELETE from data WHERE page < 151 OR page > 200 OR page is null
DELETE from data WHERE page < 201 OR page > 250 OR page is null
DELETE from data WHERE page < 251 OR page > 300 OR page is null
DELETE from data WHERE page < 301 OR page > 350 OR page is null
DELETE from data WHERE page < 351 OR page > 400 OR page is null
DELETE from data WHERE page < 401 OR page > 450 OR page is null
DELETE from data WHERE page < 451 OR page > 500 OR page is null
DELETE from data WHERE page < 501
```

