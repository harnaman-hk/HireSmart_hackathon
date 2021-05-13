from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import json 
import os

def scrape_hearth(url):
    options = Options()
    options.add_argument('--headless')

    browser = webdriver.Firefox(options=options)

    browser.get(url)
    browser.implicitly_wait(20)

    login_element = browser.find_element_by_link_text('Log in')
    login_element.click()
    usrname = browser.find_element_by_id("id_login")
    pwd = browser.find_element_by_id("id_password")

    usrname.send_keys(os.environ.get("username"))
    pwd.send_keys(os.environ.get("passwd"))
    submit_btn = browser.find_element_by_name("submit")
    pwd.send_keys(u'\ue007')

    followers_element = browser.find_element_by_link_text('Followers')
    followers_element.click()

    # # now on the followers page
    data = {}

    # # scroll to get all followers in visible frame
    # view_more_btn = browser.find_element_by_xpath("//a[contains(@class, 'load-scroll-content button btn-blue hidden')]")
    # scroll_end = browser.find_element_by_xpath("//p[contains(@class, 'no-scroll-content-message body-font gray-text hidden')]")

    # while not scroll_end.is_displayed():
    #     try:
    #         view_more_btn.click()
    #     except Exception as e:
    #         pass

    # scrape followers
    all_followers = browser.find_elements_by_xpath("//a[contains(@class, 'track-follower-user regular dark weight-600')]")

    for i, follower in enumerate(all_followers):
        data[i] = {}
        data[i]["name"] = follower.text
        data[i]["profile_link"] = follower.get_attribute("href")
        
    for i in data:
        try:
            browser.get(data[i]["profile_link"])
            skills = browser.find_element_by_xpath("//div[contains(@class, 'attributes regular dark')]")
            data[i]["skills"] = skills.text
            data[i]["skills"] = [sk.strip() for sk in data[i]["skills"].split(',')]
            current_job = browser.find_element_by_xpath("//span[contains(@class, 'text')]")
            data[i]["cuurent_job"] = current_job.text
            browser.implicitly_wait(2)
        
        except Exception as e:
            pass

    with open("scrapeddata.json", 'w') as f:
        json.dump(data, f)

    print("Hackerearth scraping successful")