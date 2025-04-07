import os
import xml.etree.ElementTree as ET
import datetime
import subprocess
import json

def CreateDictionary():
    """Loads an XML file and converts it into a dictionary."""
    try:

        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Config.xml")

        # Check if the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Error: The file '{file_path}' does not exist.")
        
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Convert XML to dictionary
        configDictionary = {child.tag: child.text for child in root}
        
        # Add the current year and month to the configDictionary
        currentYear = str(datetime.datetime.now().year)
        currentMonth = str(datetime.datetime.now().month - 2)
        configDictionary['currentYear'] = currentYear
        configDictionary['currentMonth'] = currentMonth
        
        
        monthNames = {
        '1': "january", '2': 'february', '3': 'march', '4': 'april', '5': 'may', '6': 'june',
        '7': 'july', '8': 'august', '9': 'september', '10': 'october', '11': 'november', '12': 'december'
        }
        
        configDictionary['currentMonthName'] = monthNames[configDictionary['currentMonth']]
        
        # Get values from the locker
        configDictionary = GetSecretKeys(configDictionary)
        
        
        return configDictionary

    except FileNotFoundError as e:
        print(e)
    except ET.ParseError as ParseError:
        print(f"Error: Failed to parse XML file '{file_path}'. Invalid XML format.\n{ParseError}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    return None  # Return None if an error occurs

def GetSecretKeys(configDictionary):
    
    # Doppler loads secrets into environment variables
    configDictionary["emailFrom"] = os.getenv("EMAIL_FROM")
    configDictionary["emailTo"] = os.getenv("EMAIL_TO")
    configDictionary["gmailPassword"] = os.getenv("GMAIL_PASSWORD")
    return configDictionary