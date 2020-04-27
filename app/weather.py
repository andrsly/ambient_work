import json, requests

url = "http://weather.labben.org/api/yr/?location=Portugal/Lisboa/Lisboa"

def getWeatherData(): 
    response = requests.get(url)
    data = response.text
    parsed = json.loads(data)
    return parsed



