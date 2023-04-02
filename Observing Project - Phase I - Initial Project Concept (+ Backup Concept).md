### Members: Rhessa Weber Langstaff, Ngan Bao, Alex Savino

### Main project topic, research question or idea:

Robot astronomer — Build your own AI astronomer that gets coordinates of object AND decides what to observe.

#### Data Collections and Methods

- Stage 1: Collect data from space news sites: website\_scraping.ipynb:
    - Use BeautifulSoup for website scraping
    - Websites: https://www.space.com/science-astronomy', 
        'https://www.sciencenews.org/topic/astronomy', 
        'https://www.nature.com/natastron/news-and-comment', 
        'https://phys.org/space-news/
    - Scrape headlines to headlines.txt

- Stage 2: Process keywords keyword\_processing.ipynb
    - Use nltk for language and POS tagging
    - Find most popular topics popular\_topics():
        - Read headlines.txt
        - Get nouns with nltk
        - Write nouns in a dictionary and track count in headlines.
        - Exclude generic words, websites, org names
        - Get top 10 words with highest counts.
        - Write these words in popular\_topics.txt and their occurrences

- Stage 3: Search top topics in databases to find more information about the objects and the coordinates.
    - Reverse search using keywords on websites 
    - Get exact objects
    - Get objects' coordinates from databases, can feed object name to https://archive.stsci.edu/cgi-bin/dss_form, use Astropy, Pystellarium
    - Determine if objects are observable, flag and move to next object if not observable
    - Use coordinates RA and Dec to get image from https://archive.stsci.edu/cgi-bin/dss_form
    - Save brief information about objects, coordinates and photos.

- Stage 5: Create an interface for user.
    - Display image of objects and links to papers/ articles

#### Project Goals:
We want to automate the process of retrieving news from astronomy and space news websites and decide the most popular objects, retrieving the objects' coordinates and display the objects on our webpage.

Future improvements: Get the coordinates and feed it to other programs such as Stellarium to get the objects' data.
    
#### Background:

  
  
