import yaml
import pytest
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep

with open("settings.conf", "r") as ymlfile:
    cfg = yaml.full_load(ymlfile)

# FUNCTION DEFINITIONS:

def scrape_canvas():
    # options
    options = webdriver.ChromeOptions()

    # declare prefs
    prefs = {"download.prompt_for_download" : False, "download.default_directory" : cfg["save_location"]}

    # add prefs
    options.add_experimental_option("prefs", prefs)

    chrome_driver = webdriver.Chrome(service=Service(cfg["chromedriver_location"]), options=options)
    chrome_driver.get('https://utexas.instructure.com/')
    #chrome_driver.maximize_window()

    if not "Sign in with your UT EID" in chrome_driver.title:
        chrome_driver.quit()
        raise Exception("Could not load page, check internet connection")

    # Enter login information
    chrome_driver.find_element(By.NAME, "j_username").send_keys(cfg["login"]["username"])
    chrome_driver.find_element(By.NAME, "j_password").send_keys(cfg["login"]["passwd"] + Keys.ENTER)


    if not chrome_driver.find_element(By.ID, "duo_iframe"):
        raise Exception("Could not log in, please check credentials in scraper-settings.conf")
    else:
        print("waiting for you to authenticate with duo")
        while True:
            sleep(1)
            if("Dashboard" in chrome_driver.title):
                break

    # Now logged in, try to navigate to courses
    chrome_driver.get('https://utexas.instructure.com/courses')


    course_links = []

    for element in chrome_driver.find_elements(By.CSS_SELECTOR, "*"):
        try:
            if "/courses/" in element.get_attribute('href'):
                link = element.get_attribute('href')
            if link != None and link not in course_links:
                course_links.append(link)
        except:
            pass

    num_of_downloads = 0
    courses_downloaded = []
    # go through each course and download all files
    for link in course_links:

        #Load modules webpage for courses
        chrome_driver.get(link + "/files")

        course_name = chrome_driver.find_element(By.CLASS_NAME, "ellipsible").text
        print("Scraping " + str(course_name))

        if "Files" in chrome_driver.title:

            sleep(3)
            #select all files
            checkbox = chrome_driver.find_element(By.ID, "selectAllCheckbox")
            chrome_driver.execute_script("arguments[0].setAttribute('class','')", checkbox)

            checkbox.click()
            chrome_driver.find_element(By.XPATH, '//*[@id="content"]/div/header[2]/div/div/button').click()
            #wait for processing to finish
            sleep(5)
            while True:
                sleep(1)
                try:
                    chrome_driver.find_element(By.CLASS_NAME, "alert")
                except:
                    break
            num_of_downloads = num_of_downloads + 1
            courses_downloaded.append(course_name)

        else:
            print("Course has no files")

    with open(cfg["save_location"] + "course_list.txt", "w+") as f:
      for listitem in courses_downloaded:
        f.write('%s\n' % listitem)

    input("Type anything when it finishes downloading...")
    print("reached end of script, quitting in 10 seconds")
    sleep(10)
    chrome_driver.quit()

scrape_canvas()
