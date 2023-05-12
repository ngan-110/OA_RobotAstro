<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->


<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#structure">Structure</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#methods">Methods</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Product Name Screen Shot][product-screenshot]

For our project, we have decided to build our own AI astronomer which determines the most searched objects in a given day and gets the coordinates of said objects through a DSS (Digitized Sky Survey) query. The project itself can be navigated through a simple and easily understandable 
website.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites
  ```sh
  pip install -r requirements.txt
  ```

### Installation
1. Clone the repo
   ```sh
   git clone https://github.com/ngan-110/OA_RobotAstro.git
   ```
3. Install packages
   ```sh
   https://github.com/ngan-110/OA_RobotAstro.git
   ```
4. Run
   ```sh
   python main.py
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Structure:
1. COMPONENTS: All Python scripts
2. DATA: All data files
3. IMAGES: Where all images used for websites and images downloaded from STScI database are stored
4. PAGES: All HTML files
5. SCRIPTS: All javascript files
6. STYLES: All CSS files
7. UNIVERSAL: All common header and footer across all pages

<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://github.com/ngan-110/OA_RobotAstro/blob/main/Report.pdf)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Methods:

- [ ] Collect data from space news sites: [website_scrapping.py](https://github.com/ngan-110/OA_RobotAstro/blob/main/Astro-Website/COMPONENTS/website_scrapping.py):
    - Websites: https://www.space.com/science-astronomy, https://www.sciencenews.org/topic/astronomy, https://www.nature.com/natastron/news-and-comment, https://phys.org/space-news/
    - Write article headlines and links to [headlines.txt](https://github.com/ngan-110/OA_RobotAstro/blob/main/Astro-Website/DATA/headlines.txt) and [links.txt](https://github.com/ngan-110/OA_RobotAstro/blob/main/Astro-Website/DATA/links.txt) 
- [ ] Process keywords [keyword_processing.py](https://github.com/ngan-110/OA_RobotAstro/blob/main/Astro-Website/COMPONENTS/keyword_processing.py)
    - Use nltk for language and POS tagging
    - Find most popular topics:
        - Read [headlines.txt](https://github.com/ngan-110/OA_RobotAstro/blob/main/Astro-Website/DATA/links.txt)
        - Get nouns with nltk
        - Write nouns in a dictionary and track count in headlines.
        - Exclude generic words, websites, org names
        - Get the top 10 words with the highest counts
        - Write these words in [popular_topics.txt](https://github.com/ngan-110/OA_RobotAstro/blob/main/Astro-Website/DATA/popular_topics.txt) and their occurrences
- [ ] Find object names from popular topics list:
    [back_search.py](https://github.com/ngan-110/OA_RobotAstro/blob/main/Astro-Website/COMPONENTS/back_search.py)
    - Use genism for summaries and object locating
        - Search all headlines for top words
        - Scrape articles from their corresponding links
        - Create 40\% sized summaries of each article 
        - Filter through summaries with a large list of object names accumulated from multiple databases
        - Create list of final object names [list_objects.txt](https://github.com/ngan-110/OA_RobotAstro/blob/main/Astro-Website/DATA/list_objects.txt)
- [ ] Search top topics in databases to find more information 
    about the objects, the coordinates, and populate to HTML: [popular_object_to_html.py](https://github.com/ngan-110/OA_RobotAstro/blob/main/Astro-Website/COMPONENTS/popular_object_to_html.py):
    - Reverse search using keywords on websites
    - Get exact objects names
    - Get objects' coordinates from databases, can feed object name to https://archive.stsci.edu/cgi-bin/dss_form, use Astropy
    - Determine if objects are observable, flag, and move to the next object if not observable
    - Use coordinates RA and Dec to get image 
              from https://archive.stsci.edu/cgi-bin/dss_form
    - Save information about objects: coordinates and images and update on HTML files
- [ ] Create a user interface (website) that:
    - Displays images of the most-searched objects (catalog and originally taken), general information about each object (ie. each's location in the sky)
    - Includes a link to GitHub documentation
    - Includes an 'About Us' page, a page about the history of the stellarium telescope, a project 'README' page, and possibly additional informational pages

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

[Ngan Bao](https://www.linkedin.com/in/ngan-tkb-nguyen/) - [Alexandra Savino](https://www.linkedin.com/in/alexandra-savino-879146200/) - [Rhessa Weber Langstaff](https://www.linkedin.com/in/rhessa-weber-langstaff/)


Project Link: [https://github.com/ngan-110/OA_RobotAstro](https://github.com/ngan-110/OA_RobotAstro)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[product-screenshot]: Astro-Website/IMAGES/product-screenshot.PNG
