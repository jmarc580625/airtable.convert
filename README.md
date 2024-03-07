# airtable.convert

---

Converting airtable into simple format like json or cvs

## Purpose

---

I once needed to scrap the content of an airtable (see: [airtable.com](https://www.airtable.com)).
Traditional scraping tool were unable to:

- extract the full content of a large table having more rows than what is displayed on a web page.
- accurately organize the scraped data in tabular way (missing column names, data from a column randomly allocated to another, etc.).

I then decided to develop my own custom tools to dealt with airtable content scraping.

In this process I found a blog post (see credits) helping me sorting out two chalenges:

- extracting the airtable data
- parsing the content of an airtable

Airtable content is not organized as straightforward as it is rendered on the web.
To cope with many table design and application use cases, it is structured with two main parts: a dictionary and table content.
Getting straight organized data (tabular or dictionary) requires to navigate both.

## Command syntax

---

```text
usage: airtable-convert.py [-h] [-f FILE] [-x EXCLUDE [EXCLUDE ...] | -i INCLUDE [INCLUDE ...]] [-r RENAME [RENAME ...]] [-o {json,csv}]

convert airtable content

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  airtable file to be processed
  -x EXCLUDE [EXCLUDE ...], --exclude EXCLUDE [EXCLUDE ...]
                        exclude column from extraction
  -i INCLUDE [INCLUDE ...], --include INCLUDE [INCLUDE ...]
                        include column in extraction
  -r RENAME [RENAME ...], --rename RENAME [RENAME ...]
                        rename column during extraction
  -o {json,csv}, --outformat {json,csv}
                        define output format (default: csv)

any include, exclude or rename parameter which did not match an airtable dictionary entry is silently ignored
```

## Credits

---

From an original idea in *[scraping data from airtable](https://medium.com/@sivcan/scraping-data-from-airtable-69007294ff26)* blog post describing:

- how to get airtable content from a airtable rendering web page
- how to scrape an airtable content
