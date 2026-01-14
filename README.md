# Japan Online Store Search Watchlist

#### Video Demo (Submission for Harvard CS50x: Introduction to Computer Science): <https://youtu.be/lTiz-ha-avc>

## What is this project?

As an avid buyer of items from Japan, I constantly juggle between the online stores when searching for what I want. This project combines listings from Yahoo Auctions Japan and Mercari Japan into a single page. It also has the ability to store searched keywords and apply multiple search conditions for synchronous store searching.

## Getting Started

### Prerequisites

Install the necessary packages for the program to work.

  ```sh
  pip install -r requirements.txt
  ```

### Usage

Locate the root directory of the folder and launch **manage.py**. Click the IP link of the development server.

  ```sh
  python manage.py runserver
  ```

# Mini Documentation

## User View

The premise of the interface is for all content to load on a single page, from top to bottom:

- **Item keyword input** – This input bar allows the user to type in the name of the item they want to search for. The text is automatically stored in the _saved keywords_ section. Saving a keyword without initiating a search is also possible through the save button at the end of the search bar.

- **Parameters and conditions** – A section of the search interface where multiple search conditions can be toggled, including item category, condition (new or used), and sorting options such as recency, price, or relevance.

- **Store selection** – Allows the user to choose which stores to search from. The search can be conducted on a single store or multiple websites simultaneously.

- **Saved keywords list** – A list of keywords saved by the user. Each clickable item will automatically fill the search bar.

- **Results grid** – Listings appear in a grid below the search section. Each tile displays the item image, name, price, and time remaining if it is an auction listing. Clicking the image redirects the user to the item’s original webpage.

- **Page selector** – The user can browse additional listings by clicking the page buttons. Navigation is possible from the first page to the last available page, reloading the site with new listings. Jumping to a specific page number is also supported by entering a number in the input field.

## Frontend and Backend

The [Django](https://www.djangoproject.com/) framework for [Python](https://www.python.org/) was chosen for this project, as it provides most of the necessary tools to host the website. Web scraping is the core method for gathering content from Yahoo Auctions Japan, since its public API was discontinued years ago. [BeautifulSoup](https://beautiful-soup-4.readthedocs.io/en/latest/) is used to scrape HTML results after an HTTP request is made. For Mercari, [Mercapi](https://take-kun.github.io/mercapi/) is used to gather listing data directly from their system.

### Backend

Since Django provides the necessary prerequisites to set up a dynamic website, only a few files need to be modified to implement the system.

- **home.html** – The placeholders for elements used to send data to the backend and reflect results on the site are handled through Django’s proprietary templating system. JavaScript is only used for keyword autofilling and saving, with saved keywords stored using Django’s model layer in _models.py_.

- **views.py** – This file processes HTTP requests from the HTML and returns web responses. When the search button is initiated, the encoded keyword and selected search conditions are retrieved through a GET request and bundled into parameters. These parameters are passed to a combination of functions located in different files. A list is initialized to store item results, which is populated after data is scraped from the web or retrieved via the API. If the user chooses to sort listings by price, this is executed at the end using a lambda function. All data is assigned to a dictionary and sent back to the template using Django’s render function.

- **scrapers.py** – This library is responsible for gathering listing data from the selected store websites. Search parameters requested by the user are passed to the search.py system, which interprets them into a URL for BeautifulSoup (Yahoo Auctions) or a dictionary for the Mercapi API (Mercari). Yahoo Auctions occasionally returns incomplete pages, so a loop is used to retry HTTP requests until a fully loaded page is retrieved. BeautifulSoup requires a user agent to simulate a real browser and avoid detection as a bot. The raw HTML is transformed into a parse tree, from which specific tags, classes, and IDs are extracted and normalized into a unified dictionary format. Mercari searches are relatively simpler, as parameters are directly interpreted by the API. Results from both stores are mapped to common field names (such as item name and price) to ensure a consistent format when rendered on the site.

- **search.py** – A utility library for translating search parameters into a Yahoo Auctions search URL or a Mercapi-compatible dictionary. The functions in this file are used by scrapers.py. For Yahoo Auctions, parameters from views.py are passed to a function that constructs the appropriate URL by breaking down and mapping each search condition. For Mercari, search parameters are translated into values that the Mercapi API can interpret.
