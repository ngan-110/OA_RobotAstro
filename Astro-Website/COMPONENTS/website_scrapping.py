# Cell scrapes website for space.com headlines and outputs to the headlines.txt file 
import requests
from bs4 import BeautifulSoup
import re

SOURCES = 'Astro-Website/DATA/sources.txt'
HEADLINES = 'Astro-Website/DATA/headlines.txt'
LINKS = 'Astro-Website/DATA/links.txt'
ignore = ['Subscribe or renew today', 'Most Popular', 'Subscriber Services', 'More Information', 'Society for Science', 'Quick links', 
            'About Nature Portfolio', 'Discover content','Publishing policies', 'Author & Researcher services', 'Libraries & institutions',
            'Advertising & partnerships', 'Career development', 'Regional websites', 'More news','Other news','Medical Xpress','Tech Xplore',
            'Science X','Science X Account']

#Site 1
def site_1(urls_h3,f,l):
    if urls_h3[0]:
        url = urls_h3[0]
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')
        #print(soup)
        headlines = soup.find('body').find_all('h3')

        for x in headlines:
            current_headline = x.text.strip()
            containers = x.find_parents('div')
            for container in containers:
                for child in container.find_all('a'):
                    if 'href' in child.attrs:
                        value = str(child['href'])
                        break
                else:
                    continue
                break
            if value:
                l.write(str(value))
                l.write('\n')
            f.write(current_headline)
            f.write('\t')
            f.write('\n')

# Site 2
def site_2(urls_h3,f,l,ignore):
    if urls_h3[1]:
        url = urls_h3[1]
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')
        #print(soup)
        headlines = soup.find('body').find_all('h3')

        printed_links = []  # keep track of links that have been printed
        headlines_list = []
        for x in headlines:
            current_headline = x.text.strip()
            if current_headline in ignore:
                continue
            if current_headline in headlines_list:
                continue
            else:
                f.write(current_headline)
                f.write('\t')
                f.write('\n')
            headlines_list.append(current_headline)
            containers = x.find_parents('div')
            for container in containers:
                for child in container.find_all('h3'):
                    value = child.find('a')['href']
                    if value in printed_links:  # skip printing if link has already been printed
                        continue
                    printed_links.append(value)  # add link to printed links set
                    break
                break
        for value in printed_links:
            l.write(str(value))
            l.write('\n')

# Site 3
def site_3(urls_h3,f,l, ignore):
    if urls_h3[2]:
        url = urls_h3[2]
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')
        #print(soup)
        headlines = soup.find('body').find_all('h3')

        printed_links = []  # keep track of links that have been printed
        headlines_list = []
        for x in headlines:
            current_headline = x.text.strip()
            if current_headline in ignore:
                continue
            if current_headline in headlines_list:
                continue
            else:
                f.write(current_headline)
                f.write('\t')
                f.write('\n')
            headlines_list.append(current_headline)
            containers = x.find_parents('div')
            for container in containers:
                for child in container.find_all('h3'):
                    value = child.find('a')['href']
                    if value in printed_links:  # skip printing if link has already been printed
                        continue
                    printed_links.append(value)  # add link to printed links set
                    break
                break
        for value in printed_links:
            l.write('https://www.nature.com'+str(value))
            l.write('\n')

# Site 4
def site_4(urls_h3,f,l, ignore):
    if urls_h3[3]:
        headers ={'User-Agent': 'Chrome/58.0.3029.110 Safari/537.3'}
        url = urls_h3[3]
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')
        #print(soup)
        headlines = soup.find('body').find_all('h3')
        #print(headlines)

        printed_links = []  # keep track of links that have been printed
        headlines_list = []
        for x in headlines:
            current_headline = x.text.strip()
            if current_headline in ignore:
                continue
            if current_headline in headlines_list:
                continue
            else:
                f.write(current_headline)
                f.write('\t')
                f.write('\n')
            headlines_list.append(current_headline)
            containers = x.find_parents('div')
            for container in containers:
                for child in container.find_all('a'):
                    if 'href' in child.attrs:
                        value = str(child['href'])
                        if value in printed_links:  # skip printing if link has already been printed
                            continue
                    printed_links.append(value)  # add link to printed links set
                    break
                break
        for value in printed_links:
            l.write(str(value))
            l.write('\n')

def run_sites():
    with open(SOURCES) as s:
        for line in s:
            urls = [elt.strip() for elt in line.split(',')]
    ## Ignores website specific non-headlines
    f = open(HEADLINES, 'w', encoding="utf-8")
    l = open(LINKS, 'w', encoding="utf-8")
    site_1(urls,f,l)
    print ('Finished scraping source 1', urls[0])
    site_2(urls,f,l,ignore)
    print ('Finished scraping source 2', urls[1])
    site_3(urls,f,l,ignore)
    print ('Finished scraping source 3', urls[2])
    site_4(urls,f,l,ignore)
    print ('Finished scraping source 4', urls[3])
    print ('Headlines and links saved to', HEADLINES, 'and', LINKS)


