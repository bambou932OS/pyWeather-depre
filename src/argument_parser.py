import sys
import argparse

def parse_method(parse_str :str):
    print(parse_str)
    return parse_str.split(',')

def get_args():
    parser = argparse.ArgumentParser(description='Get the weather forecast for a given location.')

    parser.add_argument('location', metavar='location', type= parse_method, nargs='+', help='The location to get the weather forecast.')
    # Celsius scale, 섭씨 온도 척도
    parser.add_argument('-c', '-m', '--metric', dest='metric', action='store_true', help='Use metric units instead of imperial.')
    # Fahrenheit scale, 화씨 온도 척도
    parser.add_argument('-f', '-i', '--imperial', dest='metric', action='store_false', help='Use imperial units instead of metric.')

    parser.set_defaults(metric=True)
    return parser.parse_args()