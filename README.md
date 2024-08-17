# docker-noaa

Docker NOAA is an automated tool recive APT images from NOAA Weather satellites.

This uses [SatDump](https://github.com/SatDump/SatDump) to demodulate satellite images. \
The base image is [Ubuntu](https://hub.docker.com/_/ubuntu).

This uses an RTL-SDR dongle to recive the images. With either a [V-Dipole or QFH antenna](https://www.rtl-sdr.com/rtl-sdr-tutorial-receiving-noaa-weather-satellite-images/). \
You can optionally use a [SAWbird+ NOAA LNA/Filter](https://a.co/d/8yfDv9x) 