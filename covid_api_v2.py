
import requests
import json

def get_data():

    summary = requests.get('https://api-corona.azurewebsites.net/summary')
    raw_data = json.loads(summary.content)
    for i in raw_data["countries"]:
        if i["Code"] == "IN":
            break
    del i["Country_Region"]
    del i["Code"]
    del i["Timeline"]
    del i["Slug"]

    return i


if __name__ == "__main__":
    d = get_data()

    for i, j in d.items():
        print(i, j)

