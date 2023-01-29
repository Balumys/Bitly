import sys
import os
import requests
from dotenv import load_dotenv
import argparse


def is_bitlink(token, user_url):
    url_template = "https://api-ssl.bitly.com/v4/bitlinks/{}"
    url = url_template.format(user_url)
    authorization_params = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=authorization_params)
    return response.ok


def count_clicks(token, user_url):
    url_tempalet = "https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary"
    url = url_tempalet.format(user_url)
    authorization_params = {"Authorization": f"Bearer {token}"}
    payload = {"unit": "day",
               "units": "-1"}
    response = requests.get(url, params=payload, headers=authorization_params)
    response.raise_for_status()
    return response.json()["total_clicks"]


def shorten_link(token, user_url):
    url = "https://api-ssl.bitly.com/v4/bitlinks"
    authorization_params = {"Authorization": f"Bearer {token}"}
    payload = {"long_url": user_url}
    response = requests.post(url, json=payload, headers=authorization_params)
    response.raise_for_status()
    return response.json()["id"]


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Convert url to bitlink or show сlicks amount on bitlink ")
    parser.add_argument("url", help="URL link to be shorted or bitlink")
    args = parser.parse_args()
    user_url = args.url
    token = os.getenv("BITLY_TOKEN")

    try:
        if is_bitlink(token, user_url):
            clicks_count = count_clicks(token, user_url)
            print(clicks_count, "Clicks on bitlink")
        else:
            bitlink = shorten_link(token, user_url)
            print('Bitlink:', bitlink)

    except requests.exceptions.HTTPError as err:
        sys.exit(err)


if __name__ == '__main__':
    main()
