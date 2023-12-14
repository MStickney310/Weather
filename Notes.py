#DoesHeKnowTheMusical

# API = Application Programming Interface

# we are going to use the requests library

# let's make a virtual environment
import requests

data = requests.get('https://www.google.com')
print(data.status_code)
print(data.text)
