# CryptoSnake


TA-Lib is widely used by trading software developers requiring to perform technical analysis of financial market data.

1 Installation

1.1 Download
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/
 
1.2 Install TA-LIB
If the next command fails, then gcc is missing, install it by doing “apt-get install build-essential”)
sudo ./configure
sudo make
sudo make install
 
1.3 Install TA-LIB Python Wrapper
Install TA-Lib Python Wrapper via pip (or pip3):
pip install ta-lib
 
1.4 Test
Try to import talib in your Python application:
import talib
 
If you get an error like below:
ImportError: libta_lib.so.0: cannot open shared object file: No such file or directory

You will need to do the following additional steps:
Do either export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH or for a permanent solution, you’ll have to add /usr/local/lib to /etc/ld.so.conf as root then run /sbin/ldconfig (also as root).
 
Finished.