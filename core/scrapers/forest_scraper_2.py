import os
from requests.api import request
from tqdm import tqdm
import requests

with open("Forest Gain APIs.txt") as f:
    urls = f.read().split()

for url in tqdm(urls):
    r = requests.get(url)

    with open(os.path.join("..", "..", "data", "forest", url.split("/")[-1]), "wb") as fout:
        fout.write(r.content)