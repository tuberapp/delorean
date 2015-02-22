wget --no-check-certificate https://bootstrap.pypa.io/get-pip.py
python get-pip.py
pip install requests
echo "src mraa-upm http://iotdk.intel.com/repos/1.1/intelgalactic" > /etc/opkg/mraa-upm.conf
opkg update
opkg upgrade
mkdir /tuber
