I initially stored the raw HTML in one big sqlite database (`raw.html.db`). But Github has a 100mb file size limit, so i split the thing up manually.

For my reference, these were the commands (one applied to each database file, which was initially the full data):

```
DELETE from data WHERE page > 140 OR page is null
DELETE from data WHERE page < 141 OR page > 280 OR page is null
DELETE from data WHERE page < 281 OR page > 420 OR page is null
DELETE from data WHERE page < 421
```

