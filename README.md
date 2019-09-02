# lunchplans

lunchplans is a small web-crawler/heroku app prototype that looks up the lunch menues at several restaurants near the TU Wien. In particular, it checks the following websites

* https://nam-nam.at/wp-content/uploads/Wochenkarten/Nam-Nam-Wochenkarte-Dabba.pdf
* http://www.feinessen.at/
* https://www.bep-viet.at/
* http://teigware.at

and presents the menues on a simple [website](https://lunchplans.herokuapp.com).

This repository serves as illustration of simple, hard coded, web crawling.

## Features:

* Uses the simply web framework [flask](https://palletsprojects.com/p/flask/) to generate a dynamic webpage.
* Uses [camelot](https://camelot-py.readthedocs.io/en/master/) to extract information of a table in pdf and saves it into a pandas data frame. If this fails, it grabs a jpg with the same information, provided by the website, and uses [PIL](https://en.wikipedia.org/wiki/Python_Imaging_Library) to slice it into the menus for a day.
* Uses [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to extract information from an html page.

## Installation on heroku:

* Get a heroku account.
* Use the information provided [here](https://stackoverflow.com/questions/49469764/how-to-use-opencv-with-heroku/51004957) to install [OpenCV](https://opencv.org/) on heroku.
* Follow the heroku deployment procedure:
* 
```sh
$ heroku login
$ heroku create (if not already created)
$ git init
$ virtual/bin/pip3 freeze > requirements.txt
$ git add .
$ git commit -m "comment"
$ git push heroku master
```
## Installation on local pc:

## Usage

## Heroku deployment: Known issues.

* If build process does not work out, look into requirements.txt if a package with version number 0.0.0 is inside and delete it.
* Apt-file: In order to use [OpenCV](https://opencv.org/) on heroku, follow the instructions [here](https://stackoverflow.com/questions/49469764/how-to-use-opencv-with-heroku/51004957).

