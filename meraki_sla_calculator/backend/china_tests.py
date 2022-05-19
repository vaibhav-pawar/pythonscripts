import requests

URL = "https://api.meraki.com/api/v1/organizations/894791"
# URL = URL.replace("v1", "v0")
URL = f"{URL}/networks"
HEADERS = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Cisco-Meraki-API-Key": "2828f0a3484fe9c296f2230cfad9899e3196aecf"
        }

print(URL, HEADERS)

req = requests.get(url=URL, headers=HEADERS, verify=True)
print(req.text)
