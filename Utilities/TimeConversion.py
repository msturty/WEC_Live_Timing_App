from datetime import datetime, timezone, timedelta

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
        logger.error("unable to parse event. {e}")
        

def ConvertEventTimeToLocal(currentEvent, logger):
    match currentEvent:
        case "qatar":
            gmtOffset = 3
        case "imola":
            gmtOffset = 1
        case "spa":
            gmtOffset = 1
        case "lone star le mans":
            gmtOffset = - 6
        case "sao paulo":
            gmtOffset = - 3
        case "le mans":
            gmtOffset = 1
        case "fuji":
            gmtOffset = 9
        case "bahrain":
            gmtOffset = 3
        case "silverstone":
            gmtOffset = 0
    gmtSystemOffset = datetime.now().astimezone().tzinfo
    gmtSystemOffset = datetime.now(gmtSystemOffset)
    gmtSystemOffset = gmtSystemOffset.utcoffset
    print(gmtOffset)
    print(gmtSystemOffset)
    input("wait")
    eventTime = timezone(timedelta(hours=gmtOffset))
    systemTime= timezone(timedelta(hours=gmtSystemOffset))
    
currentEvent = "qatar"
logger = ""
ConvertEventTimeToLocal(currentEvent, logger)