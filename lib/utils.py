from urequests import get
import wifi
import json
from uio import open
import machine
rtc = machine.RTC()

def getCurrentTime(config):
    if not wifi.wlan.isconnected():
        wifi.connect(config)
    else:
        res = get(config["timeUrl"])
        data = json.loads(res.text)
        dt = string_to_tuple_with_offset(data['utc_datetime'], data['utc_offset'])
        print(dt)
        return dt
    
    
def getConfig():
    file = open('../config.json')
    config = json.load(file)
    return config

def setRTC():
    config = getConfig()
    rtc.datetime(getCurrentTime(config))
    print(rtc.datetime())
    
def getTime():
    return rtc.datetime()

def getIsotime():
    return tuple_to_iso_string(rtc.datetime())


#chatgpt for the win!
def string_to_tuple_with_offset(utc_datetime, utc_offset):
    # Parse UTC datetime string
    year = int(utc_datetime[0:4])
    month = int(utc_datetime[5:7])
    day = int(utc_datetime[8:10])
    hours = int(utc_datetime[11:13])
    minutes = int(utc_datetime[14:16])
    seconds = int(utc_datetime[17:19])
    subseconds = int(utc_datetime[20:26])

    # Calculate weekday using Zeller's congruence formula
    if month < 3:
        year -= 1
    month = (month + 9) % 12 + 1
    century = year // 100
    year_of_century = year % 100
    weekday = (day + (13 * month - 1) // 5 + year_of_century + year_of_century // 4 + century // 4 - 2 * century) % 7

    # Convert UTC offset string to seconds
    utc_offset_sec = int(utc_offset[:3]) * 3600 + int(utc_offset[4:]) * 60

    # Apply UTC offset to local time fields
    hours -= utc_offset_sec // 3600
    minutes -= (utc_offset_sec % 3600) // 60

    # Handle negative hour/minute values due to UTC offset
    if minutes < 0:
        hours -= 1
        minutes += 60
    if hours < 0:
        weekday = (weekday - 1) % 7
        hours += 24
        day -= 1
        if day == 0:
            month -= 1
            if month == 0:
                month = 12
                year -= 1
            _, last_day = days_in_month(year, month)
            day = last_day

    # Create final tuple
    return (year, month, day, weekday, hours, minutes, seconds, subseconds)

def days_in_month(year, month):
    if month == 2:
        # February has 28 days in common years, 29 in leap years
        if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0):
            return 29
        else:
            return 28
    elif month in {4, 6, 9, 11}:
        # April, June, September, November have 30 days
        return 30
    else:
        # All other months have 31 days
        return 31


def tuple_to_iso_string(datetime):
    # Extract values from the tuple
    year, month, day, weekday, hours, minutes, seconds, subseconds = datetime
    
    # Format the datetime as an ISO string
    iso_string = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.{:03d}Z".format(year, month, day, hours, minutes, seconds, subseconds)
    
    # Return the ISO string
    return iso_string

def write_to_sd(text):
    f = open('/lib/sd/data.txt', 'w')
    f.write(text)
    f.close()
    
def edit_file(file, obj):
    with open('/lib/sd/' + file , 'r') as f:
        data = json.load(f)
    data.append(obj)
    with open('data.json', 'w') as f:
        json.dump(data, f)
