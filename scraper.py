from selenium import webdriver
import pandas as pd
import smtplib
import os
import json
import time
from selenium.webdriver.common.by import By
from msedge.selenium_tools import EdgeOptions, Edge


search_query = 'https://www.youtube.com/feed/trending'

def get_driver():
    options = EdgeOptions()
    options.use_chromium = True
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    driver = Edge(executable_path="C:\Program Files (x86)\Microsoft\Edge\Application\msedge_driver\msedgedriver.exe",options = options)
    return driver


def get_videos(driver):
    driver.get(search_query)
    time.sleep(5)
    video_containers = driver.find_elements(By.TAG_NAME, 'ytd-video-renderer')
    print(f'Found{len(video_containers)} videos')
    return video_containers

def parse_videos(video):
    # Extract video title
    title_element = video.find_element(By.ID, 'video-title')
    title = title_element.text
    url = title_element.get_attribute('href')
    
    thumbail_tag = video.find_element(By.TAG_NAME,'img')
    thumbnail_url = thumbail_tag.get_attribute('src')
    
    channel = video.find_element(By.CLASS_NAME,'ytd-channel-name')
    channel_name = channel.text 
    
    description = video.find_element(By.ID,'description-text').text 
    
    return{
        'title': title,
        'url': url,
        'thumbnail':thumbnail_url,
        'channel': channel_name,
        'description': description
    }
    
if __name__ == '__main__':
        print("Creating Driver")
        driver = get_driver()
        
        print("Fetching the data")
        videos1 = get_videos(driver)
        print(f'Found {len(videos1)} videos')
        
        print("Parsing top 10 videos")
        data = [parse_videos(video) for video in videos1[:10]]
        
        print("Save the data to csv")
        
        df = pd.DataFrame(data)
        print(df)
        df.to_csv('trending.csv',index=None)
        