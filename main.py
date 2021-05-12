# THIS PROGRAM SENDS YOU AN EMAIL WITH THE COVID NUMBERS OF THE WORLD AND OF INDIA
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from email.mime.multipart import MIMEMultipart
import time
import smtplib
from email.mime.text import MIMEText
import os

while True:

    def init():
        path = "" #path of directory in which chromedriver.exe is located

        driver = selenium.webdriver.Chrome(path)

        driver.get("https://www.worldometers.info/coronavirus/")

        driver.implicitly_wait(15)

        return driver


    def grab():

        driver = init()

        total_cases = driver.find_element_by_xpath('//*[@id="maincounter-wrap"]/div/span')
        print("Total cases:",total_cases.text)

        total_death = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div/div/div[6]/div/span')
        print("Total deaths:",total_death.text)

        total_recovered = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[1]/div/div[7]/div/span')
        print("Total recovered:", total_recovered.text)

        india_cases = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div/div[6]/div[1]/div/table/tbody[1]/tr[7]/td[3]')
        print("India total cases:", india_cases.text)

        india_deaths = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div/div[6]/div[1]/div/table/tbody[1]/tr[7]/td[5]')
        print("India total deaths:", india_deaths.text)

        india_recovered = driver.find_element_by_xpath('/html/body/div[3]/div[3]/div/div[6]/div[1]/div/table/tbody[1]/tr[7]/td[7]')
        print("India total recovered:", india_recovered.text)

        return total_cases, total_death, total_recovered, india_cases, india_deaths, india_recovered, driver


    def store_in_file():

        ret_grab = grab()

        # storing data in text file
        file = open("covid.txt", "w+")
        file.write("Worldwide Total Cases: ")
        file.write(ret_grab[0].text)
        file.write(" ")
        file.write(", Worldwide Total Deaths: ")
        file.write(ret_grab[1].text)
        file.write(" ")
        file.write(", Worldwide Total Recovered: ")
        file.write(ret_grab[2].text)
        file.write(" ")
        file.write(", India Total Cases: ")
        file.write(ret_grab[3].text)
        file.write(" ")
        file.write(", India Total Deaths: ")
        file.write(ret_grab[4].text)
        file.write(" ")
        file.write(", India Total Recovered: ")
        file.write(ret_grab[5].text)
        file.close()

        return ret_grab[6]


    def send_message():

        driver = store_in_file()

        msg = MIMEMultipart('alternative')
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.connect('smtp.gmail.com', 587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login('sampleprogrammingemail@gmail.com', 's4mpl3progr4mming3mail') # a sample email account I made for this program

        to_email, from_email = '', 'sampleprogrammingemail@gmail.com' # add the receiving email in the first empty single quotes
        msg['Subject'] = 'subject'
        msg['From'] = from_email
        body = 'This is your daily Covid - 19 update! Click on the attachment to view'

        filename = "covid.txt"
        f = open('covid.txt', 'r+')
        attachment = MIMEText(f.read())
        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(attachment)

        content = MIMEText(body, 'plain')
        msg.attach(content)
        s.sendmail(from_email, to_email, msg.as_string())

        return driver


    def destroy():
        driver = send_message()
        driver.quit()


    def delete_file():
        file_name = 'covid.txt'

        location = "" # location of file to delete. currently the txt file is in the same directory, so the current config i.e. "" should automatically delete the file 

        path = os.path.join(location, file_name)

        os.remove(path)

    destroy()
    delete_file()

    time.sleep(60 * 60 * 24) # CHANGE THIS VALUE (IN SECONDS) IN THE BRACKET TO SET HOW FREQUENTLY YOU WANT THE PROGRAM TO UPDATE YOU
