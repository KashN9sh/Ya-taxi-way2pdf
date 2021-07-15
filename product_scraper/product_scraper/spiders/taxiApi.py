import requests

URL_AUTH = 'https://fleet-api.taxi.yandex.net/v1/parks/driver-profiles/list'
url = 'https://fleet-api.taxi.yandex.net/v1/parks/driver-work-rules?park_id=e96b6ddf4309416ba66bc8f801bc847f'

# {'id': 'de98224d038a4f98a10b0fd8bf967efe', 'is_enabled': True, 'name': 'Арендники Я-Таксист'},

headers = {
    'X-Client-ID': 'taxi/park/e96b6ddf4309416ba66bc8f801bc847f',
    'X-API-Key': 'zohhKIuBMdIpJTEiKzrePMQIUuHXDyNFgRrSf',
}

'''
response = requests.get(url, headers=headers)
print(response.status_code)
print(response.json())
'''

shtrul_array =[]

data = {"query": {"park": {"id": "e96b6ddf4309416ba66bc8f801bc847f",
                           "driver_profile": {"work_rule_id": ["de98224d038a4f98a10b0fd8bf967efe",
                                                               "badd1c9d6b6b4e9fb9e0b48367850467"],
                                              "work_status": ["working", "not_working"]}}}}
response = requests.post(URL_AUTH, headers=headers, json=data)
print(response.status_code)
print(len(response.json()['driver_profiles']))

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
