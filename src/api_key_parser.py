from configparser import ConfigParser

def make_api_key_file():
    print('Enter your API key: ', end='')
    api_key = input()

    config = ConfigParser()
    config['openweathermap'] = {'api_key': api_key}
    with open('api_key.ini', 'w') as f:
        config.write(f)

def get_api_key():
    config = ConfigParser()
    try:
        config.read('api_key.ini')
        result = config['openweathermap']['api_key']
    except:
        print('Failed to parse api_key.ini file.')
        print('Please Enter Valid API Key.')
        raise SystemExit
    
    return result