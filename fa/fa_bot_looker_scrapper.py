import logging
from selenium import webdriver
from time import sleep
from random import randint

print(randint(0, 9))

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


# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--disable-extensions')
# chrome_options.add_argument('--profile-directory=Default')
# chrome_options.add_argument("--incognito")
# chrome_options.add_argument("--disable-plugins-discovery");
# chrome_options.add_argument("--start-maximized")
# driver = webdriver.Chrome(chrome_options=chrome_options)
driver = webdriver.Chrome()
driver.delete_all_cookies()

print("Opening the web")
driver.get('https://www.filmaffinity.com/')

if len(driver.window_handles) < 1:
    print("Pop up activated 1")

sleep(4)
print("Logging stage")
log = driver.find_element_by_id("top-search-input")
log.send_keys("ice age")
log.send_keys(webdriver.common.keys.Keys.ENTER)

if len(driver.window_handles) < 1:
    print("Pop up activated 2")

table = driver.find_elements_by_css_selector('.se-it.mt')
fa_title = table[0].find_element_by_class_name('mc-title').text
print(table[0].find_element_by_class_name('mc-title').text)
print(table[0].find_element_by_class_name('ye-w').text)
print(table[1].find_element_by_class_name('mc-title').text)
print(table[1].find_element_by_class_name('ye-w').text)

sleep(4)
# cookies?
driver.find_element_by_class_name('qc-cmp-button').click()
sleep(4)
table[0].find_element_by_class_name('mc-title').click()
sleep(4)

all_info = driver.find_element_by_class_name("movie-info").text.split("\n")
all_info_dict = dict(zip(all_info[::2], all_info[1::2]))
rating = driver.find_element_by_id('rat-avg-container').text.split('\n')
critics = driver.find_element_by_id('movie-reviews-box').text.split(' ')
print(rating)
print(critics)
print(all_info_dict)
sleep(2)
driver.close()


# df = pd.DataFrame(columns=['title', 'original_title', 'year',
#                            'age_rating', 'duration', 'genres',
#                            'fa_rating', 'number_votes', "direction",
#                            'critic_number', 'plot',
#                            'music', 'producer', 'summary'])

fields = [fa_title, all_info_dict['Título original'], all_info_dict['Año'],
          'unknown', all_info_dict['Duración'], all_info_dict['Género'],
          rating[0], rating[1], all_info_dict['Dirección'],
          critics[0], all_info_dict['Guion'],
          all_info_dict['Música'], all_info_dict['Productora'], all_info_dict['Sinopsis']]
print(fields)
