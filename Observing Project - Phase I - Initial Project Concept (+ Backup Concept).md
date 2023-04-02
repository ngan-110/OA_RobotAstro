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

- Stage 3: Search top topics in databases to find more information about the objects and the coordinates: object\_retrieve.ipynb.
    - Reverse search using keywords on websites 
    - Get exact objects
    - Get objects' coordinates from databases, can feed object name to https://archive.stsci.edu/cgi-bin/dss_form, use Astropy
    - Determine if objects are observable, flag and move to next object if not observable
    - Use coordinates RA and Dec to get image from https://archive.stsci.edu/cgi-bin/dss_form
    - Save brief information about objects, coordinates and photos.

- Stage 5: Create an interface for user.
    - Display image of objects and links to papers/ articles

#### Project Goals:
The goal of this project is to automate the process of retrieving popular stellar objects from space news websites, analyzing them, and quickly determining the most popular ones to observe. The project aims to achieve this goal by utilizing advanced techniques in AI and automation.

The first objective of the project is to develop a web scraping tool that can crawl popular space news websites and retrieve articles related to stellar objects. The tool will then use natural language processing techniques to identify and extract the names of the stellar objects mentioned in the articles.

The second objective is to analyze the data collected by the web scraping tool to determine the most popular stellar objects among the articles retrieved. This will be achieved by using natural language processing to tag keywords mentioned in headlines to process the data and identify most mentioned objects in the articles.

The third objective is to search for the popular stellar objects identified in the second objective within the Space Telescope Science Institute (STScI) database using regular expression names. The tool will retrieve the  International Celestial Reference System (ICRS) coordinates of the objects, their images, and related articles/research papers from the STScI database.

The final objective is to present the data retrieved in a user-friendly interface that allows astronomers to quickly identify the most popular and promising stellar objects to observe. The interface will provide users with a dashboard that displays the ICRS coordinates, images, and related articles/research papers of the popular stellar objects.

Overall, the project aims to streamline the process of identifying and observing popular stellar objects by automating the data retrieval and analysis process. By achieving these objectives, the project will enable astronomers to make more efficient use of their time and resources, and increase the likelihood of making groundbreaking discoveries in the field of astronomy.
    
#### Background:
The field of astronomy has been revolutionized by advances in Artificial Intelligence (AI) and automation. These technologies have greatly improved our ability to collect and analyze vast amounts of astronomical data, and have enabled us to make significant discoveries about the universe.

One of the primary applications of AI and automation in astronomy is in the collection of data. With the development of advanced telescopes and sensors, astronomers can now capture vast amounts of data about the universe. However, processing and analyzing this data manually can be a time-consuming and labor-intensive process. AI and automation have therefore been used to streamline the data collection process, allowing astronomers to gather more data in less time. In addition to collecting data, AI and automation have also been used to identify and select objects of interest for further observation. This is particularly important in astronomy, where there are billions of stars and other celestial objects to observe. By using AI algorithms to analyze the data collected by telescopes and sensors, astronomers can quickly identify objects that are most likely to yield valuable scientific insights.

Auto-selecting stellar objects to observe has become an important aspect of modern astronomy. AI and automation have made this process more efficient by enabling astronomers to quickly identify objects that they are interested in, allowing them to focus their attention and resources on the most promising objects.
  
