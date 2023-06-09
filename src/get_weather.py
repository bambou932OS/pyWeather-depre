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
        
        if('/' in location): # '/'이 들어 있을 때
            location_split = location.split("/")

            if('' not in location_split): # 띄어쓰기가 없을 때 (ex. busan/seoul)
                location_list[index].append(location_split[0])
                location_list.append([])
                index += 1
                location_list[index].append(location_split[1])

            else:
                if(location_split[0] == '' and location_split[1] == ''): # '/' 만 들어왔을 때
                    location_list.append([])
                    index += 1
                
                elif(location_split[0] == ''): # '/'로 시작할 때 (ex. /seoul)
                    location_list.append([])
                    index += 1
                    location_list[index].append(location_split[1])
                
                elif(location_split[1] == ''): # '/'로 끝날 때 (ex. busan/)
                    location_list[index].append(location_split[0])
                    location_list.append([])
                    index += 1
                

        else: # '/'이 없을 때
            location_list[index].append(location)


    data = []

    for location in location_list:
        query_url = build_url(location, metric)

        try:
            with request.urlopen(query_url) as response: # Get the response from the URL
                data.append(json.loads(response.read()))

        except error.HTTPError as e: # If an HTTPError occurs (e.g., 404 Not Found)
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