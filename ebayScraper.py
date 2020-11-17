#TODO
# Make request to ebay.com
# Collect data from each detail page
# Collect links to detail pages for each listing
# write the data to MongoDB
import csv
import requests
from bs4 import BeautifulSoup as bs
def get_page(url):
    response = requests.get(url)
    
    if not response.ok:
        print('Server responded:', response.status_code)
    else:
        soup = bs(response.text, 'lxml')
    return soup

def get_detail_data(soup):

#title
    try:
        title = soup.find('h1', id='itemTitle').text.replace('\xa0', '')
    except:
        title = ''
    #print(title)

#sold
    try:
        sold = soup.find('span', class_='vi-qtyS-hot-red').find('a').text.strip().split(' ')[0]
    except:
        sold = ''
    #print(sold)
#price
    try:
        price = soup.find_all('span', id='prcIsum')
    except:
        price = ''
    #print(price)
#location
    try:
        location = soup.find('div', id='itemLocation').find('span').text
    except:
        location = ''
    #print(location)

    data = {'title':title,
            'sold':sold,
            'price':price,
            'location':location}
    
    
def get_index_data(soup):
    try:
        links = soup.find_all('a', class_='s-item__link')
    except:
        links = []
    
    urls = [item.get('href') for item in links]
    
    return urls

def write_csv(data, url):
    with open('output.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)

        row = [data['title'], data['sold'], data['price'], data['location'], url]
        writer.writerow(row)
    
def main():
    url = 'https://www.ebay.com.au/sch/i.html?_from=R40&_trksid=p2380057.m570.l1311&_nkw=lego&_sacat=0'
    

    products = get_index_data(get_page(url))

    for link in products:
        data = get_detail_data(get_page(link))
        print(data)
        write_csv(data, link)


if __name__ == '__main__':
    main()

