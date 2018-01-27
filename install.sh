export PYTHONPATH=/Cerelabs/openface:/Cerelabs/LightGBM/python-package
export DB_USER=root
export DB_PASS=root
export DB_NAME=surveillance

echo -e "\n------------------------------------------------\n"
echo "Start script is running..."

sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python3-dev python3-pip python-virtualenv
virtualenv --system-site-packages -p python3 /Cerelabs

directory='Cerelabs'

function python_packages()
{
    dec='y'
    if [[ "$dec" = "Y" || "$dec" = "y" ]];then
        if [ -d "/$directory" ]; then
            echo "Virtual environment exists"  
            echo "Finding out version of python"
            PYV=`/$directory/bin/python -c "import sys;t='{v[0]}.{v[1]}'.format(v=list(sys.version_info[:2]));sys.stdout.write(t)";`
            echo $PYV
            echo "Installing python dependencies..."
            sudo /$directory/bin/pip install -r src/requirements.txt
            echo "Finished installing python dependencies"
        else
            echo "No such virtual env exist"
        fi    
    fi
}

python_packages

echo -e "\n------------------------------------------------\n"
echo "Installing MySQL 5.7..."
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password password root'
sudo debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password root'
sudo apt-get -y install mysql-server

echo -e "\n------------------------------------------------\n"
echo "MySQL 5.7 has been installed."
echo "Initializing tables with ->root p->root db->surveillance"

mysql -u root -proot surveillance < database.sql

echo -e "\n------------------------------------------------\n"
echo "Installing dlib from source..."
echo "Installing dependencies..."
sudo apt-get install -y build-essential cmake pkg-config git check-install cmake yasm gfortran 
sudo apt-get install -y libx11-dev libatlas-base-dev libjpeg8-dev libjasper-dev libpng12-dev
sudo apt-get install -y libgtk-3-dev libboost-python-dev
sudo apt-get install -y libtiff5-dev
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libdc1394-22-dev
sudo apt-get install -y libxine2-dev libv4l-dev
sudo apt-get install -y libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev
sudo apt-get install -y qt5-default libgtk2.0-dev libtbb-dev
sudo apt-get install -y libatlas-base-dev
sudo apt-get install -y libfaac-dev libmp3lame-dev libtheora-dev
sudo apt-get install -y libvorbis-dev libxvidcore-dev
sudo apt-get install -y libopencore-amrnb-dev libopencore-amrwb-dev
sudo apt-get install -y x264 v4l-utils
sudo apt-get install -y libprotobuf-dev protobuf-compiler
sudo apt-get install -y libgoogle-glog-dev libgflags-dev
sudo apt-get install -y libgphoto2-dev libeigen3-dev libhdf5-dev doxygen

echo -e "\n------------------------------------------------\n"
echo "Getting dlib file..."
wget http://dlib.net/files/dlib-19.6.tar.bz2
echo -e "\n------------------------------------------------\n"
echo "Installing dlib"
tar xvf dlib-19.6.tar.bz2
cd dlib-19.6/
mkdir build
cd build
cmake ..
cmake --build . --config Release
sudo make install
sudo ldconfig
cd ..
pkg-config --libs --cflags dlib-1
cd dlib-19.6
/$directory/bin/python setup.py install
rm -rf dist
rm -rf tool/python/build
rm python_examples/dlib.so
sudo /$directory/bin/pip install dlib
echo -e "\n------------------------------------------------\n"
echo "Finished installing dlib"

echo -e "\n------------------------------------------------\n"
echo "Installing torch..."
echo -e "\n------------------------------------------------\n"

git clone https://github.com/torch/distro.git torch --recursive
cd torch; bash install-deps;
./install.sh
source ~/.bashrc
echo -e "\n------------------------------------------------\n"
echo "Finished installing torch"

echo -e "\n------------------------------------------------\n"
echo "Installing torch packages..."
for NAME in dpnn nn optim optnet csvigo cutorch cunn fblualib torchx tds; do luarocks install $NAME; done
echo "Finished installing torch packages"
echo -e "\n------------------------------------------------\n"

