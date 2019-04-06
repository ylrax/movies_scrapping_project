import logging
import sys
import pandas as pd
from selenium import webdriver
from time import sleep
# from random import randint
from pyvirtualdisplay import Display

# print(randint(0, 9))

# Logger
logger = logging.getLogger("FA_SCRAPPER")
logger.setLevel(logging.INFO)
# create a file handler
handler = logging.FileHandler('fa_scrapper.log')
handler.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)

# Configuration
BASE_FILE = "/home/pi/repos/fa_scrapper/imdb_films_scrapped.csv"
SCRAPPED_DATA_OUTPUT = "/home/pi/repos/fa_scrapper/fa_films_scrapped.csv"
WEB_ADDRESS = 'https://www.filmaffinity.com/'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--profile-directory=Default')
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-plugins-discovery")
chrome_options.add_argument("--start-maximized")

# Get movie
source_df = pd.read_csv(BASE_FILE, sep=';', encoding="utf8")
source_df["ind"] = source_df.id
source_df = source_df.set_index("ind")
try:
    imdb_id, fa_name, fa_original_name, fa_year = source_df[source_df["fa"] == 0].iloc[0, 0:4]
except IndexError as e:
    print("Seems to be the end of the file with nothing to scrap")
    print("Message {}".format(e))
    sys.exit(0)

logger.info("Opening the movie {}".format(fa_name))


logger.info("Start chrome session")

options = webdriver.chrome.options.Options()
caps = options.to_capabilities()

display = Display(visible=0, size=(800, 800))
display.start()

if 0:
    webdriver_proxy = webdriver.Proxy()
    webdriver_proxy.http_proxy = "xx.xx.xx.xx:xxxx"
    webdriver_proxy.add_to_capabilities(caps)

    driver = webdriver.Chrome(options=chrome_options, desired_capabilities=caps)
else:
    driver = webdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver',
                              options=chrome_options)

driver.delete_all_cookies()

print("Opening the web")
driver.get(WEB_ADDRESS)

if len(driver.window_handles) > 1:
    print("Pop up activated 1")

sleep(4)
print("Logging stage: searching")
logger.info("Searching")
log = driver.find_element_by_id("top-search-input")
if fa_original_name != 'None':
    log.send_keys(fa_original_name)
else:
    log.send_keys(fa_name)

log.send_keys(webdriver.common.keys.Keys.ENTER)

table = driver.find_elements_by_css_selector('.se-it.mt')

if len(table) == 0:
    print("No results for: {} nor {}".format(fa_original_name, fa_name))
    logger.info("No results for: {} nor {}".format(fa_original_name, fa_name))
    driver.close()
    source_df.at[imdb_id, 'fa'] = 1
    source_df.to_csv(path_or_buf=BASE_FILE, sep=';', encoding='UTF8', index=False)
    sys.exit(0)

fa_title = table[0].find_element_by_class_name('mc-title').text
print(table[0].find_element_by_class_name('mc-title').text)
print(table[0].find_element_by_class_name('ye-w').text)
print(table[1].find_element_by_class_name('mc-title').text)
print(table[1].find_element_by_class_name('ye-w').text)


sleep(4)
if len(driver.window_handles) > 1:
    print("Pop up activated 3")
    print(driver.window_handles)
    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

# cookies?
sleep(2)
driver.find_element_by_class_name('qc-cmp-buttons').click()
# except:
#     print('fail')
#     driver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/button').click()


sleep(1)
# find the exact year
all_years = [table[i].find_element_by_class_name('ye-w').text for i in range(len(table))]
try:
    table_position = all_years.index(str(fa_year))
except ValueError:
    driver.find_element_by_class_name('see-all-button').click()
    all_years = [table[i].find_element_by_class_name('ye-w').text for i in range(len(table))]
    table_position = all_years.index(str(fa_year))

driver.find_elements_by_css_selector('.se-it.mt')[table_position].find_element_by_class_name('mc-poster').click()
sleep(4)

logger.info("Scrapping movie data")

all_info = driver.find_element_by_class_name("movie-info").text.split("\n")
print(all_info)

all_info_dict = dict(zip(all_info[::2], all_info[1::2]))
rating = driver.find_element_by_id('rat-avg-container').text.split('\n')
critics = driver.find_element_by_id('movie-reviews-box').text.split(' ')
print(rating)
print(critics)
print(all_info_dict)
sleep(2)
driver.close()
display.stop()
logger.info("Chrome session closed successfully")

# df = pd.DataFrame(columns=['title', 'original_title', 'year',
#                            'age_rating', 'duration', 'genres',
#                            'fa_rating', 'number_votes', "direction",
#                            'critic_number', 'plot',
#                            'music', 'producer', 'summary'])

fields = [fa_title, all_info_dict['Título original'], all_info_dict['Año'],
          'unknown', all_info_dict['Duración'], all_info_dict['Género'],
          rating[0], rating[1], all_info_dict['Dirección'],
          critics[0], all_info_dict['Guion'],
          all_info_dict['Música'], all_info_dict['Productora'], all_info_dict.get('Sinopsis', 'None')]
print(fields)
logger.info("Saving data")

# df = pd.DataFrame(columns=['title', 'original_title', 'year',
#                            'age_rating', 'duration', 'genres',
#                            'fa_rating', 'number_votes', "direction",
#                               'criticas', 'guion'
#                             'musica', 'productora', 'sinopsis'])


# with open(SCRAPPED_DATA_OUT, 'a', newline='') as f:
#     writer = csv.writer(f, delimiter=';')
#     writer.writerow(fields)

source_df.at[imdb_id, 'fa'] = 1
source_df.to_csv(path_or_buf=BASE_FILE, sep=';', encoding='UTF8', index=False)

logger.info("Done and finished")
