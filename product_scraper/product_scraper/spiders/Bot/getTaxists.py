import requests
import pandas as pd

url_auth = 'https://fleet-api.taxi.yandex.net/v1/parks/driver-profiles/list'

headers = {
            'X-Client-ID': 'taxi/park/e96b6ddf4309416ba66bc8f801bc847f',
            'X-API-Key': 'zohhKIuBMdIpJTEiKzrePMQIUuHXDyNFgRrSf',
           }

offset = 0

xl = pd.read_excel('data1.xlsx')
xl = xl.astype({"Phone": str}, errors='raise')
print(xl)

for k in range(6):

    data = {"limit": 1000,
            "offset": offset,
            "query": {"park": {"id": "e96b6ddf4309416ba66bc8f801bc847f"}}
            }

    response1 = requests.post(url_auth, headers=headers, json=data)
    for i in range(len(response1.json()['driver_profiles'])):
        profile = response1.json()['driver_profiles'][i]['driver_profile']
    #profile['first_name'] + ' ' + profile['last_name'] + ' ' + profile['middle_name'] + ' ' + profile['phones']
        for j in range(len(xl['User'])):
            if profile['last_name'].lower() == xl['User'][j].split()[0].lower():
                print(profile['last_name'] + ' ' + profile['first_name'] +  ' ' + profile['phones'][0])
                if xl['Phone'][j] == 'nan':
                    xl['Phone'][j] = str(profile['phones'][0])
                print(i)
    offset = offset + 1000
            
xl.to_csv('1.csv')