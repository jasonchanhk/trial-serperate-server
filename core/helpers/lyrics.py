from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup

firefox_installation = GeckoDriverManager().install()

def click_on_page(song_name, artist_name):
    if artist_name == "":
        artist_name = "none"   

    options = Options()
    # options.headless = True
    driver = webdriver.Firefox(options=options, service = Service(firefox_installation))

    search_URL = f"https://lyricstranslate.com/en/translations/328/42/{artist_name}/{song_name}/none/0/0/0/0"
    driver.get(search_URL)
    print(search_URL)

    try:
        WebDriverWait(driver, 4).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/div/div/div[2]/div/button[2]'))).click()
    except TimeoutException:
        print("no accept cookie button")
        pass
    
    try:
        WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="lyricstranslatesearch-searchtranslate-form"]/div/div[2]/table[2]/tbody/tr[1]/td[2]/a'))).click()
    except TimeoutException:
        print("can't click on first search")
        pass  

    try:
        WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="lyrics-preview"]/p/a'))).click()
    except TimeoutException:
        print("no show lyrics button")
        pass    

    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,'//*[@id="song-body"]')))
    except TimeoutException:
        print("no original lyrics")
        pass    

    page_source = driver.page_source
    driver.close()
    return page_source

def scrap_content(source):
    soup = BeautifulSoup(source, 'lxml')
    return soup

def parse_into_array(element):
    arr = []

    for par in element:
        each_line = par.find_all("div")
        arr.append(" ")
        for line in each_line:
            arr.append(line.text)

    return arr

def render_lyrics(source, language):
    soup = scrap_content(source)
    class_tag = ""

    if language == "english":
        class_tag = "song-node-text"
    elif language == "spanish":
        class_tag = "translate-node-text"

    lyrics_elements = soup.find("div", class_=class_tag)
    block_elements = lyrics_elements.find("div", class_="ltf direction-ltr")
    par_elements = block_elements.find_all("div", class_="par")

    arr = parse_into_array(par_elements)
    return arr
