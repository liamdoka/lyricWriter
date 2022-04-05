from selenium import webdriver
from time import sleep
import nltk
import syllables
import re
import json


FACEBOOK_USERNAME = ""
FACEBOOK_PASSWORD = ""


def BinarySearch(lys, val):
    first = 0
    last = len(lys)-1
    index = -1
    while (first <= last) and (index == -1):
        mid = (first+last) // 2
        if lys[mid][0] == val:
            index = mid
        else:
            if val < lys[mid][0]:
                last = mid - 1
            else:
                first = mid + 1
    return index

class FacebookBot():
    def __init__(self):
        options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        options.headless = True
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(options=options)

    def login(self):
        self.driver.get('https://facebook.com')
        email_in = self.driver.find_element_by_xpath('//*[@id="email"]')
        email_in.send_keys(FACEBOOK_USERNAME)

        pass_in = self.driver.find_element_by_xpath('//*[@id="pass"]')
        pass_in.send_keys(FACEBOOK_PASSWORD)

        login_btn = self.driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div/div/div[2]/div/div[1]/form/div[2]/button')
        login_btn.click()

    def nav(self):
        self.driver.get('https://facebook.com/UoMLoveLetters')
        sleep(6)
        print(self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div[2]/div/div/div/div[2]/div/div/div[1]/h2/span/span').text)

        lst = []
        for idx in range(80):
            try:
                post = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div[2]/div/div[2]/div[2]/div/div/div[2]/div[' + str(2 + idx) + ']/div/div/div/div/div/div/div/div/div/div[2]/div/div[3]')
            except:
                self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                sleep(2)               
                post = self.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[4]/div[2]/div/div[2]/div[2]/div/div/div[2]/div[' + str(2 + idx) + ']/div/div/div/div/div/div/div/div/div/div[2]/div/div[3]')
            finally:
                if post.text[-8:] == "See more":
                    btn = post.find_elements_by_tag_name('div')
                    btn[-1].click()
                

                # Split when you run into any of these "[!:;?,.\n]"
                strings = re.split("[!:;?,.\n]", post.text.lower())
                
                
                lst.append(strings)
                #print(idx, post.text)

        return lst


bot = FacebookBot()
bot.login()
sleep(2)
lst = bot.nav()

sentences = []
for item in lst:
    bruh = [sentence.strip() for sentence in item[1:] if len(sentence.strip()) != 0]
    sentences += bruh
    #print(bruh)


entries = nltk.corpus.cmudict.entries()
data = []
for item in sentences:
    x = entries[BinarySearch(entries, item.split()[-1])]
    sentence_len = sum([syllables.estimate(word) for word in item.split()])
    if x[0] != "zywicki":
        data.append([item, sentence_len, x])

with open('data.json', 'w') as outfile:
    json.dump(data, outfile)

bot.driver.quit()