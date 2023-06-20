import requests
from bs4 import BeautifulSoup

response = requests.get("https://www.youtube.com/feed/trending")

print("Status code",response.status_code)
print("Output",response.text)

with open('trending.html', 'w', encoding='utf-8') as f:
    f.write(response.text)

doc = BeautifulSoup(response.text,'html.parser')

print('Page title:', doc.title.text)

#find all the video divs

video_div = doc.find_all('div',class_ = 'ytd-video-renderer')
print(f"Found {len(video_div)} videos")