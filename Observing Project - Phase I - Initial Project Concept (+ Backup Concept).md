

### Members: Rhessa Weber Langstaff, Ngan Bao, Alex Savino

### Main project topic, research question or idea:

Robot astronomer — Build your own AI astronomer that controls a telescope AND decides what to observe.

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
        - Exclude generic words: 'A', 'world', 'scientist', 'scientists', 'sky', 'space', 'science', 'bookshelf', '’', 'nature', 'ideas', 'doesn', 't', 'bodies'
        - Get top 10 words with highest counts.
        - Write these words in popular\_topics.txt and their occurrences
- Stage 3: Search top topics in databases to find more information about the objects and the coordinates.
    - Reverse search using keywords on websites 
    - Get exact object
    - Get objects' coordinates from databases
    - Save brief information about objects, coordinates and photos

- Stage 4: Create an interface for user.
    - Display image of objects and links to papers/ articles

#### Project Goals:
    
#### Background

  
  
