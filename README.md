# CS467_W2020_Capstone
###### Repository for "The Neighborhood Cookbook"

## Purpose
The Neighborhood Cookbook is a web app that seeks to utilize a web scraping module to parse out recipe details from your favorite recipe websites, allowing you to reference all of your favorite recipes while bypassing cumbersome ads and needless storytelling. 

## How to run locally

**NOTE: This repository requires Python 3 to run locally. [Go here](https://www.python.org/downloads/release/python-381/) if you need to install Python 3.**

1. Clone the git repository into your local directory of choice
2. Run `pip3 install -r requirements.txt` in terminal
3. Run `flask db init`, `flask db stamp head`, `flask db migrate`, and `flask db upgrade` in that order in terminal
4. Run `redis-server &` in terminal
5. Run `rq worker &` in terminal
6. Run `flask run` in terminal
5. Navigate to the website through `http://127.0.0.1:5000` or `http://localhost:5000`

## Credits
- [Matthew Esqueda](https://github.com/matthewjw2007)
- [Ting Sheppy](https://github.com/pdxting)
- [Brian Sprague](https://github.com/brian-sprague)
