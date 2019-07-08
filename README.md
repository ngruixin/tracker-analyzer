# tracker-analyzer

Analyzing data sent to first- and third-party domains on both web and mobile sites. 

# Requirements

Raspberry Pi 
Wireless USB adapter 
Wireshark 

# Current Setup
Raspberry Pi 3 installed with Raspbian Stretch Lite (2018-11-13) with a TL-WN722N wireless adapter. 

# Setup 

Install Raspbian OS on the Raspberry Pi. 

On the Raspberry Pi, enable it to work as an access point (AP) by running the installation scripts provided in /setup. 
```
sudo ./install_ap.sh <SSID> <PASSPHRASE> <IP_RANGE> <IN> <OUT>
```
whereby SSID refers to the name of the AP to be created, PASSPHRASE is the password used to connect to the AP, IP_RANGE is the subnet range allocated to devices connected to the AP, IN is the input interface from which the Raspberry Pi connects to the internet, and OUT is the output interface that broadcasts the WiFi signals (in this case, the network interface of the USB adapter. If none of the parameters are provided, the default configuration will be used (SSID: RDRTesting, passphrase: RDRTesting). 

Install mitmproxy and tshark on the Raspberry Pi by running the following command. 
```
sudo ./install_mitm.sh 
```

Reboot the device. 
```
sudo reboot
```