echo "Installing Openface..."
git clone --recursive https://github.com/cmusatyalab/openface.git
echo -e "\n------------------------------------------------\n"
echo "Finished installing openface"

echo -e "\n------------------------------------------------\n"
echo "Installing LightGBM..."
git clone --recursive https://github.com/Microsoft/LightGBM
cd LightGBM
mkdir build
cd build
cmake -DCMAKE_GENERATOR_PLATFORM=x64 ..
cmake --build . --target ALL_BUILD --config Release
cd ..
echo -e "\n------------------------------------------------\n"
echo "Finished installing LightGBM"

echo -e "\n------------------------------------------------\n"
echo "Installing FFMPEG"
apt-get update -qq && apt-get -y install \
  autoconf \
  automake \
  build-essential \
  cmake \
  git \
  libass-dev \
  libfreetype6-dev \
  libsdl2-dev \
  libtheora-dev \
  libtool \
  libva-dev \
  libvdpau-dev \
  libvorbis-dev \
  libxcb1-dev \
  libxcb-shm0-dev \
  libxcb-xfixes0-dev \
  mercurial \
  pkg-config \
  texinfo \
  wget \
  zlib1g-dev
mkdir -p ~/ffmpeg_sources ~/bin
cd ~/ffmpeg_sources && \
wget -O ffmpeg-snapshot.tar.bz2 http://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2 && \
tar xjvf ffmpeg-snapshot.tar.bz2 && \
cd ffmpeg && \
PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure \
  --prefix="$HOME/ffmpeg_build" \
  --pkg-config-flags="--static" \
  --extra-cflags="-I$HOME/ffmpeg_build/include" \
  --extra-ldflags="-L$HOME/ffmpeg_build/lib" \
  --extra-libs="-lpthread -lm" \
  --bindir="$HOME/bin" \
  --enable-gpl \
  --enable-libass \
  --enable-libfdk-aac \
  --enable-libfreetype \
  --enable-libmp3lame \
  --enable-libopus \
  --enable-libtheora \
  --enable-libvorbis \
  --enable-libvpx \
  --enable-libx264 \
  --enable-libx265 \
  --enable-nonfree && \
PATH="$HOME/bin:$PATH" make && \
make install
hash -r
echo "Finished Installing FFMPEG"
echo -e "\n------------------------------------------------\n"
cd ~/

echo "Installing OpenCV..."
git clone https://github.com/opencv/opencv.git
cd opencv 
git checkout 3.3.1 
cd ..
git clone https://github.com/opencv/opencv_contrib.git
cd opencv_contrib
git checkout 3.3.1
cd ..
echo "Running CMake on OpenCV"
cmake -D CMAKE_BUILD_TYPE=RELEASE \
      -D CMAKE_INSTALL_PREFIX=/usr/local \
      -D INSTALL_C_EXAMPLES=ON \
      -D INSTALL_PYTHON_EXAMPLES=ON \
      -D WITH_TBB=ON \
      -D WITH_V4L=ON \
      -D WITH_QT=ON \
      -D WITH_OPENGL=ON \
      -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules \
      -D BUILD_EXAMPLES=ON ..
echo -e "\n------------------------------------------------\n"
echo "CMake Finished building OPenCV"
echo -e "\n------------------------------------------------\n"
make -j4
sudo make install
sudo sh -c 'echo "/usr/local/lib" >> /etc/ld.so.conf.d/opencv.conf'
sudo ldconfig
echo ""
find /usr/local/lib/ -type f -name "cv2*.so"
cd /$directory/lib/python3.5/site-packages
ln -s /usr/local/lib/python3.5/dist-packages/cv2.cpython-36m-x86_64-linux-gnu.so cv2.so
echo "Finished Installing OpenCV"
echo -e "\n------------------------------------------------\n"

cd src/system
/$directory/bin/python WebApp.py



