from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time

# TODO 1 The program is looking at the properties found on rigmove.co.uk
prefix = "https://www.rightmove.co.uk"
# TODO 2 Google form with 3 short answers, 1 - address, 2 - price, 3 - rightmove url
FORM_URL = "https://forms.gle/XXXXXXXXXXXXXXXX"
# TODO 3 Rightmove url with filters already set. The program only looks at a first page of 25 results.
URL = "XXX"
# TODO 4 Update path to chrome driver
chrome_driver_path = r"XXX\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)
driver.get(url=URL)
address_list = driver.find_elements_by_class_name("propertyCard-address")
price_list = driver.find_elements_by_class_name("propertyCard-priceValue")
url_list = []
data_raw = requests.get(url=URL)
data = data_raw.text
soup = BeautifulSoup(data, "html.parser")

# Getting links to the properties.
# Might not be the best way to implement it but I think spending 2 hours on this algorithm would be an overkill.
for i in range(0, 50, 2):
    link = str(soup.find_all(class_="propertyCard-link")[i]).split("href")[1].split('"')[1]
    if link != "":
        url_list.append(link)
    else:
        break
new_address_list = []
new_price_list = []
new_url_list = []

for i in range(len(address_list)):
    new_address_list.append(address_list[i].text)
    new_price_list.append(float(price_list[i].text.split("£")[1].split(" ")[0]))
    new_url_list.append(prefix + url_list[i])

for i in range(len(new_address_list)):
    driver.get(url=FORM_URL)
    time.sleep(1)
    inputs = driver.find_elements_by_class_name("quantumWizTextinputPaperinputInput")
    address = new_address_list[i]
    price = new_price_list[i]
    url = new_url_list[i]
    # That [0], [1], [2] looks hideous as hell but it's Tuesday and
    # I need to get some sleep before my night shift at a warehouse :'(
    inputs[0].send_keys(address)
    inputs[1].send_keys(str(price))
    inputs[2].send_keys(url)
    driver.find_element_by_class_name("exportButtonContent").click()


driver.quit()