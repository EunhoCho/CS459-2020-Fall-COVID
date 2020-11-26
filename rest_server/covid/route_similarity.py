import math

import requests


def _user_route(userID):
    response = requests.get("http://192.249.19.250:7880/api/v1/route/user/?userID=" + str(userID))
    routes = response.json()

    result = []
    for route in routes:
        result.append((route['latitude'], route['longitude']))
    return result


def check_similarity(covidUserID):
    covid_user_route = _user_route(covidUserID)

    response = requests.get("http://192.249.19.250:7880/api/v1/user")
    users = response.json()

    ans = []
    for user in users:
        if user['id'] != covidUserID and not user['isCOVID']:
            target_route = _user_route(user['id'])

            distances = []
            for i in range(len(covid_user_route)):
                covid_lat = math.radians(covid_user_route[i][0])
                covid_lon = math.radians(covid_user_route[i][1])
                target_lat = math.radians(target_route[i][0])
                target_lon = math.radians(target_route[i][1])

                diff_lat = covid_lat - target_lat
                diff_lon = covid_lon - target_lon

                a = math.sin(diff_lat / 2) ** 2 + math.cos(covid_lat) * math.cos(target_lat) * math.sin(diff_lon / 2) ** 2
                distances.append(6373.0 * 2 * math.atan2(a ** 0.5, (1 - a) ** 0.5) * 1000)

            inside_2m = 0
            for dist in distances:
                if dist < 2:
                    inside_2m += 1
                if inside_2m > 10:
                    ans.append(user)
                    break

    return ans
