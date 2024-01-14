import requests
from time import sleep
import random

while True:
    requests.get(f"https://backend.townesquare.xyz/activity/point/{random.randint(1, 100000000000000)}/A1Q09")
    