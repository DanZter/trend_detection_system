#imports here
from re import T
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import random
import datetime
import pandas as pd
import datetime
from tqdm import tqdm

import requests # request img from web
import shutil # save img locally
import os

import IPython.display as display
# from PIL import Image

# constants
n_years = 2
numdays = n_years * 365
base = datetime.datetime.today()
start_date = base - datetime.timedelta(days=numdays)
start_date = datetime.date.strftime(start_date, "%Y-%m-%d")
end_date = "2021-05-27"

nba_players_instahandles = ['kingjames', 'stephencurry30', 'russwest44', 'kyrieirving', 'EasyMoneySniper', 
                           'jharden13', 'cp3', 'zo', 'damianlillard', 'giannis_an34', 'ygtrece', 'klaythompson',
                           'lamelo', 'antdavis23', 'lukadoncic', 'kuz', 'zionwilliamson']
upcoming_nba_players = ['jamorant', 'theanthonyedwards_', 'jordan_poole', 'jokicnikolaofficial', 'melo']

football_players_instahandles = ['cristiano', 'leomessi', 'kevindebruyne', '_rl9', 'mosalah', 'k.mbappe', 'harrykane',
                                 'hm_son7', 'lukamodric10', 'neymarjr']
f1_players_instahandles = ["maxverstappen1", "lewishamilton", "landonorris", "valtteribottas", "carlossainz55", "charles_leclerc",
                           "danielricciardo", "georgerussell63", "fernandoalo_oficial", "pierregasly"]
def random_time():
    random_t = random.uniform(4, 8)
    return random_t

def log_in():
    #specify the path to chromedriver.exe (download and save on your computer)
    driver = webdriver.Chrome(executable_path = './chromedriver')
    #open the webpage
    driver.get("http://www.instagram.com")
    time.sleep(random_time())
    try:
        cookie_1 = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Only Allow Essential Cookies")]'))).click()
    except:
        cookie_2 = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Accept All")]'))).click()
        pass
    
    #target username
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))

    #enter username and password
    username.clear()
    # username.send_keys("dannysimonuk@gmail.com")
    # username.send_keys("silcoolgal01@gmail.com")
    username.send_keys("silcoolgal2@gmail.com")
    password.clear()
    password.send_keys("Blackrose_007")

    time.sleep(random_time())
    #target the login button and click it
    button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "Log")]'))).click()
    # button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    #We are logged in!
    time.sleep(random_time())
    # try:
    #     cookie_1 = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Only Allow Essential Cookies")]'))).click()
    # except:
    #     cookie_2 = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Accept All")]'))).click()
    #     pass
    try:
        time.sleep(random_time())
        alert = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not now")]'))).click()
    except:
        time.sleep(random_time())
        alert2 = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
    
    return driver

