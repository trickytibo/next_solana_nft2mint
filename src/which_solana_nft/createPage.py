from encodings import utf_8
import requests
import os
from datetime import datetime
import os.path
import sys
import subprocess
import urllib3, sys, os, getopt, json, re
import operator
import time
from json2html import *

class createHtmlPagefromJSON:
    """This class build a html page from json file."""
    
    # Initialisation de la classe
    def __init__(self, inputfile, nbElements2display, period2parse):
        self.inputfile = inputfile
        self.results_dir = 'www'
        self.dst_file = 'index.htm'
        self.nbElements2display = nbElements2display
        self.period2parse = period2parse
        
    def buildHtmlPage(self):
        """Build html page from json file."""
        
        f = open(self.results_dir + '/' + self.inputfile)
        data = json.load(f)

        smallhowrareis = {}
        for x in list(data)[0:self.period2parse]:
            myday = []

            # Verify that the number of nft released is above the number of elements asked. 
            if len(data[x]) > self.nbElements2display:
                self.nbElements2display = self.nbElements2display
            else: 
                self.nbElements2display = len(data[x])

            # 
            for i in range(self.nbElements2display):
                myday.append(data[x][i])
            f.close()
            
            smallhowrareis[x]=myday
        
        template = {'<>':'div','class':'card','html':[
                    {'<>':'img','alt':'this is our logo','src':'logo.jpg'},
                    {'<>':'p','text':'Welcome to json2html!'}
                ]};
        
        table_attributes = {"class": 'table table-striped" border="1" style="border: 1px solid #000000; border-collapse: collapse;" cellpadding="4" id="data'}
        
        r = json2html.convert(json = smallhowrareis, 
                         table_attributes=table_attributes)
        
        with open(self.results_dir + '/' + self.dst_file, 'w') as webpage:
            json.dump(r, webpage)
        webpage.close()

# r = createHtmlPagefromJSON(file='www/howrareis_reformated.json', nbElements2display='10', period2parse='9')
# r.buildHtmlPage()