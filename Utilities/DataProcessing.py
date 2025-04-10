

def CreateAndCompareDictionary(currentLiveTiming, lastLiveTiming, logger):
    try:
        newLiveTiming = []
        for key in currentLiveTiming:
            for key2 in lastLiveTiming:
                if key["#"] == key2["#"]:
                    if key["Laps"] != key2["Laps"]:
                        newLiveTiming.append(key)
                    break
        return newLiveTiming
    
    except Exception as e:
        logger.error(f"Unable to create new dictionary for database insertion | {e}")
        return False