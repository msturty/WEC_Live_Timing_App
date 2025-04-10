from Utilities import StandardConfig
from Utilities import LoggingConfig
from Utilities import StandardEmail
from Utilities import DataProcessing
from WebScrapers import WebInteractions
import os
import time
import copy


def main():

    #Initialize Config Dictionary and validate
    try:
        configDictionary = StandardConfig.CreateDictionary()
        logger = LoggingConfig.LogToFile(configDictionary)
        logger.info("Initialized configDictionary")


    except Exception as e:
        logger.error(f"Unable to initialize configDictionary | {e}")
        configDictionary = {"smtpServer":"smtp.gmail.com",
                            "smtpPort" : 587, 
                            "applicationName":"WEC_Live_Timing_APP",
                            "emailPassword":os.getenv("GMAIL_PASSWORD"),
                            "emailFrom":os.getenv("EMAIL_FROM"),
                            "emailTo":os.getenv("EMAIL_TO")}
        StandardEmail.SendGmail(message = f"Unable to initialize configDictionary | {e}",
                                subject = "WEC Live Timing App - Critical",
                                **configDictionary)
        exit()

    #Sets the outer loop for scrapping the WEC Live Timing page that handles opening the site and navigating to the appropriate live timing event
    continueLoop = True
    loopCounter = 0
    while continueLoop == True:
        loopCounter += 1
        logger.info(f"Attempt number {loopCounter} to run {configDictionary["applicationName"]}")
        if loopCounter == 4:
            logger.critical(f"Attempted to run web scrapping 3 tiems and failed. Stopping {configDictionary["applicationName"]}.")
            StandardEmail.SendGmail(message = "Attempted to run web scrapping 3 times and failed. Stopping the process.",
                                    subject = f"Fatal Error Running {configDictionary["applicationName"]}",
                                    **configDictionary)
            break
        
        #Opens the WEC live timing web page
        try:
            webDriver = WebInteractions.OpenWebPage(configDictionary, logger)
            if configDictionary["currentYear"] in webDriver["windowTitle"]:
                logger.info(f"Opened web browser and navigated to site")
            else:
                raise ValueError("The window title is not valid")
        except Exception as e:
            logger.error(f"Unable to open web browser or navigate to site | {e}")
            WebInteractions.CloseWebPage(configDictionary, webDriver["webDriver"], logger)
            continue
        
        #Clicks the event in the current month on the WEC live timing page
        try:
            validateSuccess = WebInteractions.ClickEvent(configDictionary, webDriver["webDriver"], logger)
            if validateSuccess == True:
                logger.info(f"Navigated to Live Timing")
            else:
                logger.error(f"Unable to navigate to Live Timing.")
                continue
            
        except Exception as e:
            logger.error(f"Unable to click the event | {e}")
            continue
            
        
        #Determines the timezone of the current event    
        try:
            eventTimeZone = validateSuccess = WebInteractions.DetermineSelectedEventTZ(configDictionary, webDriver["webDriver"], logger)
            if eventTimeZone == False:
                logger.error("Unable to determine event timezone")
                continue
            else:
                logger.info(f"Time zone located as {eventTimeZone}")
            
        except Exception as e:
            logger.error(f"Unable to determine the applicable session by time | {e}")
            continue

        #Clicks session if session time has started within the last hour and validates to traversal to live timing
        try:
            validateSuccess = WebInteractions.ClickSessionIfActive(configDictionary, webDriver["webDriver"], logger, eventTimeZone)
            if validateSuccess == False:
                logger.error("Unable to find an active session")
                continue
            else:
                logger.info(f"Active session found")
            
        except Exception as e:
            logger.error(f"Unable to determine the applicable session by time | {e}")
            continue
    
    errorCount = 0
    countAfterFinish = 0
    
    try:
        if  currentLiveTiming is not None:
            logger.info("currentLiveTiming variable is initialized")
    except NameError as ne:
        logger.warning("Creating dictionary currentLiveTiming as it is not initialized")
        currentLiveTiming = {}
        
    while True:
        try:
            if errorCount == 2:
                logger.error("Error extracting session data")
                WebInteractions.CloseWebPage(configDictionary, webDriver["webDriver"], logger)
                break
            if sessionParamaters["sessionStatus"] == "finish":
                countAfterFinish = countAfterFinish + 1
                if countAfterFinish == 6:
                    continueLoop = False
                    break
            
            lastLiveTiming = copy.deepcopy(currentLiveTiming)
            
            currentLiveTiming = WebInteractions.ExtractLiveTimingTable(configDictionary, webDriver["webDriver"], logger)
            if currentLiveTiming == False:
                logger.error("Unable to extract live timing data from site")
                errorCount = errorCount + 1
                continue
            else: 
                logger.info("Extracted live timing table")
                
        
            sessionParamaters = WebInteractions.ExtractSessionParamaters(configDictionary, webDriver["webDriver"], logger)
            if sessionParamaters == False:
                logger.error("Unable to capture session paramaters")
                errorCount = errorCount + 1
                continue
            else: 
                logger.info("Extracted session paramaters")
            
            
            newLiveTiming = DataProcessing.CreateAndCompareDictionary(currentLiveTiming, lastLiveTiming, logger)
            if newLiveTiming == False:
                logger.error("Unable to parse live timing")
                errorCount = errorCount + 1
                continue
            else: 
                logger.info("Extracted session paramaters")
            
            
            
            
            errorCount = 0
        except Exception as e:
            logger.error(f"Unable to capture session paramaters| {e}")
            continue
        
        #Compares the last scrape to the current scrape and outputs only the data that has changed
        
        
        #Inserts the new data into the db
        
        
        
        time.sleep(int(configDictionary["extraLongDelay"]))
if __name__ == "__main__":
    main()