from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

def writeTofile(a):
    f = open("TODO: enter path", "a")
    f.write(a)
    f.write("\n")
    f.close()


# Return all camera links for a specific camera brand
# Sample camera link: "https://www.flickr.com/cameras/samsung/"
# You may iterate over a list of camera links retrieved from the flickr API.
wd = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
wd.get() #TODO: Put flickr camera link

search = wd.find_elements(By.TAG_NAME, "a")

search = list(set(search))
elems = []
search2 = wd.find_elements(By.TAG_NAME, "a")

for s2 in search2:
    print(s2.text.strip())
    try:
        print(s2.find_element(By.TAG_NAME, "i").text.strip())
    except:
        print("".strip())

wd.close()
wd.quit()
