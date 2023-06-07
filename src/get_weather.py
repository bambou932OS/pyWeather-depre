from urllib import parse, request
import json
from . import api_key_parser # This is a relative import

WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

def build_url(location, metric=True):
    # location is a list of strings, so we need to join them together
    city_name = " ".join(location)
    # We need to encode the city name to make it URL-safe
    city_name_encoded = parse.quote_plus(city_name)

    units = "metric" if metric else "imperial" # This is a ternary operator
    api_key = api_key_parser.get_api_key() # This is a relative import

    # Build the URL
    url = f'{WEATHER_API_URL}?q={city_name_encoded}&units={units}&appid={api_key}'
    
    return url

def get_weather(locations, metric=True):
    #location은 '/'을 기준으로 나누어야 한다.
    location_list = [[]]

    index = 0
    for location in locations:
        location = ''.join(location) # location is a list of strings, so we need to join them together
        
        if('/' in location):
            location_split = location.split("/")
            if(location == '/'): # '/'만 입력했을 때
                location_list.append([])
                index += 1

            elif(len(location_split) == 2): # '/'기준으로 뒤에 아무것도 없을 때
                location_list[index].append(location_split[0])
                location_list.append([])
                index += 1

            elif(len(location_split) == 3): # '/'기준으로 뒤에 문자열이 있을 때
                location_list[index].append(location_split[0])
                location_list.append([])
                index += 1
                location_list[index].append(location_split[2])
                
        else:
            location_list[index].append(location)

    print(location_list)

    query_url = build_url(location, metric)

    with request.urlopen(query_url) as response: # Get the response from the URL
        data = response.read()

    return json.loads(data) # Convert the response to a Python dict