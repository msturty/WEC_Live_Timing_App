"""
Contains all the functions for interacting with a webpage
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
from Utilities import TimeConversion


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
        webDriver["webDriver"].quit()
        return True

    except Exception as e:
        logger.error("Unable to close the webpage")
        return False



"""
Clicks the event on WEC Live Timing page based on the current month
"""
def ClickEvent(configDictionary, webDriver, logger):
    try:
        for i in range(int(configDictionary["numberOfEvents"])):
            aTagElement = i + 1
            element = webDriver["webDriver"].find_element(By.XPATH, f"/html/body/div/div/div/div[2]/div/div[2]/div/a[{aTagElement}]/div[2]/div[2]/div")
            innerHTML = element.get_attribute("innerHTML")
            if configDictionary["currentMonth"] in innerHTML:
                element.click()
                logger.info(f"Clicking Event number {i} of {configDictionary["numberOfEvents"]}")
                return True
    except Exception as e:
        logger.error(f"Unable to click the event. {e}")
        return False
    
    
    
"""
Clicks the event on WEC Live Timing page based on the time of the session start current time zone
"""          
def DetermineSelectedEventTZ(configDictionary, webDriver, logger):
    try:
        while 1 == 1:
            i += i
            element = webDriver["webDriver"].find_element(By.XPATH, f"/html/body/div/div/div/div[1]/div[1]/div[1]/div[1]/span")
            innerHTML = element.get_attribute("innerHTML")
            formattedEventName = TimeConversion.DetermineCurrentEventSelected(configDictionary, innerHTML, logger)
            if formattedEventName == False:
                raise RuntimeError("Event not not found. Unable to format.")
            timeDifference = TimeConversion.DetermineCurrentEventSelected(configDictionary, formattedEventName, logger)
            if timeDifference == False:
                raise RuntimeError("Time difference not calculated.")
            
            
    except Exception as e:
        logger.error(f"Unable to determine time of current event. {e}")
        return False




def ClickSession(configDictionary, webDriver, logger):
    try:
        for i in range(int(configDictionary["numberOfEvents"])):
            aTagElement = i + 1
            element = webDriver["webDriver"].find_element(By.XPATH, f"/html/body/div/div/div/div[2]/div/div[2]/div/a[{aTagElement}]/div[2]/div[2]/div")
            innerHTML = element.get_attribute("innerHTML")
            if configDictionary["currentMonth"] in innerHTML:
                element.click()
                logger.info(f"Clicking Event number {i} of {configDictionary["numberOfEvents"]}")
                return True
    except Exception as e:
        logger.error(f"Unable to click the element. {e}")
        return False