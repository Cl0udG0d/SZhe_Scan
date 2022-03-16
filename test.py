import requests
import time
while True:
    rep=requests.get('')
    print(rep.text)
    time.sleep(2)