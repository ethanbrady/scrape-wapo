# Readme

This is a scraping tool designed for Washington Post's online website. It uses the `requests` and `bs4` (beautiful soup) modules in Python. The script bypasses the subscription wall and can be successfully executed beyond the free article limit.

## Caveats
1. There is some lag time from the request. I suspect this is due to the Post's cookies trying to be set.

2. The website's HTML sometimes differs depending on when the request is made. Author names in particular can appear in a dict or list format. The `parse_authors` function is designed to handle this.

## Future Work
I plan to add the following features as time permits.
1. ETL function to write story data on a regular schedule (e.g. on the hour) and log each top story in a database.
2. Use of `nltk` library functions to process the text of each story and note any market-moving developments.
