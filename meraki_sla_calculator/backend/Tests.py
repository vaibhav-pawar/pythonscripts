import requests

URL = ""
API_KEY = ""
HEADERS = {"Content-Type": "application/json", "Accept": "application/json", "X-Cisco-Meraki-API-Key": API_KEY}

req = requests.get(url=URL, headers=HEADERS)

"""
print("__________JSON__________")
print(req.json())
print("________________________")
"""

"""
print("__________TEXT__________")
print(req.text)
print("________________________")
"""

"""
print("__________HTML__________")
print(req.content)
print("________________________")
"""
