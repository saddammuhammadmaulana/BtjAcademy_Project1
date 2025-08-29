import requests

req = requests.get(url="http://127.0.0.1:8080/")
print(req.content)