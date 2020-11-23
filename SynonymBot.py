from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import InvalidSessionIdException
from time import sleep
import random
from Selenium_Info import selenium_path


class GetSynonymBot:

    synoList = []
    driverlocation = selenium_path
    print("Calling creation Method:")
    driver = webdriver.Chrome(driverlocation)

    def getSynonymn(self,searchWord):

        self.synoList = []

        if str(searchWord).__len__() < 3:
            return searchWord

        isUpperCase = False
        allUpperCase = False
        if not (str(searchWord).__getitem__(0).isupper()):
            isUpperCase = False
            print(searchWord+" is lower case.")
        elif (str(searchWord)).isupper():
            print(searchWord + " is in ALL CAPS.")
            allUpperCase = True

        else:
            print(searchWord + " begins with a capital letter.")
            isUpperCase = True

            self.driver.get("https://thesaurus.com/browse/" + searchWord)
        sleep(1)
        if str(self.driver.current_url).__contains__("misspelling") or str(self.driver.current_url).__contains__("noresult"):
            print("Given word: "+searchWord+" not found.")
            return searchWord
        elementsLocation = []
        elementsLocation = self.driver.find_element_by_xpath(
            '//*[@id="root"]/div/div/div[2]/main/section/section/div[2]/ul')
        self.synoList = elementsLocation.find_elements_by_class_name('etbu2a31')
        newString = ""
        for x in self.synoList:
            newString += str((x.get_attribute('outerText')) + "\n")
        if (newString == ''):
            return searchWord
        newList = []
        newList = str.splitlines(newString)
        newList.append(searchWord)
        randChance = newList.__len__()
        returnedString = newList.__getitem__(random.randint(0, randChance - 1))
        if bool(isUpperCase):
            return str(returnedString).capitalize()
        return returnedString

    def getSynonymnAdv(self,searchWord,partOfSpeech,specificityBetween1and3):

        self.synoList = []

        if str(searchWord).__len__() < 3:
            return searchWord

        isUpperCase = False
        allUpperCase = False
        if not (str(searchWord).__getitem__(0).isupper()):
            isUpperCase = False
            print(searchWord + " is lower case.")
        elif (str(searchWord)).isupper():
            print(searchWord + " is in ALL CAPS.")
            allUpperCase = True

        else:
            print(searchWord + " begins with a capital letter.")
            isUpperCase = True

        partOfSpeech = self.__formatPartOfSpeech(partOfSpeech,searchWord)
        try:
            self.driver.get("https://thesaurus.com/browse/" + searchWord)
        except InvalidSessionIdException:
            self.openBrowser()
        sleep(1)
        if str(self.driver.current_url).__contains__("misspelling") or str(self.driver.current_url).__contains__("noresult"):
            print("Given word: "+searchWord+" not found.")
            return searchWord

        numberOfTimestoTryAndFindPartOfSpeech = 10
        while(numberOfTimestoTryAndFindPartOfSpeech > 0):
            try:
                self.driver.find_element_by_xpath("//em[contains(text(), '" + str(partOfSpeech) + "')]").click()
                break
            except NoSuchElementException:
                print("Note: "+searchWord+" does not have an entry listed unter the following part of speech: "+partOfSpeech+".")
                #return searchWord
                break
            except ElementNotInteractableException:
                self.driver.find_element_by_class_name("css-15ap5rb-RightArrow").click()
                numberOfTimestoTryAndFindPartOfSpeech -= 1
            except ElementClickInterceptedException:
                self.driver.find_element_by_class_name("sailthru-overlay-close").click()
                #self.driver.execute_script("arguments[0].click", destroyme)
                #self.driver.find_element_by_class_name("bx-close-inside").click()
                numberOfTimestoTryAndFindPartOfSpeech -= 1

        elementsLocation = []
        try:
            elementsLocation = self.driver.find_element_by_xpath('//*[@id="root"]/div/div/div[2]/main/section/section/div[2]/ul')
        except NoSuchElementException:
            print("No Synonymns exist for "+searchWord +".")
            return searchWord

        self.synoList = elementsLocation.find_elements_by_class_name('eh475bn1')

        newString = ""
        if (type(specificityBetween1and3) is int):
            if (specificityBetween1and3 == 1):
                for x in self.synoList:
                    newString += str((x.get_attribute('outerText')) + "\n")
            elif (specificityBetween1and3 == 2):
                for x in self.synoList:
                    if (str(x.get_attribute('className')).__contains__('r5sw71')) or (str(x.get_attribute('className')).__contains__('1k3kgmb')):
                        newString += str((x.get_attribute('outerText')) + "\n")
            else:
                for x in self.synoList:
                    if (str(x.get_attribute('className')).__contains__('r5sw71')):
                        newString += str((x.get_attribute('outerText')) + "\n")
        if (newString == ''):
            print("Note: No synoymns found at specificity level "+str(specificityBetween1and3)+" for the word '"+searchWord+"'.")
            return searchWord
        newList = []
        newList = str.splitlines(newString)
        newList.append(searchWord)
        randChance = newList.__len__()
        returnedString = newList.__getitem__(random.randint(0, randChance - 1))
        if bool(isUpperCase):
            print("Synonymn " + returnedString + " chosen for the given word: " + searchWord + ".")
            return str(returnedString).capitalize()
        if bool(allUpperCase):
            print("Synonymn " + returnedString + " chosen for the given word: " + searchWord + ".")
            return str(returnedString).upper()
        print("Synonymn "+returnedString+" chosen for the given word: "+searchWord+".")
        return returnedString

    def printList(self):
        for x in self.synoList:
            print(x.get_attribute('outerText'))

    def __formatPartOfSpeech(self,unFormattedPartOfSpeechString,searchWord):
        unFormattedPartOfSpeechString = str(unFormattedPartOfSpeechString).lower()
        if unFormattedPartOfSpeechString.startswith("n"):
            return "noun"
        elif unFormattedPartOfSpeechString.startswith("v"):
            return "verb"
        elif unFormattedPartOfSpeechString.startswith("adj"):
            return "adj."
        elif unFormattedPartOfSpeechString.startswith("adv"):
            return "adv."
        elif unFormattedPartOfSpeechString.startswith("i"):
            return "interj."
        elif unFormattedPartOfSpeechString.startswith("p"):
            return "prep."
        elif unFormattedPartOfSpeechString.startswith("c"):
            return "conjuction"
        else:
            print(
                "ERROR: erroneous part of speech value entered for the word '" + searchWord + "'. '" + unFormattedPartOfSpeechString + "' is not a valid entry.")
            return unFormattedPartOfSpeechString

    def closeBrowser(self):
        self.driver.close()

    def openBrowser(self):
        self.driver = webdriver.Chrome(self.driverlocation)
