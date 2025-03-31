from Utilities import StandardConfig
from Utilities import LoggingConfig
from Utilities import StandardEmail
from WebScrapers import WebInteractions
import os


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

    #Sets the outer loop for scrapping the WEC Live Timing page that handles opening the site and navigating to the appropriate live timing
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
            closeBrowser = WebInteractions.CloseWebPage(configDictionary, webDriver, logger)
            continue
        
        #Clicks the event in the current month on the WEC live timing page
        try:
            validateSuccess = WebInteractions.ClickEvent(configDictionary, webDriver, logger)
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
            eventTimeZone = validateSuccess = WebInteractions.DetermineSelectedEventTZ(configDictionary, webDriver, logger)
            if eventTimeZone == False:
                logger.error("Unable to determine event timezone")
                continue
            else:
                logger.info(f"Time zone located as {eventTimeZone}")
            
        except Exception as e:
            logger.error(f"Unable to determine the applicable session by time. {e}")
            continue

        #Clicks session if session time has started with the last hour
        try:
            validateSuccess = WebInteractions.ClickSessionIfActive(configDictionary, webDriver, logger, eventTimeZone)
            if validateSuccess == False:
                logger.error("Unable to find an active session")
                continue
            else:
                logger.info(f"Active session found")
            
        except Exception as e:
            logger.error(f"Unable to determine the applicable session by time. {e}")
            continue




if __name__ == "__main__":
    main()