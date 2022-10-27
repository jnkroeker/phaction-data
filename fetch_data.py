#!/Users/johnkroeker/Desktop/phaction_scripts/bin/python

# ^ modify above to path displayed as the result of executing 'which python' in you venv
# the above points to the python in the venv created in ~/Desktop/phaction_resources/ on your laptop
# remember to always source the venv before executing this script (`source ~/Desktop/phaction_scripts/bin/activate`)

import requests
import urllib3
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Strava endpoints to pull
auth_url = "https://www.strava.com/oauth/token"

activites_url = "https://www.strava.com/api/v3/athlete/activities"
# routes_url    = "https://www.strava.com/api/v3/athletes/{id}/routes"

## for each route export each as gpx
# export_route_gpx_url = "https://www.strava.com/api/v3/routes/{id}/export_gpx"


payload = {
    'client_id': "xxxx",
    'client_secret': 'xxxx',
    'refresh_token': 'xxxx',
    'grant_type': "refresh_token",
    'f': 'json'
}

print("Requesting Token...\n")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']
print("Access Token = {}\n".format(access_token))

header = {'Authorization': 'Bearer ' + access_token}
param = {'per_page': 200, 'page': 1}
my_dataset = requests.get(activites_url, headers=header, params=param).json()

print(my_dataset[0]["name"])
print(my_dataset[0]["map"]["summary_polyline"])

# save data to a file
# later to s3
with open("data.json", "w") as outfile:
    json.dump(my_dataset, outfile)

