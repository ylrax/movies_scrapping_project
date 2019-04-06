# movies_scrapping_project
Scrapping movies data and scores from 
IMDB and FA to compare them


- Environment:

Python 2 or 3 is required as long 
as long as the packages: pandas, selenium and pyvirtualdisplay

    pip install pandas, selenium, pyvirtualdisplay
    
The selenium package will require additional drivers to run correctly. 
The script uses Chrome (or chromium) 
as the browser, but it can be changed to 
Firefox as well.

The driver and instructions can be downloaded here: 
https://selenium-python.readthedocs.io/installation.html

<br>
A file containing the movies to get is required
and can be found as final_movies.scv

The scripts are design to run iside a raspberry pi.

- Get the imdb data:

Following as first links to grab the 
published on Kaggle and internet, the links
are gathered and their data updated
 (from a csv file)

For that we use selenium cromedriver to
start the session and get the data. It is
stored into a scv file.

    python ./imdb/imdb_bot_scraper.py

- Get the Filmaffinity data:

Same goes for filmaffinity data. The data gathered from
IMDB is read and then extracted on the Filmaffinity page.
The result is again a csv file.

    python ./imdb/fa_bot_looker_scraper.py
    
