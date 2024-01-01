#Arknights Gamepress Web Scrapper

This is just a basic learning project to familiarize myself with Python and web scraping.

## Table of Contents

- [Project Description](#project-description)
- [Installation](#installation)
- [Technologies Used](#Technologies-Used)

## Project Description
### Overview:
This Python script automates collecting specific data elements from a target website. This script uses MongoDB to store the information.

### Purpose:
The goal is to learn core web scraping/crawling skills using Python libraries like BeautifulSoup and Requests.

### Functionality:
The script takes a starting URL as input. It crawls the site recursively by following links, identifies key data fields using CSS/XPath selectors, and downloads/processes each page. 

**Disclamer**: 
This is for educational and demonstrative purposes. I have no affiliation with the site and neither 
Neither I nor the software would be held liable for any consequences of its use.

## Installation

If you would like to use this script, please follow these steps.

1. Clone the repository:

     ```bash
     git clone https://github.com/Nathan-Dinh/arknights-web-scrapper.git
     ```

2. Install the needed packages 

     ```shell
     pip install beautifulsoup4
     ```

     ```shell
     pip install requests
     ```

     ```shell
     pip install pymongo
     ```

3. Connect your Mongodb database to your application by adding your connection string to the .env file

     ```dotenv
     MONGODB_CONNECTION_STRING = "<Add your string here>"
     DATABASE_NAME = "Arknights"
     OPERATORS_COLLECTION = "Operators"
     SKINS_COLLECTION = "Skins"

     DOMAIN_NAME = "https://gamepress.gg"
     OPERATOR_LIST_URL = "/arknights/tools/interactive-operator-list#tags=null##stats"
     SKIN_LIST_URL = "/arknights/database/skin-list"
     ````
   
5. Run python script 

## Technologies Used

The following technologies were used in the development:

- Python: Main language for this project
- BeautifulSoup: Python package for parsing HTML and XML documents
- Requests: Python package that allows HTTP request 
- Pymongo: Python library that provides a high-level interface for MongoDB
- MongoDB: None Relational database
