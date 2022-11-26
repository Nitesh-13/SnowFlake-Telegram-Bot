import requests

#Implementation of fun apis
def get_url():
    contents = requests.get('https://random.dog/woof.json').json()    
    url = contents['url']
    return url

def get_fact():
    contents = requests.get('https://uselessfacts.jsph.pl/random.json?language=en').json()
    fact = contents['text']
    return fact