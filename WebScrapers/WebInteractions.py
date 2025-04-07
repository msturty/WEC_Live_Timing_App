"""
Contains all the functions for interacting with a webpage
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Utilities import TimeConversion
import time
from bs4 import BeautifulSoup


"""
Opens the web page found using Chrome and Selenium to the openingURL key
"""
def OpenWebPage(configDictionary, logger):
    try:
        # Set up ChromeOptions
        options = Options()
        options.binary_location = configDictionary["chromeBrowser"] 

        # Specifies the path to the chrome driver and initializes it
        service = Service(configDictionary["chromeWebDriver"])
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()
        
        # Opens the webbrowser at the page specified in the config
        driver.get(configDictionary["openingURL"])
        return {"windowTitle" : driver.title, "webDriver" : driver}
    
    except Exception as e:
        logger.error(f"Unable to open web browser at specified URL | {e}")


"""
Closes a Selenium session by passing in the current session selenium driver details
"""
def CloseWebPage(configDictionary, webDriver, logger):
    try:
        
        # Wait for 5 seconds to see the browser
        time.sleep(int(configDictionary["longDelay"]))
        webDriver.quit()
        return True

    except Exception as e:
        logger.error(f"Unable to close the webpage | {e}")
        return False



"""
Clicks the event on WEC Live Timing page based on the current month
"""
def ClickEvent(configDictionary, webDriver, logger):
    try:
        WebDriverWait(webDriver, configDictionary["longDelay"]).until(
            lambda webDriver: webDriver.execute_script("return document.readyState") == "complete")
        for i in range(int(configDictionary["numberOfEvents"])):
            aTagElement = i + 1
            element = webDriver.find_element(By.XPATH, f'//*[@id="body"]/div/div/div/div[2]/div/div[2]/div/a[{aTagElement}]/div[2]/div[2]')
            innerHTML = element.get_attribute("innerHTML").lower()
            logger.info(f"Checking innger HTML value {innerHTML} for a match with {configDictionary["currentMonthName"]} on event number {aTagElement}")
            if configDictionary["currentMonthName"] in innerHTML:
                element.click()
                logger.info(f"Clicking Event number {i} of {configDictionary["numberOfEvents"]}")
                return True
    except Exception as e:
        logger.error(f"Unable to click the event | {e}")
        return False
    
"""
Clicks the event on WEC Live Timing page based on the time of the session start current time zone
"""          
def DetermineSelectedEventTZ(configDictionary, webDriver, logger):
    try:
        time.sleep(int(configDictionary["longDelay"]))
        WebDriverWait(webDriver, 10).until(
            lambda webDriver: webDriver.execute_script("return document.readyState") == "complete")
        element = webDriver.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div[1]/div[1]/div[1]')
        innerHTML = element.get_attribute("innerHTML").lower()
        logger.info(f"checking element {innerHTML}")
        formattedEventName = TimeConversion.DetermineCurrentEventSelected(configDictionary, innerHTML, logger)
        if formattedEventName == False:
            raise RuntimeError("Event not not found. Unable to format.")
        eventTimeZone = TimeConversion.DetermineTimeZone(formattedEventName, logger)
        if eventTimeZone == False:
            raise RuntimeError("Time Zone not calculated.")
        return eventTimeZone
            
    except Exception as e:
        logger.error(f"Unable to determine time of current event | {e}")
        return False


"""
Clicks the event if the event start is within 1 hour of the current time
"""
def ClickSessionIfActive(configDictionary, webDriver, logger, eventTimeZone):
    try:
        WebDriverWait(webDriver, configDictionary["longDelay"]).until(
            lambda webDriver: webDriver.execute_script("return document.readyState") == "complete")
        i = 0
        while 1 == 1:
            #loops through the available sessions and gets the inner HTML
            i = i + 1
            aTagElement = i + 1
            element = webDriver.find_element(By.XPATH, f'/html/body/div/div/div/div[1]/div[2]/div/div/div[{aTagElement}]/a/div[2]')
            
            #parses and extracts the inner HTML by removing the HTML tags and white space
            innerHTML = element.get_attribute("innerHTML")
            innerHTML = BeautifulSoup(innerHTML, "html.parser")
            innerHTML = innerHTML.get_text()
            formattedInnerHTML = innerHTML.replace('\n', '').replace(' ', '')
            
            #formats the event time into a datetime object
            formattedEventTime = TimeConversion.FormatEventTime(formattedInnerHTML, logger)
            if formattedEventTime == False:
                raise ValueError("Event time not formatted.")
            
            #compares the event time to the current time and clicks the active session
            eventFound = TimeConversion.DetermineIfEventTimeNow(configDictionary ,eventTimeZone, formattedEventTime, logger)
            if eventFound == True:
                element.click()
                time.sleep(int(configDictionary["longDelay"]))
                navigatedToLiveTiming = ValidateLiveTimingActive(webDriver, logger)
                if navigatedToLiveTiming == True:
                    return True
                else:
                    raise RuntimeError("Unable to navigate to the live timing site")
                
    except Exception as e:
        logger.error(f"Unable to click the element and navigate to live timing | {e}")
        return False


"""
Validates if the live timing screen is currently displayed
"""
def ValidateLiveTimingActive(configDictionary, webDriver, logger):
    try:
        time.sleep(int(configDictionary["longDelay"]))
        WebDriverWait(webDriver, 10).until(
            lambda webDriver: webDriver.execute_script("return document.readyState") == "complete")
        element = webDriver.find_element(By.XPATH, f'//*[@id="livePage"]/div[1]/div[2]/div[2]/div[1]/div/div/div[2]/div[1]/div/div[1]/div[1]')
        innerHTML = element.get_attribute("innerHTML")
        if innerHTML.lower() == "wind":
            return True
        
    except Exception as e:
        logger.error(f"Unable to validate traversal to live timing page | {e}")
        return False
    

"""
Extracts the contents of the live timing table
"""
def ExtractLiveTimingTable(configDictionary, webDriver, logger):
    try:
        WebDriverWait(webDriver, configDictionary["longDelay"]).until(
        lambda webDriver: webDriver.execute_script("return document.readyState") == "complete")
        
        element = webDriver.find_element(By.XPATH, '/html/body/div/div[1]/div[2]/div[2]/div[2]/div[2]/table')
        innerHTML = element.get_attribute('innerHTML')
        
        table = BeautifulSoup(innerHTML, 'lxml')
        table = table.find('table')
        
        headers = [th.get_text(strip=True) for th in table.select('thead th')]
        
        data = []
        for row in table.select('tbody tr'):
            cells = [td.get_text(strip=True) for td in row.select('td')]
            if cells:
                row_dict = dict(zip(headers, cells))
                #data.append(row_dict) 
        
    except Exception as e:
        logger.error(f"Error Extracting Live Timing Table | {e}")
        return False