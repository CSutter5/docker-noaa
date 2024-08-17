FROM ubuntu:24.10

RUN apt update && apt upgrade -y

RUN apt install -y \
    python3 \
    python3-pip \
    git \
    cron \
    # For RTL-SDR
    libusb-1.0-0-dev \
    cmake \
    pkg-config \
    # For SatDump
    build-essential \
    g++ \
    libfftw3-dev \
    libpng-dev \
    libtiff-dev \
    libjemalloc-dev \
    libcurl4-openssl-dev \
    libvolk-dev \
    libnng-dev \
    ocl-icd-opencl-dev \
    # Web server
    nginx

RUN pip3 install ephem

COPY install/install_rtlsdr.sh /usr/local/bin/install_rtlsdr.sh
COPY install/install_satdump.sh /usr/local/bin/install_satdump.sh

RUN /usr/local/bin/install_rtlsdr.sh
RUN /usr/local/bin/install_satdump.sh