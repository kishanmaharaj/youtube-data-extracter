from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager

 

url = input() 



driver = webdriver.Chrome(ChromeDriverManager().install())  
channel_url = url + "/videos?view=0&sort=p&flow=grid"

print ("Requesting URL: " + channel_url)
driver.get(channel_url) 
print ("Channel found ...")

element_xpath = '//*[@id="items"]' 
element = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
print ("Scrolling document upto bottom ...")

for i in tqdm(range(100), desc="Scrolling"):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
body = driver.find_element_by_tag_name("body").get_attribute("innerHTML")

print("Closing Chrome ...") 
driver.quit()    
 

soupBody = BeautifulSoup(body,features = "html.parser")
channel_name = soupBody.findAll("yt-formatted-string", {"class" : "style-scope ytd-channel-name"})[0].text 
subscriber_count = soupBody.findAll("yt-formatted-string", {"id" : "subscriber-count"})[0].text
 
views_time = soupBody.findAll("span", {"class": "style-scope ytd-grid-video-renderer"})
video_info = soupBody.findAll("h3", {"class": "style-scope ytd-grid-video-renderer"})
upload_time = views_time[0 : len(views_time) : 2]
views = views_time[1 : len(views_time) : 2]

 
filename = "results/"+channel_name+".csv"

 
header = ["video name","upload time","views"]
 
rows = []
print("Creating CSV DATA")
for i in tqdm(range(len(video_info)), desc = "CSV "):
    x = [video_info[i].text, views[i].text, upload_time[i].text]
    rows.append(x)

 
with open(filename, 'w') as csvfile:  
    csvwriter = csv.writer(csvfile)  
    csvwriter.writerow(header)  
    csvwriter.writerows(rows) 
