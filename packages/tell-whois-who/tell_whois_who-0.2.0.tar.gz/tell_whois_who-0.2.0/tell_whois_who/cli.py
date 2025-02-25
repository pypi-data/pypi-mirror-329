# tell_whois_who/cli.py

import argparse
import requests
import json
import sys

# --- Configuration ---
JSON_URL = "https://raw.githubusercontent.com/Sriharan-S/whois-who-data/main/data.json"

def who_is_command(parameter):
    """
    Fetches JSON data from a URL, looks up the provided parameter as a key,
    and prints the corresponding value as a plain string, or error as JSON.
    """
    try:
        response = requests.get(JSON_URL)
        response.raise_for_status()
        data = response.json()

        if parameter in data:
            value = data[parameter]
            print(value)
        else:
            print(f"No topic for \"{parameter}\".")

    except requests.exceptions.RequestException as e:
        print(json.dumps({"error": f"Error fetching JSON data: {e}"}))
    except json.JSONDecodeError:
        print(json.dumps({"error": "Error decoding JSON response. Invalid JSON format."}))


def main():
    parser = argparse.ArgumentParser(description="Look up information from a JSON data source.")
    parser.add_argument("parameter", help="The key to look up in the JSON data.")
    args = parser.parse_args()

    who_is_command(args.parameter)


if __name__ == "__main__":
    main()