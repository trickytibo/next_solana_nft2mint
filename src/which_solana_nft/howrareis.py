from encodings import utf_8
import requests
import os
from datetime import datetime
import os.path
import sys
import subprocess
import urllib3, sys, os, getopt, json, re
import operator
from which_solana_nft.twitterFollowersCount import *
import time
import shutil
from os.path import exists

class getDataFromhowrareis:
    """This class retrieves the content of the website Howrare.is,
    then copy it in a file in json format."""
    
    host='https://howrare.is/api/v0.1/drops'
    # Initialisation de la classe
    def __init__(self, file_howrareis, file_howareis_reformated):
        self.results_dir = 'www'
        self.file_howrareis = file_howrareis
        self.file_howareis_reformated = file_howareis_reformated
        
    def getDatafromHowrareis(self):
        """Retrieve data from howrare.is api."""
        try:
            headers = {'Accept': 'application/json', 'content-type': 'application/json'}
            r = requests.get(self.host, headers=headers)
            r_json = r.json()
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
           
        return r
    
    def copyRequests2file(self, entry, filedst):
        """Copy content to a file."""
        try:
            with open(self.results_dir + '/' + filedst, 'wb') as fd:
                for chunk in entry.iter_content(chunk_size=128):
                    fd.write(chunk)

        except ValueError as err:
            print(err)
            
        finally:
            fd.close()
            
    def extractData(self):
        """Extract Data from howrare.is, retrieve the number twitter followers and copy the results within a json file."""
        smallhowrareis = {}
        try:
            f = open(self.results_dir + '/' + self.file_howrareis, encoding="utf-8")
            data = json.load(f)
            
            for mydate in data['result']['data']:
                myday = []
                for myproject in data['result']['data'][mydate]:
                    # Get fields from json 
                    name = myproject['name']
                    utf8_name = name.encode(encoding = 'utf_8').decode()
                    twitter = myproject['twitter']
                    twitter_id = twitter.partition(".com/")[2]
                    utf8_twitter_id = twitter_id.encode(encoding = 'utf_8').decode()
                    # utf8_twitter_id = str(str(twitter_id).encode('utf8'))
                    discord = myproject['discord']
                    website = myproject['website']
                    price = myproject['price']
                    nft_count = myproject['nft_count']
                    # Get number of twitter followers 
                    twitter_followers = getFollowersCount(project=utf8_twitter_id)
                    
                    # Number of followers is forced to 0 If the requests failed (ex twitter account suspended)  
                    if twitter_followers.getCount():
                        try:
                            nb_twitter_followers = twitter_followers.getCount()[0]["followers_count"]
                        except KeyError:
                            continue
                            
                    else: 
                        nb_twitter_followers = 0
                    
                    # Verify that the variable nb_twitter_followers is an integer. If not, force to 0.   
                    if str(nb_twitter_followers).isdigit():
                        nb_twitter_followers = nb_twitter_followers
                    else:
                        nb_twitter_followers = 0
                        
                    # Reformate data with limited fields 
                    projectinfo = {'Name' : utf8_name, 'Website': website, 'Twitter Link': twitter, 'Twitter Followers': nb_twitter_followers, 'Discord Link': discord, 'Price': price, 'Number of items': nft_count}
                    myday.append(projectinfo)

                # Sort list according to dedicated field
                sorted_d = sorted(myday, key=operator.itemgetter('Twitter Followers'), reverse=True)
                smallhowrareis[mydate]=sorted_d
                
            pretty = json.dumps(smallhowrareis, indent=4)
                        
        except ValueError as err:
            print(err)
        
        finally:
            f.close()
        
        return smallhowrareis 

    def executeTask(self):
        myexecute = self.getDatafromHowrareis()

        # Create www directory if not exists
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

        self.copyRequests2file(entry=myexecute, filedst=self.file_howrareis)
        mydata = self.extractData()

        try:
            with open(self.results_dir + '/' + self.file_howareis_reformated, 'w') as myfile:
                json.dump(mydata, myfile)
                
        except ValueError as err:
            print(err)
            
        finally:
            myfile.close()
                
# r = getDataFromhowrareis()
# execute = r.executeTask()