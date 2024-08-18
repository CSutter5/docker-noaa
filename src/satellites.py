
# List of satellites to get images from
satellites = {
    "NOAA 15": {
        "CATNR": 25338,
        "url": "https://celestrak.org/NORAD/elements/gp.php?CATNR=25338&FORMAT=tle",
        # "apt_freq": 137.62e6
        "apt_freq": 106.3e6
    }, 
    "NOAA 18": {
        "CATNR": 28654,
        "url": "https://celestrak.org/NORAD/elements/gp.php?CATNR=28654&FORMAT=tle",
        "apt_freq": 137.9125e6
    }, 
    "NOAA 19": {
        "CATNR": 33591,
        "url": "https://celestrak.org/NORAD/elements/gp.php?CATNR=33591&FORMAT=tle",
        "apt_freq": 137.1e6
    }
}