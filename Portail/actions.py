from time import sleep

import requests
import Portail.sonoff as sonoff
import Portail.portail as portail

s = sonoff.Sonoff('emilie.pedro@libertysurf.fr', '106106106', 'eu')


def getToken():
    return s.get_bearer_token()


def getDevices():
    headers = {
        'Authorization': 'Bearer ' + getToken(),
        'Content-Type': 'application/json;charset=UTF-8'
    }
    r = requests.get(
        'https://{}-api.coolkit.cc/api/user/device?appid=YzfeftUVcZ6twZw1OoVKPRFYTrGEg01Q'.format('eu'),
        headers=headers)
    devices = r.json()

    return devices


def toggle(devices):
    if devices:
        # We found a device, lets turn something on
        device_id = devices[0]['deviceid']
        headers = {
            'Authorization': 'Bearer '+getToken(),
            'Content-Type': 'application/json;charset=UTF-8'
        }

        data = {
            'deviceid' : device_id,
            'params' : {'switch':'on'},
            'appid': 'YzfeftUVcZ6twZw1OoVKPRFYTrGEg01Q',
            'version': 8,
          }
        r = requests.post(
            'https://{}-api.coolkit.cc:8080/api/user/device/status'.format('eu'),
            headers=headers, json=data)
        return r.json()


def open():
    status, message, labels = portail.predict()
    if status == 'Closed':
        result = toggle(getDevices())
    elif status == 'Open':
        result = 'Already open'
    else:
        label_one = labels.index(status)
        result = toggle(getDevices())
        sleep(1)
        status, message, labels = portail.predict()
        label_two = labels.index(status)

        if label_one < label_two:
            pass
        else:
            toggle(getDevices())
            result = toggle(getDevices())

    return result


def close():
    status, message, labels = portail.predict()
    if status == 'Closed':
        result = 'Already clsoed'
    elif status == 'Open':
        result = toggle(getDevices())
    else:
        label_one = labels.index(status)
        result = toggle(getDevices())
        sleep(1)
        status, message, labels = portail.predict()
        label_two = labels.index(status)

        if label_one > label_two:
            pass
        else:
            toggle(getDevices())
            result=toggle(getDevices())

    return result