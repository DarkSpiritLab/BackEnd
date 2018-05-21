import json


def read_relays():
    content = json.loads(open("details").read())
    data = list()
    for item in content['relays']:
        try:
            data.append([item['longitude'], item['latitude'], item['or_addresses'][0].split(':')[0], item['country'],
                         item['running']])
        except:
            data.append([-360, -360, item['or_addresses'][0].split(':')[0], 'unknown', item['running']])
    return data, content['relays_published']
