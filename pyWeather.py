import sys
sys.path.append('./code')

from src.argument_parser import get_args # This is a relative import
from src.api_key_parser import get_api_key, make_api_key_file # This is a relative import
from src.get_weather import get_weather # This is a relative import
from src.print_weather_info import print_weather_info # This is a relative import

def main():
    # api_key.ini 파일을 읽어서 api_key를 가져오는데,
    # api_key.ini 파일이 없거나, api_key.ini 파일이 올바른 형식이 아니면
    # sys.stdin.readline()을 통해 api_key를 입력받고, api_key.ini 파일을 생성하여 저장한다.
    try: 
        api_key = get_api_key()
        if(len(api_key) == 0):
            raise Exception
        
    except: # api_key.ini 파일이 없거나, api_key.ini 파일이 올바른 형식이 아닐 때
        make_api_key_file()
    
    args = get_args() # Get the command-line arguments

    location = args.location
    metric = args.metric
    
    weather_data = get_weather(location, metric)

    print_weather_info(weather_data, metric)

if __name__ == "__main__": # Tells Python to run main() if we run this file directly
    main()