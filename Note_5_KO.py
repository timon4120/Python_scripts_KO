from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import rich.progress
import argparse
import time
import json

"""
Kamil Orzechowski
| The program enters the YT website, enters a given phrase in the search engine, 
| enters the channel and from the movies tab downloads the titles, dates and number of views of movies from N scrolls.
| Chromedriver.exe is required! YT dynamic scraper :)
Exec: python Note_5_KO.py 
Flags:
--filename : output .json filename
--iter : Number of scrolls on the webpage. If you dont't use the flag, default value equals 10.
--title : YT Channel Title. If you dont't use the flag, default value is 'RMF'.
"""

def make_it_possible_chrome(N,title):
    options = Options()
    service = Service('./chromedriver.exe')
    driver = webdriver.Chrome(service = service, options=options)
    driver.maximize_window()

    driver.get('https://www.youtube.com')
    time.sleep(5)

    driver.find_element(By.XPATH,'//*[@id="content"]/div[2]/div[6]/div[1]/ytd-button-renderer[2]/yt-button-shape/button').click()
    time.sleep(5)

    xd1 = driver.find_element(By.NAME,'search_query')
    xd1.send_keys(title)
    time.sleep(5)

    driver.find_element(By.XPATH,'//*[@id="search-icon-legacy"]').click()
    time.sleep(5)

    driver.find_element(By.XPATH,'//*[@id="channel-title"]').click()
    time.sleep(5)

    driver.find_element(By.XPATH,'//*[@id="tabsContent"]/tp-yt-paper-tab[2]').click()
    time.sleep(5)

    for i in rich.progress.track(range(int(N))): 
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN) 
        time.sleep(1)

    xx = driver.find_elements(By.XPATH, '//*[@id="video-title"]')
    yy = driver.find_elements(By.XPATH, '//*[@id="metadata-line"]')

    map_x = list(map(lambda x : x.text,xx))
    map_x = list(filter(lambda x : x != '',map_x))
    map_y = list(map(lambda y : y.text,yy))
    map_y = list(filter(lambda y : y != '',map_y))
    map_y = list(map(lambda y : y.split('\n'),map_y))

    driver.close()
    dict_map = {}
    for i,j in zip(map_x,map_y): dict_map[i] = j
    return dict_map

def main():
    argp = argparse.ArgumentParser()
    argp.add_argument("--filename", default = "output")
    argp.add_argument("--iter", default = 10)
    argp.add_argument("--title", default = "RMF")
    args = argp.parse_args()

    dct = make_it_possible_chrome(args.iter,args.title)

    with open(f"{args.filename}.json","w") as f:
        json.dump(dct,f,indent=6) 

if __name__ == '__main__':
    main()
