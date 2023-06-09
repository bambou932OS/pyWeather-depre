from urllib import parse, request, error
import json
from . import api_key_parser # This is a relative import

WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

def build_url(location, metric=True):
    # location is a list of strings, so we need to join them together
    city_name = " ".join(location)
    # We need to encode the city name to make it URL-safe
    city_name_encoded = parse.quote_plus(city_name)

    units = "metric" if metric else "imperial" # This is a ternary operator
    try: 
        api_key = api_key_parser.get_api_key()
        if(len(api_key) == 0):
            raise Exception
        
    except: # api_key.ini 파일이 없거나, api_key.ini 파일이 올바른 형식이 아닐 때
        api_key_parser.make_api_key_file()

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

            
    
    data = []

    for location in location_list:
        query_url = build_url(location, metric)

        try:
            with request.urlopen(query_url) as response: # Get the response from the URL
                data.append(json.loads(response.read()))

        except error.HTTPError as e:
            if(e.code == 400):
                print('400 Bad Request.')
                print('If this error occurs periodically, please report an issue')

            if(e.code == 401):
                print('Invalid API Key. Enter Valid API Key.')
                api_key_parser.make_api_key_file()

            if(e.code == 404):
                print('City not found. Please enter valid city name.')
                raise SystemExit

            if(e.code == 429):
                print('Too many requests. Please try again later.')
                raise SystemExit

            if(e.code//100 == 5): # 5xx Server Error
                print('Unexpected Error. Check Internet connection and try again later.')
                raise SystemExit
                
    return data