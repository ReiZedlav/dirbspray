import asyncio
import httpx
import concurrent.futures
import random
from fake_useragent import UserAgent
import time

#Modification required as diff websites can have custom status codes for an empty page

#Check status code first

class Recon:
    def __init__(self, target):
        self.target = target
        self.counter = 0
        self.limit = [0,0, 0.50,0.50,0.50,0.50,0.50,0.35,0.35,0.35,0.10,0.10]  # Random speed bumps
        self.check = 555
        self.cookies = {
            # Test: Null
        }

    async def dirb(self, chunk):
        async with httpx.AsyncClient() as client:
            try:
                for i in chunk:
                    RNG = random.randint(1, 1000)
                    random_bump = random.choice(self.limit)
                    time.sleep(random_bump)  # imitate a human making requests at random intervals
                    directory = i.strip()
                    user_agents = {  # Randomizes per iterations
                        'User-Agent': UserAgent().random
                    }
                    command = f"{self.target}/{directory}"
                    response = await client.get(command, timeout=None, cookies=self.cookies, headers=user_agents)
                    content_length = response.headers.get('Content-Length')
                    if response.status_code == 429:  # Rate limit detect. Subject to debug
                        print("Rate limited! Need script adjustments!")
                        self.counter += 1
                    elif response.status_code != 404 and content_length is not None and int(content_length) != 0:
                        print(f"Success: {command} | Status Code: {response.status_code} Size: {content_length} | Progress: {self.counter} | Speed: {random_bump}")
                        self.counter += 1
                    else:
                        self.counter += 1
                        if RNG == self.check:
                            print(f"Progress: {self.counter}")
                        #print(f"Troubleshoot: {command}")  #comment if working fine

            except Exception as e:
                print(f"Something went wrong: {e}")

    def process_file(self, file, chunk_size=400):
        with open(file, "r") as Fuzz:
            while True:
                chunk = [next(Fuzz, None) for _ in range(chunk_size)]
                chunk = [item.strip() for item in chunk if item is not None]
                if not chunk:
                    break
                for i in range(0, len(chunk), 5):  # Iterate through 5 lines at a time
                    asyncio.run(self.dirb(chunk[i:i+5]))

    def process_files(self, files, chunk_size=400):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(self.process_file, files, [chunk_size] * len(files))

def main():
    URL = "https://www.tiktok.com"  # Set target
    recon = Recon(URL)

    spray = [ #These are all stored in a local folder. If this doesnt work for you, Use the format C://path/path or D://path/path to insert a file. 
        r"big2.txt",
        r"big.txt",
        r"common.txt",
        r"common2.txt",
        r"bignew.txt",
        r"wordlist.txt",
        r"wordlist2.txt",
    ]

    recon.process_files(spray)

if __name__ == "__main__":
    main()
