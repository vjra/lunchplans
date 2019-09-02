# lunchplans

lunchplans is a small web-crawler/heroku app prototype that looks up the lunch menues at several restaurants near the TU Wien. In particular, it checks the following websites

* https://nam-nam.at/wp-content/uploads/Wochenkarten/Nam-Nam-Wochenkarte-Dabba.pdf
* http://www.feinessen.at/
* https://www.bep-viet.at/
* http://teigware.at

and presents the menues on a simple [website](https://lunchplans.herokuapp.com).

This repository serves as illustration of simple, hard coded, web crawling.

## Installation

## Usage

## Heroku deployment: Known issues.

* If build process does not work out, look into requirements.txt if a package with version number 0.0.0 is inside and delete it.
* Apt-file: In order to use [OpenCV](https://opencv.org/) on heroku, follow the instructions [here](https://stackoverflow.com/questions/49469764/how-to-use-opencv-with-heroku/51004957).

