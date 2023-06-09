# Print weather information
import pprint

def print_weather_info(weather_data, metric=True):
    #pprint.pprint(weather_data)

    print(
        f'The weather in {weather_data["name"]}({weather_data["sys"]["country"]}) '
        f'is {weather_data["main"]["temp"]}°{"C" if metric else "F"}, {weather_data["weather"][0]["description"].capitalize()}'
    )
