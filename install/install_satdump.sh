git clone https://github.com/SatDump/SatDump.git

cd SatDump
mkdir build && cd build

cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/usr -DBUILD_GUI=OFF ..
make -j`nproc`

make install