def process(handle, driver, start_date):
    nba_dict = {}
    time.sleep(random_time())
    driver.get(f"http://www.instagram.com/{handle}/")
    posts = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "posts")]'))).text.replace('posts', "").strip()
    followers = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "followers")]'))).text.replace('followers', "").strip()
    following = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "following")]'))).text.replace('following', "").strip()
    try:
        title = driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[2]/span").text
    except:
        title = ''
    try:
        bio = driver.find_element_by_class_name('QGPIr').text
    except:
        bio = ''
    
    JS_SCROLL_SCRIPT = "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;"
    JS_PAGE_LENGTH_SCRIPT = "var lenOfPage=document.body.scrollHeight; return lenOfPage;"
    
    # last_position = driver.execute_script(JS_PAGE_LENGTH_SCRIPT)
    # print(current_position, last_position)
    last_position = 0
    max_attempt = 2
    attempt = 0
    scroll_more = True
    posts_list = []
    posts_list_final = []
    next_button = 0
        
    while scroll_more:
        try:
            time.sleep(random_time())
            uploaded_posts = driver.find_elements_by_class_name('FFVAD')
            uploaded_posts_click = driver.find_elements_by_class_name('_9AhH0')
            for uploaded_post, uploaded_post_click in zip(uploaded_posts, uploaded_posts_click): 
                if uploaded_post.get_attribute('src')[:117] not in posts_list:
                    time.sleep(random_time())
                    print("***"*10)
                    posts_dict_final = {}
                    uploaded_post_click.click()
                    src_url = uploaded_post.get_attribute('src')[:117]
                    src_url_full = uploaded_post.get_attribute('src')
                    posts_dict_final[src_url_full] = {}
                    posts_dict_final[src_url_full]['post_date'] = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, '_1o9PC'))).get_attribute('datetime') #driver.find_element_by_class_name('_1o9PC').get_attribute('datetime')
                    try:
                        posts_dict_final[src_url_full]['post_bio'] = driver.find_element_by_xpath("/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/div/li/div/div/div[2]/div[1]/span").text
                    except:
                        posts_dict_final[src_url_full]['post_bio'] = ''
                    posts_dict_final[src_url_full]['post_hashtags'] = [x.text for x in driver.find_elements_by_class_name('xil3i')]
                    try:
                        posts_dict_final[src_url_full]['likes'] = int(driver.find_element_by_xpath("/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div/div/a/div/span").text.replace(',', '').replace('.', ''))
                    except:
                        pass
                    try:
                        posts_dict_final[src_url_full]['likes'] = int(driver.find_element_by_xpath("/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div[2]/div/a/div/span").text.replace(',', '').replace('.', ''))
                    except:
                        pass
                    try:
                        posts_dict_final[src_url_full]['likes'] = int(driver.find_element_by_xpath("/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/section[2]/div/div/div/a[1]/div").text.replace(',', '').replace('.', ''))
                    except:
                        pass
                    try:
                        posts_dict_final[src_url_full]['likes'] = int(driver.find_element_by_xpath("/html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/section[2]/div/span/div/span").text.replace(',', '').replace('.', ''))
                    except:
                        pass 
                    
                    try:
                        posts_dict_final[src_url_full]['type'] = driver.find_element_by_css_selector("video.tWeCl").get_attribute('type') 
                    except:
                        posts_dict_final[src_url_full]['type'] = 'photo'
                        
                    print(posts_dict_final)
                    posts_list_final.append(posts_dict_final)
                    posts_list.append(src_url)
                    
                    url = src_url_full 
                    file_name = f"/Users/dannysimon/Documents/QARIK/OPUS/output/posts/nba/{handle}/{posts_dict_final[src_url_full]['post_date']}.png" #input('Save image as (string):') #prompt user for file_name
                    res = requests.get(url, stream = True)
                    
                    if res.status_code == 200:
                        with open(file_name,'wb') as f:
                            shutil.copyfileobj(res.raw, f)
                            print('Image sucessfully Downloaded: ',file_name)
                    else:
                        print('Image Couldn\'t be retrieved')
                        
                    time.sleep(random_time())
                    driver.back()

                    if posts_dict_final[src_url_full]['post_date'] < start_date:
                        scroll_more = False
                        break
            current_position = driver.execute_script(JS_SCROLL_SCRIPT)
            if last_position == current_position:
                attempt += 1
                current_position = driver.execute_script(JS_SCROLL_SCRIPT)
                if attempt == max_attempt:
                    scroll_more = False
            else:
                attempt = 0
                last_position = current_position
        except:
            # driver = log_in() 
            driver.get(f"http://www.instagram.com/{handle}/")
        
    nba_dict['title'] = title
    nba_dict['insta_handle'] = handle
    nba_dict['no_posts'] = int(posts.replace('k', '000').replace('m', '000000').replace(',', '').replace('.', ''))
    nba_dict['followers'] = int(followers.replace('k', '000').replace('m', '000000').replace(',', '').replace('.', ''))
    nba_dict['following'] = int(following.replace('k', '000').replace('m', '000000').replace(',', '').replace('.', ''))
    nba_dict['bio'] = bio
    nba_dict['posts'] = posts_list_final
    
    return nba_dict, handle
    # /html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/ul[1]/div/li/div/div/div[2]/div[1]/span
    # /html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/ul[3]/div/li/div/div/div[2]/div[1]/span
    # /html/body/div[6]/div[3]/div/article/div/div[2]/div/div/div[2]/div[1]/ul/ul[20]/div/li/div/div/div[2]/div[1]/span
def main(start_date, nba_players_instahandles):  
    loop_more = True
    try:
        driver = log_in()  
    except:
        driver = log_in()
    nba_list = []
    nba_list_completed = []
    
    # while loop_more:
    for handle in tqdm(nba_players_instahandles[0:2]):
        if handle not in nba_list_completed:
            # exist or not.
            if not os.path.exists(f"/Users/dannysimon/Documents/QARIK/OPUS/output/posts/nba/{handle}"):
                
                # if the demo_folder directory is not present 
                # then create it.
                os.makedirs(f"/Users/dannysimon/Documents/QARIK/OPUS/output/posts/nba/{handle}")
            try:
                nba_dict, nba_completed = process(handle, driver, start_date)
                nba_list_completed.append(nba_completed)
                nba_list.append(nba_dict)
                print("<"*30, nba_completed, ">"*30)
            except:
                driver = log_in()
                pass
        # if nba_players_instahandles == nba_list_completed:
        #     loop_more = False

    nba_df = pd.DataFrame(nba_list)
    nba_df.to_csv('./output/nba_new_players.csv')

main(start_date, upcoming_nba_players)      

