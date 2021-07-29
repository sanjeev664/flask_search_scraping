from logging import debug
from flask import Flask, render_template, redirect, url_for, request
from pandas._config.config import options
from pandas.tseries.offsets import Hour
from selenium import webdriver
from selenium.webdriver.chrome.options import  Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import pandas as pd
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import csv


# Initialize the Flask application
app = Flask(__name__)

global my_dict, first_link, second_link, new, first_text, second_text, Profession1, Profession2

# This is main Route
@app.route('/')
def main():
    return render_template('app/home.html')


# Get the author information
def impo_link(second_link, new, my_dict):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome("/home/hp/workspace/sanjeevupwork/matthew/chromedriver", options=options)
    for link in second_link:
        driver.get(link)
        driver.delete_all_cookies()
        time.sleep(5)
        driver.maximize_window()
        # Click on the cookies button 
        try:
            WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div[3]/div/div[1]/div/div[2]/div/button[2]'))).click()
        except:
            pass
        # relations persons
        res = driver.page_source
        soup = BeautifulSoup(res, 'html.parser')
        data = soup.find('p', {'class': 'relations persons'})
        print(data.text)
        new.append(data.text)

    # Create the CSV file for the Searching keywords
    print("Data : ", my_dict['Name'])
    print("Data : ", my_dict['PersionLink'])
    print("second link :", second_link)
    print("new data  :", new)
    c2=pd.Series(data=my_dict['PersionLink'], name="Address")
    c3=pd.Series(data=my_dict['Name'], name="Name")
    c4=pd.Series(data=new, name="Author Name")
    data= pd.concat([ c2, c3, c4 ], axis=1) 
    data_frame=pd.DataFrame(data)
    print(data_frame)
    data_frame.to_csv('test.csv',index=False,mode='a',header=False, sep ='\t')
    # data_frame.to_csv('test.csv', index=False, mode='a', sep='\t')


def research_output(keywords):
    global my_dict, first_link, second_link, new, first_text, second_text, Profession1, Profession2
    my_dict = {"Name":[],"Address":[], "StartDate": [], "EndDate": [], "Profesion": [], "PersionLink": [], "OrgText": []}
    first_link = []  
    second_link = [] 
    first_text = []
    second_text = []
    Profession1 = []
    Profession2 = [] 
    new = []
    options = Options()

    # headless work with chrome driver
    options.headless = True

    #firsly You have downloaded chrome driver then You need to chrome driver path.
    driver = webdriver.Chrome("/home/hp/workspace/sanjeevupwork/matthew/chromedriver", options=options)

    driver.get('https://pureportal.coventry.ac.uk/en/publications/')

    # Delete all cookies of the chrome driver.
    driver.delete_all_cookies()

    # Chrome driver wait for the scrape data.
    time.sleep(5)

    # window maximize of chrome driver.
    driver.maximize_window()

    try:
        # click on the chrome driver cookies button and if the right path of the cookie button.
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[21]/div[3]/div/div[1]/div/div[2]/div/button[2]'))).click()
    except:
        pass

    # Enter the input box with keyword
    # driver.find_element_by_xpath('//*[@id="global-search-input"]').send_keys(Keys.ENTER)
    time.sleep(4)

    for n in range(1, 2):
        res = driver.page_source
        soup = BeautifulSoup(res, 'html.parser')
        data = soup.find('ul', {'class': 'list-results'})
        single_card = data.find_all('div', {'class': 'result-container'})

        for card in single_card:
            name = card.find('span')
            my_dict["Name"].append(name.text)
            
            name_link = card.find('h3', {'class': 'title'})
            persion_link = name_link.find('a', {'class': 'link'}).get('href')
            my_dict['PersionLink'].append(persion_link)
            second_link.append(persion_link)

            try:
                a_link = card.find('a', {'class': 'link person'})
                first_text.append(a_link.text)
                first_link.append(a_link.get('href'))
            except:
                first_text.append(" ")
                first_link.append(" ")

        time.sleep(5)
        num = 0
        num += n
        print(num)
        try:
            if num == 1:
                next_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="main-content"]/div/div[2]/nav/ul/li[13]/a')))
                next_button.click()
            elif num <= 2:
                next_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="main-content"]/div/div[2]/nav/ul/li[14]/a')))
                next_button.click()
            else:
                pass
            time.sleep(4)
        except:
            pass
    impo_link(second_link, new, my_dict)
        

