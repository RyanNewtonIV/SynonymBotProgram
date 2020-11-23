from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.common.action_chains import ActionChains

from time import sleep
from selenium.webdriver.common.keys import Keys
from Selenium_Info import selenium_path

class GetPartsOfSpeechBot:


    driverlocation = selenium_path
    driver = webdriver.Chrome(driverlocation)

    def returnPartsOfSpeechList(self,stringToCheck):

        try:
            self.driver.get("https://parts-of-speech.info/")
        except InvalidSessionIdException:
            self.openBrowser()
            self.driver.get("https://parts-of-speech.info/")

        partsOfSpeechList = []
        sleep(1)
        textBox = self.driver.find_element_by_id('text')
        textBox.click()
        ActionChains(self.driver) \
            .key_down(Keys.CONTROL) \
            .key_down('a') \
            .perform()
        textBox.send_keys(Keys.BACKSPACE)
        textBox.send_keys(stringToCheck)
        self.driver.find_element_by_id('submit').click()
        secondsWaited = 0
        textContainer = ""
        taggedSentenceElements = ""
        while (secondsWaited < 30):
            try:
                textContainer = self.driver.find_element_by_id("textTagged")
                taggedSentenceElements = textContainer.find_elements_by_tag_name("span")
                if (taggedSentenceElements != []):
                    break
                else:
                    print("Waiting " + str(secondsWaited) + " second(s) for text to be analyzed.")
                    sleep(1)
                    secondsWaited += 1
            except NoSuchElementException:
                print("Waiting "+str(secondsWaited+1)+" second(s) for text to be analyzed.")
                sleep(1)
                secondsWaited += 1

        if secondsWaited >= 30:
            print("CRITICAL ERROR: Given Text could not be analyzed")
            return



        for x in taggedSentenceElements:
            wordAndPartOfSpeechList = []
            wordAndPartOfSpeechList.append(str(x.get_attribute("innerText")))
            if str(wordAndPartOfSpeechList[0]) == "n't":
                wordAndPartOfSpeechList[0] = "not"
            wordAndPartOfSpeechList.append(self.checkTagName(x.get_attribute("className")))
            partsOfSpeechList.append(wordAndPartOfSpeechList)

        self.driver.close()
        return partsOfSpeechList

    def checkTagName(self,stringToCheck):
        if "Determiner" in stringToCheck:
            return "determiner"
        elif "Other" in stringToCheck:
            return "other"
        elif "Noun" in stringToCheck:
            return "noun"
        elif "Pronoun" in stringToCheck:
            return "pronoun"
        elif "Verb" in stringToCheck:
            return "verb"
        elif "Preposition" in stringToCheck:
            return "preposition"
        elif "Adjective" in stringToCheck:
            return "adjective"
        elif "Adverb" in stringToCheck:
            return "adverb"
        elif "Conjunction" in stringToCheck:
            return "conjunction"
        elif "Number" in stringToCheck:
            return "number"
        else:
            return "ERROR"

    def closeBrowser(self):
        self.driver.close()

    def openBrowser(self):
        self.driver = webdriver.Chrome()