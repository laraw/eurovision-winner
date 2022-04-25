from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
from colored import fg
import cleantext as ct

DRIVER_PATH = r'C:/code/chromedriver.exe'



# login = driver.find_element_by_xpath("//input").send_keys(USERNAME)
# password = driver.find_element_by_xpath("//input[@type='password']").send_keys(PASSWORD)
# submit = driver.find_element_by_xpath("//input[@value='login']").click()
def cleanse(text):
    if text != None:
        if text != "":
            try:
                result = int(text)
                return result
            except ValueError:
                return text.encode('utf-8')
    return ""

def get_year_options(incSemi = False):

    start_year = 1956
    end_year = 2022
    start_year_SF = 2004
    start_year_2SF = 2008
    year_arr = list(range(start_year, end_year))
    options = []
    for  y in year_arr:
        if(y >= start_year_SF and y < start_year_2SF and incSemi):
            options.append(str(y) + "SF")
            options.append(str(y) + "F")
        elif (y >= start_year_2SF and incSemi):
            options.append(str(y) + "F")
            options.append(str(y) + "SF1")
            options.append(str(y) + "SF2")
        else:
            options.append(str(y))
    return options


def scrape_data(trId, selectName, filename, driver:webdriver.Chrome):
    try:


        labels = []
        data = []
        xpath = '//*[@id="' + trId + '"]'
        row = driver.find_element_by_xpath(xpath)
        if(trId == "submit4"):
            options = get_year_options()
        if(trId == "submit18"):
            options = []
            drop_down = Select(row.find_element_by_xpath('//select[@name="' + selectName + '"]'))
            for d in drop_down.options:
                options.append(d.text)
            
            
        for o in options:
            
            
            #checkbox = row.find_element_by_xpath('//input[@name="details"]')
            #check = checkbox.click()
            #drop_down = row.find_element_by_xpath('//select[@name="' + selectName + '"]')
            try:
                #selectNm = 'select#' + selectName
                Select(row.find_element_by_xpath('//select[@name="' + selectName + '"]')).select_by_value(o)
                
                
            except BaseException as e:
                
                print(str(e))
            submit_btn = driver.find_element_by_xpath(xpath)
            submit = submit_btn.click()
            if(len(labels) == 0):
                try:
                    if(trId == "submit4"):
                        labels.append("Year")
                    if(trId == "submit18"):
                        labels.append("Country")

                    table = driver.find_elements_by_xpath('//*[@id="tabelle1"]/thead/tr[1]/th')
                    for c in table:
                        labels.append(c.text)
                except BaseException as e:
                
                    print(str(e))
            # try:
            totalrows = driver.find_elements_by_xpath('//*[@id="tabelle1"]/tbody/tr')
            rowarr = list(range(0,len(totalrows)))
            for r in rowarr:
                xpath = '//*[@id="tabelle1"]/tbody/tr[' + str(r+1) + ']/td'
                columns = driver.find_elements_by_xpath(xpath)
                rowdata = [o]
                for c in columns:
                    
                    rowdata.append(cleanse(c.text))
                data.append(rowdata)
            # except BaseException as e:
            #     print(str(e))
            driver.execute_script("window.history.go(-1)")
            
            
        # h1 = driver.find_element_by_class_name('someclass')
        # h1 = driver.find_element_by_xpath('//h1')
        # h1 = driver.find_element_by_id('greatID')
    except BaseException as e:
        print(str(e))
        driver.quit()

    # df = pd.DataFrame.from_records(data, columns=labels)
    # df.to_csv(filename)
    driver.quit()


options = Options()
options.add_argument("--window-size=1920,1200")
#options.headless = True
driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
driver.get("https://eschome.net/")


labels = []
data = []
xpath = '//*[@id="submit18"]'
row = driver.find_element_by_xpath(xpath)

#drop_down = Select(driver.find_element_by_xpath('//*[@id="submit18"]/select[@name="country_x"]'))
options = []
drop_down = driver.find_element_by_css_selector("tr[id='submit18'] .td_home_tabelle select[name='country_x']")

for d in drop_down.options:
    options.append(str(d.text))


submit_btn = driver.find_element_by_xpath('//*[@id="submit18"]')
submit = submit_btn.click()
time.sleep(10)
# for o in options:
#     Select(driver.find_element_by_css_selector("tr[id='submit18'] .td_home_tabelle select[name='country_x']")).select_by_visible_text(o)
#     time.sleep(2)



# for o in options:
#     Select(row.find_element_by_xpath('//select[@name="country_x"]')).select_by_visible_text(str(o))
# submit_btn = driver.find_element_by_xpath(xpath)
# print(submit_btn)
# submit = submit_btn.click()
   # time.sleep(2)
    
    #driver.execute_script("window.history.go(-1)")

driver.quit()
# scrape_data("submit18", "country_x", "esc_scrape_points.csv", driver)