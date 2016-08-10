# -*- coding: utf-8 -*-
import urllib2, csv, mechanize
from bs4 import BeautifulSoup
import re
import time

# Get the output file ready
output = open('public/_assets/zika.csv', 'w')
writer = csv.writer(output)

# Get the HTML of the main page
br = mechanize.Browser()
br.open('http://www.cdc.gov/zika/geo/united-states.html')
html = br.response().read()


# Transform the HTML into a BeautifulSoup object
soup = BeautifulSoup(html, "html.parser")


# Scraping pregnancy page
output2 = open('public/_assets/zika_total_cases.csv', 'w')
writer2 = csv.writer(output2)

br2 = mechanize.Browser()
br2.open('http://www.cdc.gov/zika/geo/pregwomen-uscases.html')
html2 = br2.response().read()
soup2 = BeautifulSoup(html2, "html.parser")


# Find the main table using both the "align" and "class" attributes
main_table = soup.find('table',
    {'class': ['table', 'table-bordered']
})


#write custom head of the table
head = ['state', 'travel_associated_cases','locally_acquired_cases']
writer.writerow(head)

# Now get the data from each table row
# strip non-breaking whitespace and text in ()

for row in main_table.find_all('tr'):
    data = [re.sub('\\(.+?\\)|\ {2,}|[^a-zA-Z0-9 :]', '', cell.text.encode('utf-8')) for cell in row.find_all('td')]
    clean_data = []
    for i in data:
    	i = i.replace("\xc2\xa0", "")
    	clean_data.append(i)
    writer.writerow(clean_data)


# Writing to second file
#Total numbers
mainText = soup.findAll('div',{'class': 'syndicate'})[1]
us_all = mainText.findAll('li')[5].text.replace(",", "")
us_numbers = [int(s) for s in us_all.split() if s.isdigit()]
total_us = us_numbers[0]

us_territories_all = mainText.findAll('li')[10].text.replace(",", "").replace("*", "")
us_territories_numbers = [int(s) for s in us_territories_all.split() if s.isdigit()]
total_us_territories = us_territories_numbers[0]

head_row = ['Cases','In the 50 states and D.C.', 'In the U.S. territories']
total_row = ['Total', total_us, total_us_territories]
writer2.writerow(head_row)
writer2.writerow(total_row)

#Pregnancy numbers
us_pregnant_cases = soup2.findAll('h4')[1].text
us_territories_pregnant_cases = soup2.findAll('h4')[2].text

pregnancy_row = ['Pregnant women with possible infections', us_pregnant_cases, us_territories_pregnant_cases]
writer2.writerow(pregnancy_row)
