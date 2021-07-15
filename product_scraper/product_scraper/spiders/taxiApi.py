import requests

URL_AUTH = 'https://fleet-api.taxi.yandex.net/v1/parks/driver-profiles/list'
url = 'https://fleet-api.taxi.yandex.net/v1/parks/driver-work-rules?park_id=e96b6ddf4309416ba66bc8f801bc847f'

#{'id': 'de98224d038a4f98a10b0fd8bf967efe', 'is_enabled': True, 'name': 'Арендники Я-Таксист'},

headers = {
    'X-Client-ID': 'taxi/park/e96b6ddf4309416ba66bc8f801bc847f',
    'X-API-Key': 'zohhKIuBMdIpJTEiKzrePMQIUuHXDyNFgRrSf',
}

response_str = ''

offset = 0

while True:
    data = {"offset": offset, "query": { "park": { "id": "e96b6ddf4309416ba66bc8f801bc847f", "driver_profile":{"work_rule_id": ["de98224d038a4f98a10b0fd8bf967efe"]} } } }
    response = requests.post(URL_AUTH, headers = headers, json = data)
    print(response.status_code)
    print(len(response.json()['driver_profiles']))

    for i in range(len(response.json()['driver_profiles']) - 1):
        print(i)
        if 'car' in response.json()['driver_profiles'][i] :
            #if response.json()['driver_profiles'][i]['car']['number'].lower() == 'У468ВХ797'.lower():
            print(response.json()['driver_profiles'][i])
                #break

    #response_str += str(response.json()['driver_profiles'])
    offset += len(response.json()['driver_profiles'])
    if not len(response.json()['driver_profiles']) % 1000 == 0:
        break
'''
f = open("demofile3.txt", "a")
f.write('\n')
f.write(response_str)
f.close()
'''



'У468ВХ797'