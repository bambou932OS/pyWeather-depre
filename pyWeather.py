import sys
sys.path.append('./code')

from api_key_parser import get_api_key # This is a relative import
from argument_parser import get_args # This is a relative import

def main():
    api_key = get_api_key()
    
    args = get_args()
    print(args)

if __name__ == "__main__": # Tells Python to run main() if we run this file directly
    main()