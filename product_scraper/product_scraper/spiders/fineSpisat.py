import requests
from uuid import uuid4

URL_AUTH = 'https://fleet-api.taxi.yandex.net/v2/parks/driver-profiles/transactions'
url = 'https://fleet-api.taxi.yandex.net/v2/parks/transactions/categories/list'

# {'id': 'de98224d038a4f98a10b0fd8bf967efe', 'is_enabled': True, 'name': 'Арендники Я-Таксист'},
#'id': '023e46118ba74f1c92f2a7189af6c68b' - Petya
headers = {
    #'Accept-Language':'ru',
    'X-Client-ID': 'taxi/park/e96b6ddf4309416ba66bc8f801bc847f',
    'X-API-Key': 'zohhKIuBMdIpJTEiKzrePMQIUuHXDyNFgRrSf',
    'X-Idempotency-Token': str(uuid4())
}
'''
data = {"query": {
                  "park": {"id": "e96b6ddf4309416ba66bc8f801bc847f"
                           }
                  }
        }

response = requests.post(url, headers=headers,json=data)
print(response.status_code)
print(response.json())


shtrul_array =[]
'''
data = {"amount": "-5" ,
        "category_id": "partner_service_manual",
        "description": "test",
        "driver_profile_id": "023e46118ba74f1c92f2a7189af6c68b",
        "park_id": "e96b6ddf4309416ba66bc8f801bc847f"}
response = requests.post(URL_AUTH, headers=headers, json=data)
print(response.status_code)
print(response.json())
'''
car_number =[]
region = []
sts = []

for i in range(len(response.json()['driver_profiles'])):
    if 'car' in response.json()['driver_profiles'][i]:
        car_number.append(response.json()['driver_profiles'][i]['car']['number'][0:5])
        region.append(response.json()['driver_profiles'][i]['car']['number'][6:])
        if 'registration_cert' in response.json()['driver_profiles'][i]['car']:
            sts.append(response.json()['driver_profiles'][i]['car']['registration_cert'])
        else:
            sts.append('')

shtrul_array.append(car_number)
shtrul_array.append(region)
shtrul_array.append(sts)

print(shtrul_array[0][0])
print(shtrul_array[1][0])
print(shtrul_array[2][0])
'У468ВХ797'
'''
