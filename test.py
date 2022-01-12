import gc
import time
import pandas as pd
from selenium import webdriver

url = "https://bscscan.com/token/0x18b426813731c144108c6d7faf5ede71a258fd9a#balances"
option = webdriver.ChromeOptions()
# option.add_argument("--headless")
option.add_argument("window-size=1200,800")

driver = webdriver.Chrome("chromedriver", options=option)
driver.get(url)
time.sleep(3)

fields = ['Address', 'Quantity']
data = []
flg = False

iframe = driver.find_element_by_id("tokeholdersiframe")
driver.switch_to.frame(iframe)
time.sleep(3)

trs =  driver.find_elements_by_css_selector("table.table-md-text-normal tbody tr")
time.sleep(2)
for tr in trs :
    try:
        tmp = tr.find_element_by_css_selector("td span i")
        pass
    except:
        address = tr.find_element_by_css_selector("td span a").text
        quantity = tr.find_elements_by_css_selector("td")[2].text
        quantity = quantity.replace(",", "")
        if "Null Address:" not in address and float(quantity) >= 1000000000 :
            data.append([address, quantity])    

for i in range(0, 3) :
    nextNavigation = driver.find_element_by_css_selector('a[aria-label="Next"]')
    nextNavigation.click()
    time.sleep(3)

    trs =  driver.find_elements_by_css_selector("table.table-md-text-normal tbody tr")

    for tr in trs :
        try:
            tmp = tr.find_element_by_css_selector("td span i")
            pass
        except:
            address = tr.find_element_by_css_selector("td span a").text
            quantity = tr.find_elements_by_css_selector("td")[2].text
            quantity = quantity.replace(",", "")
            if "Null Address:" not in address and float(quantity) >= 1000000000 :
                data.append([address, quantity])
    
driver.close()

dataTable = pd.DataFrame(data, columns=fields)
dataTable.to_csv("result.csv")

