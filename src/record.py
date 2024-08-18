from rtlsdr import RtlSdr
import numpy as np
from scipy.io import wavfile
import datetime
import os
import time

from dotenv import load_dotenv 
load_dotenv() 

import ephem

from satellites import satellites

output_dir = "./captures"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Read TLE's
def update_tle():
    tle_file = open("tle.txt", "r")
    satellites_tles_raw = tle_file.readlines()
    tle_file.close()

    satellites_tles = []
    for i in range(0, len(satellites_tles_raw), 3):
        satellites_tles.append(
            ephem.readtle(
                satellites_tles_raw[i],
                satellites_tles_raw[i+1],
                satellites_tles_raw[i+2],
            )
        )
        
    return satellites_tles

satellites_tles = update_tle()

# For each satellite compute the next pass and add them to a list
location = ephem.Observer()
location.lat = os.getenv("lat")
location.lon = os.getenv("lon")
location.elevation = int(os.getenv("elevation"))

def next_pass(location, tle) -> int:
    info = location.next_pass(tle)
    
    if info == None:
        return None
    
    return  {
        "name": tle.name,
        "rise_time": ephem.localtime(info[0]),
        "rise_azimuth": info[1],
        "max_time": ephem.localtime(info[2]),
        "max_azimuth": info[3],
        "set_time": ephem.localtime(info[4]),
        "set_azimuth": info[5]
    }

def update_passes(location, tles):
    satellites_passes = []
    
    for tle in tles:
        satellites_passes.append(
            next_pass(location, tle)
        )

    sorted_passes = sorted(satellites_passes, key=lambda x: x['rise_time'])
    
    return sorted_passes

passes = update_passes(location, satellites_tles)

def record(freq, duration):
    # Start recording
    print("Recording...")
    sdr = RtlSdr()
    sdr.sample_rate = 2.048e6
    sdr.center_freq = freq
    sdr.gain = 50
    sdr.set_sample_rate(2.4e6)
    
    output = f"{output_dir}/{str(datetime.datetime.now())}.wav"
    samples_per_chunk = int(sdr.sample_rate)
    
    wavfile.write(output, int(sdr.sample_rate), np.zeros((0, 2), dtype=np.int16))  # Create an empty WAV file
    
    print("Recording...")
    for _ in range(int(duration)):
        samples = sdr.read_samples(samples_per_chunk)
        samples_iq = np.vstack((samples.real, samples.imag)).T  # Separate into I and Q channels
        samples_iq_normalized = np.int16(samples_iq * 32767)    # Normalize to 16-bit range

        # Append to the WAV file
        with open(output, 'ab') as f:
            wavfile.write(f, int(sdr.sample_rate), samples_iq_normalized)

    # Clean up
    sdr.close()
    
    # Run satdump
    os.system(f"satdump noaa_apt baseband {output}")
    

def wait_for_next_pass(passes):
    while passes:
        time_until_next = passes[0]['rise_time'] - datetime.datetime.now()
        print(f"Next pass of {passes[0]['name']} in {time_until_next}")

        if time_until_next.total_seconds() <= 60:
            duration = passes[0]['max_time'] - passes[0]['rise_time']
            duration = duration.total_seconds() + 60

            print(f"Recording {passes[0]['name']} for {duration} seconds")
            record(satellites[passes[0]["name"]]["apt_freq"], duration)

            passes = update_passes(location, satellites_tles)
        else:
            time.sleep(time_until_next.total_seconds() / 2)

    print("No more passes scheduled.")

    
wait_for_next_pass(passes)