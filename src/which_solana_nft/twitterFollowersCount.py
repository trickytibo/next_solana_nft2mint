import requests
import os
from datetime import datetime
import os.path
import sys
import subprocess
import urllib3, sys, os, getopt, json, re

class getFollowersCount:
    """This class retrieves the number of twitter followers per project."""
    
    # curl https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names=Alphawolf01122
    # Initialisation de la classe
    def __init__(self, project):
        self.host = 'https://cdn.syndication.twimg.com'
        self.project = project
        
    def getCount(self):
        """Retrieve data from grafana api."""
        try:
            headers = {'Accept': 'application/json', 'content-type': 'application/json'}
            mycount = requests.get(self.host + '/widgets/followbutton/info.json?screen_names=' + self.project, headers=headers)
            r_json = mycount.json()
            mycount.raise_for_status()
            data = mycount.json()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
            
        return r_json

# Add an element to a dictionnary
class addDataIntoDict:
    """This class add an entry to a dictionnary."""
    def __init__(self, project, data):
        self.project = project
        self.data = data
        self.my_dict = {} 
        
    # Create a new entry to the dictionnary with project name and twitter followers count
    def fillDict(self):
        # Extract followers_count to the data
        getFollowers_count = self.data[0]
        followers_count = getFollowers_count['followers_count']
        # Add an entry to dict 
        self.my_dict[self.project] = followers_count
        return self.my_dict