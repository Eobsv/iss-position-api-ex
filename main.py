import requests
from datetime import datetime, timezone
import smtplib
import time

# fake cords
MY_LAT = 72.229039
MY_LNG = 61.046019

MY_EMAIL = "fakemail"
MY_PASSWORD = "fakepassword"

# Testing coord
# MY_LAT = 5
# MY_LNG = 180

parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0,  # only needed param
}

response_iss = requests.get(url='http://api.open-notify.org/iss-now.json')
response_iss.raise_for_status()  # Raises an error if response != 200
data = response_iss.json()
longitude_iss = float(data["iss_position"]['longitude'])
latitude_iss = float(data["iss_position"]["latitude"])

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
# How to access api in webbrowser via url: endpoint?param=value&param=value
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]['sunrise'].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now(timezone.utc)

is_night = False
while True:
    time.sleep(60)
    if time_now.hour < sunrise or time_now.hour > sunset:
        is_night = True
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            if is_night and MY_LAT - 5 < latitude_iss < MY_LAT + 5 and MY_LNG - 5 < longitude_iss < MY_LNG < MY_LNG + 5:
                print("im here")
                connection.sendmail(from_addr=MY_EMAIL,
                                    to_addrs="fake email",
                                    msg="Subject: ISS overhead alert!\n\n "
                                        "Look up! Search for ISS")
