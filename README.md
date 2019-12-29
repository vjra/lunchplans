# lunchplans

lunchplans is a small web-scraper/heroku app prototype that looks up the lunch menus at several restaurants near the TU Wien. 
In particular, it checks the following websites

* https://nam-nam.at
* http://www.feinessen.at/
* https://www.bep-viet.at/
* http://teigware.at

and presents the menus on a simple [website](https://lunchplans.herokuapp.com).

This repository serves as illustration of simple, hard coded, web scraping.

## Features:

* Uses the simply web framework [flask](https://palletsprojects.com/p/flask/) to generate a dynamic webpage.
* Uses [camelot](https://camelot-py.readthedocs.io/en/master/) to extract information of a table in pdf and saves it into a pandas data frame. If this fails, it grabs a jpg with the same information, provided by the website, and uses [PIL](https://en.wikipedia.org/wiki/Python_Imaging_Library) to slice it into the menus for a day.
* Uses [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to extract information from an html page.
* Updates every 6 days to look for a new pdf or jpg from dabba(https://nam-nam.at).

## Installation on heroku:

* Get a heroku account.
* Use the information provided [here](https://stackoverflow.com/questions/49469764/how-to-use-opencv-with-heroku/51004957) to install [OpenCV](https://opencv.org/) on heroku.
* Follow the heroku deployment procedure:

```sh
$ heroku login
$ heroku create (if not already created)
$ git init
$ virtual/bin/pip3 freeze > requirements.txt
$ git add .
$ git commit -m "comment"
$ git push heroku master
```
## Local installation:
Open a terminal and change directory to your preferred installation folder.

```sh
$ git clone https://github.com/vjra/lunchplans.git
§ (optional) create or switch into a virtual python3 enviroment.
$ pip3 install -r requirements.txt
$ python3 lunchplans.py
```
After execution, you find that the website runs locally on http://127.0.0.1:5000/.

## Known issues.

### In general:


### Heroku deployment:

* If the build process on heroku does not work out, look into requirements.txt for a package with version number 0.0.0 and delete it.
* Apt-file: In order to use [OpenCV](https://opencv.org/) on heroku, follow the instructions [here](https://stackoverflow.com/questions/49469764/how-to-use-opencv-with-heroku/51004957).


