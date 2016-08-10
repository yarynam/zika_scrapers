import urllib2, csv, mechanize
from bs4 import BeautifulSoup
import re


# Start mechanize to scrape links from Web Archive
br = mechanize.Browser()
br.set_handle_robots(False)
br.open('https://web.archive.org/web/*/http://www.cdc.gov/zika/geo/united-states.html')

# Get HTML
html = br.response().read()

# Transform the HTML into a BeautifulSoup object
soup = BeautifulSoup(html, "html.parser")

# Find all days when webpage was captured
captures = soup.find_all('div',
    {'class': 'captures'}
)

#create a list of CDC links
urls = []

# Get link from each day
for i in captures:
    links = i.find_all('a')
    link = links[0]['href']
    correct_link = "https://web.archive.org" + link
    urls.append(correct_link)



# Scrape data from CDC pages
for i in urls:
    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open(i)
    html = br.response().read()

    # Transform the HTML into a BeautifulSoup object
    soup = BeautifulSoup(html, "html.parser")

    mainText = soup.findAll('div',{'class': 'syndicate'})[1]
    date = mainText.findAll('strong')[0].text.replace("As of", "").replace(", 2016","")
    date = re.sub('\\(.+?\\)', '', date).replace(" ", "_")
    print date

    # Find the main table
    main_table = soup.find('table',
        {'class': ['table', 'table-bordered']
    })

    # Get the output file ready
    output = open('data/zika'+ date + '.csv', 'w')
    writer = csv.writer(output)

    travel_cases = 'travel_cases_' + date
    local_cases = 'local_cases_' + date

    #write custom head of the table
    head = ['state', travel_cases, local_cases]
    writer.writerow(head)

    # Get the data from each table row
    for row in main_table.find_all('tr'):
        data = [re.sub('\\(.+?\\)|\ {2,}|[^a-zA-Z0-9 :]', '', cell.text.encode('utf-8')) for cell in row.find_all('td')]
        clean_data = []
        for i in data:
            i = i.replace("\xc2\xa0", "")
            clean_data.append(i)
        writer.writerow(data)
