import csv
import logging
import pandas as pd

from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from pyvirtualdisplay import Display


# Logger
logger = logging.getLogger("IMDB_SCRAPPER")
logger.setLevel(logging.INFO)
# create a file handler
handler = logging.FileHandler('imdb_scrapper.log')
handler.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)

# Configuration
BASE_FILE = "./final_movies.csv"
SCRAPPED_DATA = "./imdb_films_scrapped.csv"
WEB_ADDRESS = 'https://www.imdb.com/title/'

old_df = pd.read_csv(BASE_FILE, sep=',')
old_df["ind"] = old_df.titleId
old_df = old_df.set_index("ind")
imdb_id = old_df[old_df["captured"] == 0].iloc[0, 0]
logger.info("Opening the id {}".format(imdb_id))


display = Display(visible=0, size=(800, 800))
display.start()

driver = webdriver.Chrome()
print("Opening the web", WEB_ADDRESS + imdb_id)
driver.get(WEB_ADDRESS + imdb_id)

sleep(4)

logger.info("Scrapping all movie characteristics...")
title_scrapped = driver.find_element_by_class_name("title_wrapper").text.split("\n")
if len(title_scrapped) == 3:
    title, title_original, characteristics = title_scrapped
else:
    title, characteristics = title_scrapped
    title_original = "None"
rating, votes, _ = driver.find_element_by_class_name("ratings_wrapper").text.split("\n")
year = driver.find_element_by_id("titleYear").text[1:-1]
direction = driver.find_element_by_class_name("credit_summary_item").text
try:
    complete_title_bar = driver.find_element_by_class_name("titleReviewBar").text.split("\n")
    print(len(complete_title_bar))
    if len(complete_title_bar) == 7:
        metacritic_score, _, _, _, critic_data, _, popularity = complete_title_bar
    elif len(complete_title_bar) == 2:
        metacritic_score = None
        popularity = " ("
        critic_data = "        "
    else:
        metacritic_score = None
        popularity = " ("
        critic_data = complete_title_bar

except NoSuchElementException:
    metacritic_score = None
    popularity = " ("
    critic_data = "        "

sleep(2)
driver.close()
display.stop()


logger.info("webdriver connection closed successfully")
print(title, title_original, characteristics)
# print(rating, votes)
# print(year)
# print(direction)
# print(metacritic_score, critic_data, popularity)

# df = pd.DataFrame(columns=['id', 'title', 'original_title', 'year',
#                            'age_rating', 'duration', 'genres',
#                            'imdb_rating', 'number_votes', "direction",
#                            'metacritic_score', 'critic_number', 'number_critics', 'popularity'])

print("\n\n")
# splits
characteristics_list = characteristics.split("|")
if len(characteristics_list) == 2:
    characteristics_list = ["Unknown"] + characteristics_list

fields = [imdb_id, title.split("(")[0].strip(), title_original.split("(")[0].strip(), year,
          characteristics_list[0].strip(), characteristics_list[1].strip(), characteristics_list[2].strip(),
          rating[:-3], votes, direction,
          metacritic_score, critic_data.split(" ")[0],
          critic_data.split(" ")[3], popularity.split("(")[0].strip()]

print(fields)

logger.info("saving reference and scrapped info")

with open(SCRAPPED_DATA, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(fields)

old_df.at[imdb_id, 'captured'] = 1
old_df.to_csv(path_or_buf=BASE_FILE, sep=',', encoding='UTF8', index=False)

logger.info("Done")
