import os
import requests
import pandas as pd
from requests_html import HTML

def url_to_txt(url, filename="web.html", save=False):
    r = requests.get(url)
    if r.status_code == 200:
        html_text = r.text
        if save:
            with open(filename, 'w') as f:
                f.write(html_text)
        return html_text
    return None
url="https://websites.co.in/sitemap"
def parse_and_extract(url):
    html_text = url_to_txt(url)
    r_html = HTML(html=html_text)
    table_class = ".table"
    r_table = r_html.find(table_class)
    print(r_table)
    table_data=[]
    header_names=[]
    if len(r_table)==1:
        print(r_table[0].text)
        parsed_table=r_table[0]
        rows=parsed_table.find("tr")
        header_row=rows[0]
        header_cols=header_row.find("th")
        header_names = [x.text for x in header_cols]
        for row in rows[1:]:
            cols=row.find("td")
            row_data=[]
            for i, col in enumerate(cols):
                row_data.append(col.text)
            table_data.append(row_data)
        df = pd.DataFrame(table_data, columns=header_names)
        df.to_csv('web_scraper.csv', index=False)
parse_and_extract(url)


#creating a database
import sqlite3
import csv

conn = sqlite3.connect('webscraper.sqlite')
cur=conn.cursor()

cur.execute('DROP TABLE IF EXISTS webscraper')
cur.execute('''
CREATE TABLE "webscraper"(
    "Business_Name" TEXT,
    "Category" TEXT,
    "City" TEXT
)
''')

with open('web_scraper.csv','r',encoding="utf8") as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)
    for row in csv_reader:
        print(row)
        Business_Name=row[0]
        Category=row[1]
        City=row[2]
        cur.execute(''' INSERT INTO webscraper(Business_Name,Category,City)
            VALUES(?,?,?)''',(Business_Name,Category,City))
        conn.commit()