@app.route('/results', methods=['POST', 'GET'])
def show_result():
    global my_dict, first_link, second_link, first_text, second_text, Profession1, Profession2, new
    link = []
    name = []
    details = []
    if request.method == "POST":
        if request.form.get('keywords'):
            keywords = request.form.get('keywords')
            # research_output(keywords)
            with open("result.csv") as csv_file:
                reader = csv.reader(csv_file)
                for line in reader:
                    if keywords in str(line):
                        a = line[0].split("\t")
                        print(a)
                        link.append(a[0])
                        name.append(a[1])
                        try:
                            if a[2]:
                                details.append(a[2])
                            else:
                                details.append(" ") 
                        except:
                            details.append(" ")
            return render_template('app/home.html', link=link, name=name, details=details, keywords=keywords, result=True)
    else:
        return redirect(url_for('main'))


# scheduler time function for the CronJob.
def data_scrap_csv():
    """
    This function work with time scheduler if you set the time then it is run on the time.
    """

    # Global variable for the store values like link, author name etc.
    global my_dict, first_link, second_link, new, first_text, second_text, Profession1, Profession2

    # this is dict variable
    my_dict = {"Name":[],"Address":[], "StartDate": [], "EndDate": [], "Profesion": [], "PersionLink": [], "OrgText": []}

    first_link = []  
    second_link = [] 
    first_text = []
    second_text = []
    Profession1 = []
    Profession2 = [] 
    new = []
    driver_url = "/home/hp/workspace/sanjeevupwork/matthew/chromedriver"

    # Options import then use the headless if you want to use another options like proxy You can use here.
    options = Options()

    options.headless = True

    driver = webdriver.Chrome(driver_url, options=options)

    driver.get('https://pureportal.coventry.ac.uk/en/publications/')

    # Delete the all cookies of the current page.
    driver.delete_all_cookies()

    # chrome driver page hold for the 5 sec.
    time.sleep(5)

    # Miximize the chrome driver window
    driver.maximize_window()

    # Click on the cookies button if right the xpath
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[22]/div[3]/div/div[1]/div/div[2]/div/button[2]'))).click()
    except:
        pass

    # Enter the search button with the attched with input field.
    # driver.find_element_by_xpath('//*[@id="global-search-input"]').send_keys(Keys.ENTER)

    # driver sleep for the 4 sec.
    time.sleep(4)
    
    for n in range(1, 10):

        # Current page get the source page.
        res = driver.page_source

        # Source page convert to the html with BS4
        soup = BeautifulSoup(res, 'html.parser')

        # Data get with the class attribute
        data = soup.find('ul', {'class': 'list-results'})
        single_card = data.find_all('div', {'class': 'result-container'})

        for card in single_card:
            name = card.find('span')
            my_dict["Name"].append(name.text)
            
            name_link = card.find('h3', {'class': 'title'})
            persion_link = name_link.find('a', {'class': 'link'}).get('href')
            my_dict['PersionLink'].append(persion_link)
            second_link.append(persion_link)

            try:
                a_link = card.find('a', {'class': 'link person'})
                first_text.append(a_link.text)
                first_link.append(a_link.get('href'))
            except:
                first_text.append(" ")
                first_link.append(" ")

        time.sleep(5)
        num = 0
        num += n
        print(num)
        try:
            if num == 1:
                next_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="main-content"]/div/div[2]/nav/ul/li[13]/a')))
                next_button.click()
            elif num <= 10:
                next_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="main-content"]/div/div[2]/nav/ul/li[14]/a')))
                next_button.click()
            else:
                pass
            time.sleep(4)
        except:
            pass

    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))
    print("Scheduler working Fine with Flask application!")
    impo_link(second_link, new, my_dict)


scheduler = BackgroundScheduler()
scheduler.add_job(func=data_scrap_csv, trigger="interval", minutes=20)
# scheduler.add_job(func=data_scrap_csv, trigger="interval", seconds=60)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


if __name__ == "__main__":
    app.run(debug=True)