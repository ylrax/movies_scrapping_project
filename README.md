# movies_scrapping_project
Scrapping movies data and scores from 
IMDB and FA to compare them


- Environment:

Python 2 or 3 is required as long 
as long as the packages: pandas, selenium and pyvirtualdisplay

    pip install pandas, selenium, pyvirtualdisplay, beautifulsoup4
    
The selenium package will require additional drivers to run correctly. 
The script uses Chrome (or chromium) 
as the browser, but it can be changed to 
Firefox as well.

The driver and instructions can be downloaded here: 
https://selenium-python.readthedocs.io/installation.html

<br>
A file containing the movies to get is required
and can be found as final_movies.scv

The scripts are design to run inside a raspberry pi.

- Get the imdb data:

Following as first links to grab the 
published on Kaggle and internet, the links
are gathered and their data updated
 (from a csv file)

For that we use selenium cromedriver to
start the session and get the data. It is
stored into a scv file.

    python ./imdb/imdb_bot_scraper.py
    
The code is designed to run on a raspberry pi. it could be ran
each 3 minutes (or 2 removing time waiting elapses).

As example, the following crontab can manage all the callings:

    */3 * * * * python3 ~/repos/fa_scrapper/imdb_bot_scrapper.py >> /tmp/a.log 2>&1
    
Leaving all stout and stderr on the file */tmp/a.log*. All logs 
in *imdb_scrapper.log*, all data in *imdb_films_scrapped.csv* and 
all related links on *extra_links.csv*.


- Get the Filmaffinity data:

Same goes for Filmaffinity data. The data gathered from
IMDB is read and then extracted on the Filmaffinity page.
The result is again a csv file.

    python ./imdb/fa_bot_looker_scraper.py
    
