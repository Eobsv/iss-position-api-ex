import requests


response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status() # Raises an error if response != 200
data = response.json()["iss_position"]

print(data)
