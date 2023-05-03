# Cell scrapes website for space.com headlines and outputs to the headlines.txt file 
import requests
from bs4 import BeautifulSoup
import re
    
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
    with open('Astro-Website/DATA/sources.txt') as s:
        for line in s:
            urls = [elt.strip() for elt in line.split(',')]
            # in alternative, if you need to use the file content as numbers
            # inner_list = [int(elt.strip()) for elt in line.split(',')]
    links = []
    ## Ignores website specific non-headlines
    ignore = ['Subscribe or renew today', 'Most Popular', 'Subscriber Services', 'More Information', 'Society for Science', 'Quick links', 
            'About Nature Portfolio', 'Discover content','Publishing policies', 'Author & Researcher services', 'Libraries & institutions',
            'Advertising & partnerships', 'Career development', 'Regional websites', 'More news','Other news','Medical Xpress','Tech Xplore',
            'Science X','Science X Account']
    f = open('Astro-Website/DATA/headlines.txt', 'w', encoding="utf-8")
    l = open('Astro-Website/DATA/links.txt', 'w', encoding="utf-8")
    site_1(urls,f,l)
    site_2(urls,f,l,ignore)
    site_3(urls,f,l,ignore)
    site_4(urls,f,l,ignore)
    print('Webscraping completed!')

