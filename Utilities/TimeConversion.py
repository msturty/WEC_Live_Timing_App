from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def DetermineCurrentEventSelected(configDictionary, currentEvent, logger):
    try:
        eventList = configDictionary["eventList"].split(',')
        eventList = [eventList.lower() for event in eventList]
        currentEvent = currentEvent.lower()
        for  event in eventList:
            if event in currentEvent:
                logger.info(f"Located event {event}")
                return event
        return False
    
    except Exception as e:
        logger.error(f"unable to parse event. {e}")
        return False

def DetermineTimeZone(currentEvent, logger):
    try:
        match currentEvent.lower():
            case "qatar":
                logger.info(f"Located {currentEvent}. Setting event time zone.")
                eventTimeZone = ZoneInfo("Asia/Qatar")
            case "imola":
                logger.info(f"Located {currentEvent}. Setting event time zone.")
                eventTimeZone = ZoneInfo("Europe/Rome")
            case "spa":
                logger.info(f"Located {currentEvent}. Setting event time zone.")
                eventTimeZone = ZoneInfo("Europe/Brussels")
            case "lone star le mans":
                logger.info(f"Located {currentEvent}. Setting event time zone.")
                eventTimeZone = ZoneInfo("America/Chicago")
            case "sao paulo":
                logger.info(f"Located {currentEvent}. Setting event time zone.")
                eventTimeZone = ZoneInfo("America/Sao_Paulo")
            case "le mans":
                logger.info(f"Located {currentEvent}. Setting event time zone.")
                eventTimeZone = ZoneInfo("Europe/Paris")
            case "fuji":
                logger.info(f"Located {currentEvent}. Setting event time zone.")
                eventTimeZone = ZoneInfo("Asia/Tokyo")
            case "bahrain":
                logger.info(f"Located {currentEvent}. Setting event time zone.")
                eventTimeZone = ZoneInfo("Asia/Bahrain")
            case "silverstone":
                logger.info(f"Located {currentEvent}. Setting event time zone.")
                eventTimeZone = ZoneInfo("Europe/London")
            case _:
                raise RuntimeError(f"Error seting timezone based off of input value {currentEvent}")
                            
        return eventTimeZone
    except Exception as e:
        logger.error(f"unable set timezone. {e}")
        return False
    
    

def FormatEventTime(eventTime, logger):
    try:
        #Sets the current year for date formatting
        currentYear = datetime.now().year
        
        #Set Month names for parsing month text to number value
        monthNames = {
            'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
            'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12
            }
        
        #Removes the extra text and splites the date and time part of the string
        eventTime = eventTime.replace('th', '').replace('st', '').replace('nd', '').replace('rd', '')
        date, time = eventTime.split(' / ')
        
        #Splits the month and day for the date variable
        month, day = date.split(' ')
        month = monthNames[month.lower()]
        day = int(day)

        #formats the time/date to make the string into a datetime object
        time = time.replace('h', ':')
        eventTime = f"{currentYear}-{month:02d}-{day:02d} {time}:00"
        eventTime = datetime.strptime(eventTime, '%Y-%m-%d %H:%M:%S')
        logger.info("Successfully parsed eventTime to a datetime object")
        return eventTime.strftime('%Y-%m-%d %H:%M:%S')
    
    except Exception as e:
        logger.error(f"Unable to parse the eventTime to a datetime object {e}")
        return False
        
    
def DetermineIfEventTimeNow(eventTimeZone, eventTime, logger):

    
    eventTime = datetime.strptime(eventTime, '%Y-%m-%d %H:%M:%S')
    localEventTime = eventTime.replace(tzinfo=eventTimeZone)
    localTime = datetime.now().astimezone()  
    minusOneHourLocalTime = localTime - timedelta(hours=1)
        
    # Check if the event has already passed by more than 1 hour in your local time zone
    if minusOneHourLocalTime <= localEventTime <= localTime:
        logger.info("Local time within 1 hour of the session start time.")
        return True
    elif localEventTime <= minusOneHourLocalTime:
        logger.info("Local time more than 1 hour of the session start time.")
        return False
    else:
        return False