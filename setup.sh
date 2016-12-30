## Initialize some stuff

APP_DIR=/vagrant/scripts

sudo apt-get update

sudo apt-get install -y build-essential curl git-core \
libssl-dev libffi-dev libreadline-dev emacs \
python3-dev python-dev python3-tk

## Download pip
wget https://bootstrap.pypa.io/get-pip.py -nv
sudo python get-pip.py
sudo python3 get-pip.py
sudo rm get-pip.py

## Install virtualenv
sudo pip install virtualenv

## Setup virtualenv project
mkdir $APP_DIR
chown vagrant:vagrant $APP_DIR
chmod 0777 $APP_DIR

cd $APP_DIR
virtualenv env
source env/bin/activate

## Install some stuff
pip install numpy
pip install scipy
pip install matplotlib
pip install pandas
pip install quandl
pip install sklearn
pip install pandas-datareader
## Required to read .html into pandas DF
pip install html5lib
pip install lxml
pip install bs4 # BeautifulSoup4
pip install openpyxl
