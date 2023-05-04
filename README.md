\subsection*{Main Project Topic: The Robot Astronomer}
\quad For our project, we have decided to build our own AI astronomer which determines the most 
searched objects in a given day and gets the coordinates of said objects through a DSS (Digitized 
Sky Survey) query. The project itself can be navigated through a simple and easily understandable 
website. \\

\subsection*{Program Structure:}
\begin{enumerate}
  \item [$-$] COMPONENTS: All Python scripts
  \item [$-$] DATA: All data files
  \item [$-$] IMAGES: Where all images used for websites and images downloaded from STScI database are stored
  \item [$-$] PAGES: All HTML files
  \item [$-$] SCRIPTS: All javascript files
  \item [$-$] STYLES: All CSS files
  \item [$-$] UNIVERSAL: All common header and footer across all pages
\end{enumerate}

\subsection*{Data Collections and Methods:}
\begin{enumerate}[leftmargin=*]
    \item Stage 1: Collect data from space news sites:  \texttt{website\_scraping.py}:
        \begin{enumerate}
            \item [$-$] Websites: https://www.space.com/science-astronomy, \\
            https://www.sciencenews.org/topic/astronomy, \\ 
            https://www.nature.com/natastron/news-and-comment, \\ 
            https://phys.org/space-news/
            \item [$-$] Write article headlines and links to \texttt{headlines.txt} and \texttt{links.txt}
        \end{enumerate}
    \item Stage 2: Process keywords \texttt{keyword\_processing.py}
        \begin{enumerate}
            \item [$-$] Use nltk for language and POS tagging
            \item [$-$] Find most popular topics \texttt{popular\_topics()}:
            \begin{enumerate}[leftmargin=*]
                \item[$\cdot$] Read \texttt{headlines.txt}
                \item[$\cdot$]Get nouns with nltk
                \item[$\cdot$]Write nouns in a dictionary and track count in headlines.
                \item[$\cdot$]Exclude generic words, websites, org names
                \item[$\cdot$]Get the top 10 words with the highest counts
                \item[$\cdot$]Write these words in \texttt{popular\_topics.txt} and 
                  their occurrences
            \end{enumerate}
        \end{enumerate}
    \item Stage 3: Find object names from popular topics list:
    \texttt{back\_search.py}
        \begin{enumerate}
            \item [$-$] Use genism for summaries and object locating
            \begin{enumerate}[leftmargin=*]
                \item[$\cdot$] Search all headlines for top words
                \item[$\cdot$] Scrape articles from their corresponding links
                \item[$\cdot$] Create 40\% sized summaries of each article 
                \item[$\cdot$] Filter through summaries with a large 
                  list of object names accumulated from multiple databases
                 \item[$\cdot$] Create list of final object names \texttt{list\_objects.txt}
            \end{enumerate}
        \end{enumerate}
    \item Stage 4: Search top topics in databases to find more information 
    about the objects, the coordinates, and populate to HTML: \texttt{popular-object-to-html.py}:
        \begin{enumerate}
            \item [$-$] Reverse search using keywords on websites
            \item [$-$] Get exact objects names
            \item [$-$] Get objects' coordinates from databases, can feed object 
              name to $https://archive.stsci.edu/cgi-bin/dss\_form$, use Astropy
            \item [$-$] Determine if objects are observable, flag, and move to the next object if not observable
            \item [$-$] Use coordinates RA and Dec to get image 
              from $https://archive.stsci.edu/cgi-bin/dss\_form$
            \item [$-$] Save information about objects: coordinates and images and update on HTML files
        \end{enumerate}
    \item Stage 5: Create a user interface (website) that:
    \begin{enumerate}
        \item [$-$] Displays images of the most-searched objects (catalog and originally taken),
        general information about each object (ie. each's location in the sky)
        \item [$-$] Includes a link to GitHub documentation
        \item [$-$] Includes an 'About Us' page, a page about the history of the stellarium telescope, 
          a project 'README' page, and possibly additional informational pages
    \end{enumerate}
\end{enumerate}

\subsection*{How the Program Runs:}

\quad Run \texttt{pip install -r requirements.txt} to install all the necessary packages.\\

\quad Run \texttt{python main.py} daily to execute the whole processes and launch website. \\

\quad This section will describe the steps of how to run the program. We  decided that 
creating a \texttt{main.py} file that can be run each day and runs the files from 
each of the sections described above would be the best option to make this program 
as user-friendly as possible. This file calls functions from each back-end file, 
runs it, and moves on to the next step. We are currently working on creating the 
arguments needed for the command line option but the goal is that our website with 
the day's popular images would automatically open in the user's browser where they 
roam around on the interface.\\

\quad The user interface starts with the title page (\texttt{title-page.html}) which, when 
clicked, transitions into the homepage or most popular object page,
\texttt{object-1-page.html}. Here the user can choose to click between the three most 
popular objects of the day using the center buttons or surf through our information 
pages using the drop across the menu in the top right corner which gives the user access 
to the About Us page, (\texttt{about-us.html}), the Final Paper page
 (\texttt{final-paper-page.html}) and References page (\texttt{ref-site-page.html}). \\

\quad GitHub button in the left bottom corner of our website that brings 
the user straight to the public GitHub repository and documentation. \\

\subsection*{The User Interface:}
\quad The user interface (website) of our project was designed to be easy to navigate 
and informative. It features seven pages, including a title page, three pages for each 
of the most-searched objects, an 'About Us' page, a page that contains this final paper, 
and a references page. Except for the title page, the website has a hamburger menu on 
every page, which makes it easy to navigate to any page from anywhere on the website. 
There is also a link to our Github repository on every page aside from the title page, 
which contains more technical details about our program. \\

\quad When a user first lands on the title page, the program automatically takes them to 
the first most-searched object page upon clicking anywhere on the screen. The first object 
page displays the user's local time, their longitude and latitude, and information about 
whether or not the object is currently visible in their sky, calculated using astropy. This 
is followed by the name of the object, an easily navigable button table that can bring the 
user to each other object page, the name of the object again, its Right Ascension and Declination, 
and an image of it. The same format is repeated for the other two object pages, featuring 
respective information. \\

\quad The reference page is continually updated with a list of all the online articles that 
were read and searched through to inform the AI Astronomer's decision about what the 'most-searched' 
objects of any given day were. This page provides users with a comprehensive list of resources 
used to develop our project, allowing them to explore further on their own. \\

\subsection*{Background:}
\quad The application of Artificial Intelligence (AI) and automation in astronomy has brought 
about revolutionary changes. The advancements in these technologies have led to significant 
improvements in our ability to collect and analyze vast amounts of astronomical data, resulting 
in significant discoveries about the universe. \\

\quad AI and automation have been primarily used in the collection of data in astronomy. With the 
development of advanced telescopes, vast amounts of data can now be captured about the 
universe. However, manual processing and analysis of this data can be time-consuming and 
labor-intensive. AI and automation have made the data collection process more efficient, enabling 
astronomers to gather more data in less time. Additionally, AI and automation have been used to 
identify and select objects of interest for further observation. This is particularly crucial in 
astronomy, where there are billions of stars and other celestial objects to observe. By using AI 
algorithms to analyze the data collected by telescopes, astronomers can quickly identify 
objects that are most likely to yield valuable scientific insights. \\

\quad Auto-selecting stellar objects to observe has become a vital aspect of modern astronomy. The 
use of AI and automation has made this process more efficient by enabling astronomers to identify 
the objects they are interested in quickly. This approach allows them to concentrate their attention 
and resources on the most promising objects. Thus, the main objective of our project was to 
determine the most searched objects that general astronomy websites were discussing.  \\

\subsection*{Project Goals:}
\quad The goal of this project is to automate the process of retrieving popular stellar objects 
from space news websites, analyzing them, and quickly determining the most popular ones to 
observe. We argue that because the popular objects in question are popular amongst
verifiable space news sources, they themselves are promising sources astronomically. 
The project aims to achieve this goal by utilizing advanced techniques in AI and 
automation.\\

\quad The first objective of the project is to develop a web scraping tool that can 
crawl popular space news websites and retrieve articles related to stellar objects. 
The tool will then use natural language processing techniques to identify and extract 
the names of the stellar objects mentioned in the articles.\\

\quad The second objective is to analyze the data collected by the web scraping tool 
to determine the most popular stellar objects among the articles retrieved. This 
will be achieved by using natural language processing to tag keywords mentioned 
in headlines to process the data and identify most mentioned objects in the articles.\\

\quad The third objective is to search for the popular stellar objects identified in 
the second objective within the Space Telescope Science Institute (STScI) database 
using regular expression names. The tool will retrieve the  International 
Celestial Reference System (ICRS) coordinates of the objects, their images, 
and related articles/research papers from the STScI database.\\

\quad The final objective is to present the data retrieved in a user-friendly interface 
that allows astronomers to quickly identify the most popular and promising stellar 
objects to observe. The interface will provide users with a dashboard that displays 
the ICRS coordinates, images, and related articles/research papers of the popular 
stellar objects.\\

\quad Overall, the project aims to streamline the process of identifying and observing 
popular stellar objects by automating the data retrieval and analysis process. 
By achieving these objectives, the project will enable astronomers to make more 
efficient use of their time and resources, and increase the likelihood of making 
groundbreaking discoveries in the field of astronomy.\\

<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">project_title</h3>

  <p align="center">
    project_description
    <br />
    <a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/github_username/repo_name">View Demo</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues">Report Bug</a>
    ·
    <a href="https://github.com/github_username/repo_name/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Here's a blank template to get started: To avoid retyping too much info. Do a search and replace with your text editor for the following: `github_username`, `repo_name`, `twitter_handle`, `linkedin_username`, `email_client`, `email`, `project_title`, `project_description`

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Next][Next.js]][Next-url]
* [![React][React.js]][React-url]
* [![Vue][Vue.js]][Vue-url]
* [![Angular][Angular.io]][Angular-url]
* [![Svelte][Svelte.dev]][Svelte-url]
* [![Laravel][Laravel.com]][Laravel-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/github_username/repo_name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```js
   const API_KEY = 'ENTER YOUR API';
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.

_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3
    - [ ] Nested Feature

See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues).

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

Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - email@email_client.com

Project Link: [https://github.com/github_username/repo_name](https://github.com/github_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []()
* []()
* []()

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/github_username/repo_name.svg?style=for-the-badge
[contributors-url]: https://github.com/github_username/repo_name/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/github_username/repo_name.svg?style=for-the-badge
[forks-url]: https://github.com/github_username/repo_name/network/members
[stars-shield]: https://img.shields.io/github/stars/github_username/repo_name.svg?style=for-the-badge
[stars-url]: https://github.com/github_username/repo_name/stargazers
[issues-shield]: https://img.shields.io/github/issues/github_username/repo_name.svg?style=for-the-badge
[issues-url]: https://github.com/github_username/repo_name/issues
[license-shield]: https://img.shields.io/github/license/github_username/repo_name.svg?style=for-the-badge
[license-url]: https://github.com/github_username/repo_name/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/linkedin_username
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 