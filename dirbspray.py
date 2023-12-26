import requests
import threading
import time
import random
import concurrent.futures

#My custom script for directory enumeration. Will make a version 2 w/ asynchronous requests

class Recon:
    def __init__(self,target):
        self.target = target
        self.progress = 0

    def Dirb(self,file):
        with open(file,"r") as Fuzz:
            for i in Fuzz:
                try:
                    time.sleep(0.5) #Prevent firewall rate limit block
                    directory = i.split("\n")
                    concatenated_text = ' '.join(directory)
                    command = self.target + "/" + concatenated_text 
                    response = requests.get(command)
                    content_length = response.headers.get('Content-Length')
                    if response.status_code == 404: #Change ur preferences here. If content length is bugging you
                        self.progress = self.progress + 1
                        
                    elif content_length is not None: 
                        print(f"Success: {command} - {str(response.status_code)} | {content_length} | Progress: {self.progress}") #WILDCARD
                        self.progress = self.progress + 1
                        

                except requests.ConnectionError: #Braking system in case of net failure
                    print("Internet goin nuts")
                    for i in range(1,60):
                        time.sleep(1)
        
        def Dirb_Auth(self):
            pass

URL = 'https://www.xvideos.com' #Change this to replace target with no / at the end

recon = Recon(URL)

spray = [ #Load your own files. 
    r"wordlist.txt",
    r"big.txt",
    r"directories.txt",
    r"common.txt",
    r"willdo.txt"
]        

#Update the lines below based on how many wordlists you are spraying.


with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Submit the tasks to the executor
    futures = [executor.submit(recon.Dirb, file) for file in spray]

    # Wait for all tasks to complete
    concurrent.futures.wait(futures)