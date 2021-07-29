from selenium import webdriver
from selenium.webdriver.chrome.options import  Options
#driver = webdriver.Chrome('C:/Users/Seb/PycharmProjects/pythonProjectTinBo/chromedriver_win32 (1)/chromedriver.exe')
from random import seed
from random import random
from time import sleep, time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.keys import Keys
import pandas as pd
from bs4 import BeautifulSoup

# from secrets import username, password

'''
from selenium.webdriver.chrome.service import Service
service = Service('C:/Users/Seb/PycharmProjects/pythonProjectTinBo/chromedriver_win32 (1)/chromedriver.exe')
service.start()
'''


# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--disable-extensions")
# # chrome_options.add_argument('headless')
# chrome_options.add_argument('--hide-scrollbars')
# chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('???')
# chrome_options.add_argument('--no-proxy-server')
options = Options()
options.headless = True
df=pd.read_excel('/home/hp/workspace/pph/flask_project/flask_scraping/batch1.xlsx')

list_of_fields=["fire department","police department","gun range","whole foods near","dollar store near"]

# list_of_fields=["fire department"]
fire_department=[]
police_department=[]
gun_range=[]
foods_near=[]
dollar_store_near=[]
address_list=[]
name_list=[]
id_list=[]
print(len(df["Address"]))
for i in range (0,len(df["Address"])):
    address=df["Address"][i]+" "+df["City"][i]+" "+df["State"][i]

    # address=df["Address"][i]+", "+df["City"][i]+", "+df["State"][i]
    addresss=address
    # addresss="55-813 Congressional, La Quinta, CA"
    address_list.append(addresss)
    name_list.append(df["Name"][i])
    id_list.append(df["ID"][i])
    driver = webdriver.Chrome('/home/hp/workspace/sanjeevupwork/matthew/chromedriver', options=options)



    list_output=[]
    try:

        for i in list_of_fields:
            driver.get('https://www.google.co.in/maps/@30.7396608,76.7328256,13z')
            driver.maximize_window()
            driver.delete_all_cookies()            
            
            WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="searchboxinput"]'))).send_keys(addresss)
            driver.find_element_by_xpath('//*[@id="searchboxinput"]').send_keys(Keys.ENTER)
            time.sleep(5)
            try:
                WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,'/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[4]/div[1]/div/button'))).click()
            except:
                WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="pane"]/div/div[1]/div/div/div[4]/div[1]/div[1]/div/a'))).click()
                WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,'/html/body/jsl/div[3]/div[9]/div[8]/div/div[1]/div/div/div[4]/div[1]/div/button'))).click()
                                                                    

            WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="omnibox-directions"]/div/div[3]/div[2]/button/div'))).click()
            driver.find_element_by_xpath('//*[@id="sb_ifc51"]/input').clear()
            driver.find_element_by_xpath('//*[@id="sb_ifc52"]/input').clear()
            WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="sb_ifc51"]/input'))).send_keys(addresss)
            
        
            WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="sb_ifc52"]/input'))).send_keys(i+" "+addresss)

            driver.find_element_by_xpath('//*[@id="omnibox-directions"]/div/div[3]/div[2]/button').send_keys(Keys.ENTER)
            time.sleep(7)
            res = driver.page_source
            soup = BeautifulSoup(res, 'html.parser')

            a=soup.find('div',{'class':'section-directions-trip-distance section-directions-trip-secondary-text'})
        
            if a:
                try:
                    
                    list_output.append(a.find('div').text)
                except:
                    
                    list_output.append(a.text)

            else:
                list_output.append("NA")
        print(list_output,address)
        driver.close()
        fire_department.append(list_output[0])
        police_department.append(list_output[1])
        gun_range.append(list_output[2])
        foods_near.append(list_output[3])
        dollar_store_near.append(list_output[4])
        c1=pd.Series(data=id_list,name="ID")
        c2=pd.Series(data=address_list,name="Address")
        c3=pd.Series(data=name_list,name="Name")

        c4=pd.Series(data=fire_department,name="fire_department")
        c5=pd.Series(data=police_department,name="police_department")
        c6=pd.Series(data=gun_range,name="gun_range")
        c7=pd.Series(data=foods_near,name="foods_near")
        c8=pd.Series(data=dollar_store_near,name="dollar_store_near")
        data= pd.concat([c1, c2,c3,c4,c5,c6,c7,c8], axis=1)
        data_frame=pd.DataFrame(data).drop_duplicates().dropna()
        print(data_frame)
        data_frame.to_csv('output1.csv',index=False,mode='a',header=False, sep ='\t')
        list_output.clear()
        id_list.clear()
        address_list.clear()
        name_list.clear()
        fire_department.clear()

        police_department.clear()
        gun_range.clear()
        foods_near.clear()
        dollar_store_near.clear()
        
    except:
        pass


# print(fire_department)    
# print(police_department)    
# print(gun_range)    
# print(foods_near)    
# print(dollar_store_near)    

#   df.to_csv('my_csv.csv', mode='a', header=False)