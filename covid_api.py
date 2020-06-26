
import requests
import json

def get_data():

    summary = requests.get('https://api.covid19api.com/summary')
    raw_data = json.loads(summary.content)
    for i in raw_data["Countries"]:
        if i["CountryCode"] == "IN":
            break
    del i["Country"]
    del i["CountryCode"]
    del i["Date"]
    del i["Slug"]

    return i


if __name__ == "__main__":
    print(get_data())