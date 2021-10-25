import requests
from datetime import datetime
import smtplib
import time


MY_LONG = -82.414150
MY_LAT = 27.276930

def is_iss_overhead():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True

def is_night():
    parametrs = {
        "lat": MY_LAT,
        "long": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parametrs)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data['results']['sunrise'].split("T")[1].split(":")[0])
    sunset = int(data['results']['sunset'].split("T")[1].split(":")[0])

    now = datetime.now()
    time = int(str(now.time()).split(":")[0])
    # time = now.time().hour

    if time >= sunset or time <= sunrise:
        return True

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
            my_email = 'testForCoursesOlga@gmail.com'
            password = 'testForCourses1224'
            connection = smtplib.SMTP("smtp.gmail.com", 587)
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs=my_email,
                                msg=f"Subject:ISS\n\n Look up, there is ISS")
            connection.close()

#If the ISS is close to my current position(+- 5 degree of my current position)
# and it is currently dark
# Then send me an email to tell me to look up.

