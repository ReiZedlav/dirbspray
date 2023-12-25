import requests
import threading
import time

#Spam as many wordlist at you want w/ your target

class Recon:
    def __init__(self,target):
        self.target = target

    def Dirb(self,file):
        with open(file,"r") as Fuzz:
            for i in Fuzz:
                try:
                    command = self.target + "/" + i.strip()
                    response = requests.get(command)
                    if response.status_code == 404:
                        print(f"Failed: {command}")
                    else:
                        print(f"Valid: {command}")
                except ConnectionError:
                    print("Internet goin nuts")

URL = 'https://www.friv.com' #Change this to replace target with no / at the end

recon = Recon(URL)

spray = [ #If your file is outside your local folder, name it as exampled. C://path/path or D://path/path
    r"wordlist.txt",
    r"big.txt"
]        

#Update the lines below based on how many wordlists are you spraying.

first = threading.Thread(target=recon.Dirb,args=(spray[0],))
first.start()

second = threading.Thread(target=recon.Dirb,args=(spray[1],))
second.start()