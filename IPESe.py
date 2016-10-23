from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests,csv
from bs4 import BeautifulSoup

driver = webdriver.Chrome()
driver.get("http://www.ipe.org.cn/pollution/corporation.aspx")
inputText=driver.find_element_by_id("s_Text")
inputText.clear()
inputText.send_keys("鞍钢")
queryBtn = driver.find_element_by_id("btn_search")
queryBtn.send_keys(Keys.RETURN)

bsObj= BeautifulSoup(driver.page_source, 'html.parser')
nameTags=bsObj.findAll(attrs={"class":"tlp2"})
names=[]

linkTags=bsObj.findAll(attrs={"class":"sotlp4"})
links=[]
baseUrl="http://www.ipe.org.cn/pollution/"

for i in range(1,len(nameTags)):
    links.append(baseUrl+linkTags[i].a.get('href'))
    names.append(nameTags[i].text.strip())

for i in range(2,6):

    numText = driver.find_element_by_id("AspNetPager1_input")
    numText.clear()
    numText.send_keys(i)
    goBtn = driver.find_element_by_id("AspNetPager1_btn")
    goBtn.send_keys(Keys.RETURN)

    bsObj = BeautifulSoup(driver.page_source, 'html.parser')
    nameTags = bsObj.findAll(attrs={"class": "tlp2"})

    linkTags = bsObj.findAll(attrs={"class": "sotlp4"})
    baseUrl = "http://www.ipe.org.cn/pollution/"

    for j in range(1, len(nameTags)):
        links.append(baseUrl + linkTags[j].a.get('href'))
        names.append(nameTags[j].text.strip())
driver.close()

namesAndLinks=zip(names,links)

# 打开文件
with open('namesLinks.csv', 'w') as csvfile:
    writeHandler=csv.writer(csvfile,dialect='excel')
    writeHandler.writerows(namesAndLinks)


recordsWrite=[]
for i in links:
    url = requests.get(i)
    bsObj = BeautifulSoup(url.text, 'html.parser')
    td = bsObj.findAll(attrs={'width': "590", 'align': "left", 'colspan': "3", 'class': "pluu"})
    records = td[4].text.strip().split('\r')
    writeRes = ""
    for line in records:
        writeRes += line
    recordsWrite.append(writeRes)

finalRes=zip(names,links,recordsWrite)
print(len(names),len(links),len(recordsWrite))
# 打开文件
with open('csv_test.csv', 'w') as csvfile:
    writeHandler=csv.writer(csvfile,dialect='excel')
    writeHandler.writerows(finalRes)