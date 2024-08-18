import requests

from satellites import satellites


def download_tle(url: str):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

print("Downloading...")

satellites_tles = []
for satellite in satellites:
    tle = download_tle(satellites[satellite]["url"])
    if tle:
        satellites_tles.append(tle)

satellite_tles = set(satellites_tles)

print("Saving...")

tle_file = open("tle.txt", "w")

for tle in satellite_tles:
    tle_file.write(tle)

tle_file.close()

print("Updated")