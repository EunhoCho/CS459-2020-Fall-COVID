import json

import requests


def send_notify(text):
    # app_key = "d9696e52861ec16d2f264fd9bc2deab2"
    # uri = "http://192.249.19.250:7880"
    # url = "https://kauth.kakao.com/oauth/authorize?client_id=" + app_key + "&redirect_uri=" + uri + "&response_type=code"
    # response = requests.get(url)
    #
    # print(response.url)
    # code = response.json().get('code')

    # url = "https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id=" + app_key + "&redirect_uri=" + uri + "&code="
    # url += "_2ukeq0mgZzXIXODRoHMVhsqu8MMAOPbdBmfT9JmBU8pgvu5GcCcB4bOtJVefIWMyshpFAo9dVwAAAF2HEmPvg"
    # response = requests.post(url)
    # print(response.json())
    # access_token = response.json().get('access_token')

    access_token = "D_e2-4TQBtx_P1-kZ305sV1s2b8Dx2wBROJahQo9dNsAAAF2HEqc9g"
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    headers = {
        "Authorization": "Bearer " + access_token
    }

    data = {"template_object": json.dumps({"object_type": "text",
                                           "text": text,
                                           "link": {"web_url": "http://192.249.19.250:7880/api/v1/doc/"}
                                           })
            }

    response = requests.post(url, headers=headers, data=data)

    if response.json().get('result_code') == 0:
        return True

    print(response.json())
    return False
