git clone https://github.com/rtlsdrblog/rtl-sdr-blog

cd rtl-sdr-blog
mkdir build
cd build

cmake ../ -DINSTALL_UDEV_RULES=ON
make
make install

cp ../rtl-sdr.rules /etc/udev/rules.d/
ldconfig

# echo 'blacklist dvb_usb_rtl28xxu' | tee --append /etc/modprobe.d/blacklist-dvb_usb_rtl28xxu.conf