import requests

URL_AUTH = 'https://fleet-api.taxi.yandex.net/v1/parks/driver-profiles/list'
url = 'https://fleet-api.taxi.yandex.net/v1/parks/driver-work-rules?park_id=e96b6ddf4309416ba66bc8f801bc847f'

# {'id': 'de98224d038a4f98a10b0fd8bf967efe', 'is_enabled': True, 'name': 'Арендники Я-Таксист'},

headers = {
    'X-Client-ID': 'taxi/park/e96b6ddf4309416ba66bc8f801bc847f',
    'X-API-Key': 'zohhKIuBMdIpJTEiKzrePMQIUuHXDyNFgRrSf',
}

response_str = ''

data = {"query": {"park": {"id": "e96b6ddf4309416ba66bc8f801bc847f",
                           "driver_profile": {"work_rule_id": ["de98224d038a4f98a10b0fd8bf967efe"],
                                              "work_status": ["working", "not_working"]}}}}
response = requests.post(URL_AUTH, headers=headers, json=data)
print(response.status_code)
print(len(response.json()['driver_profiles']))

for i in range(len(response.json()['driver_profiles'])):
    print(i)
    if 'car' in response.json()['driver_profiles'][i]:
        print(response.json()['driver_profiles'][i]['car']['number'])
        if 'registration_cert' in response.json()['driver_profiles'][i]['car']:
            print(response.json()['driver_profiles'][i]['car']['registration_cert'])


'У468ВХ797'
