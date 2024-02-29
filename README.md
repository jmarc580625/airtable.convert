# airtable.convert

---

Converting airtable into simple format like json or cvs

## Purpose

---

I once needed to scrap the content of an airtable see: [airtable.com](https://www.airtable.com).
Traditional scraping tool were unable to:

- extract the full content of a large table having more rows than what can is displayed on a web page.
- accurately organize the scraped data in accurate tabular way (missing column names, data from one column randomly allocated to other, etc.).

I then decided to develop my own custom tools to dealt with airtable content srcaping.

In this process I found resources (see credits) that help me sorting out two chalenges:

- extracting the airtable data
- parsing the content of an airtable

Airtable content is not organized as straightforward as it is rendered on the web.
To cope with many table design and application use cases, it is structured with two main parts, a dictionary and a table content.
Getting straight organized data (tabular or dictionary) requires to navigate both.

## Syntax

---

airtable.convert.py [-h] [-c] [ [C ... ] [-j] ]  

**positional arguments:**
 C           column names to be converted (default is all columns if no name is given)

**options:**
 -h, --help      show this help message and exit
 -c, --columns   describe all airtable columns 
 -j, --json      convert airtable to cvs format (default is csv) 

## Credits

---

From an original idea in *[scraping data from airtable](https://medium.com/@sivcan/scraping-data-from-airtable-69007294ff26)* blog post describing:

- how to download an airtable
- how to scrape an airtable content
