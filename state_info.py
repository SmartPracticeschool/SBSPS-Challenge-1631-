
import requests
import json

def get_state_data():

    summary = requests.get('https://api.rootnet.in/covid19-in/stats/latest')
    raw_data = json.loads(summary.content)
    alpha = raw_data['data']['regional']
    
    return alpha
 


if __name__ == "__main__":
    a = get_state_data()
    g =0
    print(a[0])
    print(g)