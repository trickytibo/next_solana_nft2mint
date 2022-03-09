import requests
import os
from datetime import datetime
import os.path
import sys
import subprocess
import urllib3, sys, os, getopt, json, re


class UploadGrafanaDataToFile:
    """This class retrieves the content of a Grafana Host then copy it to a file.
        For this, you need to create an API token with at least Editor role."""
    
    # Initialisation de la classe
    def __init__(self, host, api_token, file='grafana_content.json'):
        self.host = host
        self.api_token = api_token
        self.file = file
        
    def getData(self):
        """Retrieve data from grafana api."""
        try:
            headers = {'Authorization': 'Bearer ' + self.api_token}
            r = requests.get(self.host + '/api/search?query=%', headers=headers)
            r_json = r.json()
            r.raise_for_status()
            data = r.json()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
           
        return r
    
    def copy2file(self, entry):
        """Copy content to a file."""
        try:
            with open(self.file, 'wb') as fd:
                for chunk in entry.iter_content(chunk_size=128):
                    fd.write(chunk)
        except ValueError as err:
            print(err)
        finally:
            fd.close()
            
    def executeTask(self):
        myexecute = self.getData()
        self.copy2file(myexecute)
            
# headers = {'Accept': 'application/json', 'content-type': 'application/json', 'Authorization': 'Bearer ' + self.api_token}
                
            
# r = requests.get('https://httpbin.org/basic-auth/user/pass', auth=('user', 'pass'))
# >>> r.status_code
# 200
# >>> r.headers['content-type']
# 'application/json; charset=utf8'
# >>> r.encoding
# 'utf-8'
# >>> r.text
# '{"authenticated": true, ...'
# >>> r.json()
# {'authenticated': True, ...}


# class getGrafanaData:
#     """This class creates a chorus singer that
#         can sing one of two lines."""
#     line1 = "Ma Ma Mia"
#     line2 = "let me GO !"
#     def getData(self, line):
#         """This function sings one of 2 lines"""
#         if line == 1:
#             print(self.line1)
#         else:
#             print(self.line2)