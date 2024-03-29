# tracker-analyzer

Analyzing data sent to first- and third-party domains on both websites and mobile applications. 

# Requirements

* Raspberry Pi 

* Wireless USB adapter 

* Laptop with Wireshark and Google Chrome installed 

# Current Setup

Raspberry Pi 3 installed with Raspbian Stretch Lite (2018-11-13) with a TL-WN722N wireless adapter. 

# App Analysis 

## Setup 

Install Raspbian OS on the Raspberry Pi. 

On the Raspberry Pi, enable it to work as an access point (AP) by running the installation scripts provided in /setup. 
```
sudo ./install_ap.sh <SSID> <PASSPHRASE> <IP_RANGE> <IN> <OUT>
```
Example:
```
sudo ./install_ap.sh wifiname wifipassword 192.168.1 eth0 wlan0 
```
whereby SSID refers to the name of the AP to be created, PASSPHRASE is the password used to connect to the AP, IP_RANGE is the first 3 octets of the subnet range allocated to devices connected to the AP (eg 192.168.1), IN is the input interface from which the Raspberry Pi connects to the internet, and OUT is the output interface that broadcasts the WiFi signals (in this case, the network interface of the USB adapter. If none of the parameters are provided, the default configuration will be used (SSID: RDRTesting, passphrase: RDRTesting). 

Install mitmproxy and tshark on the Raspberry Pi by running the following command. 
```
sudo ./install_mitm.sh 
```

Reboot the device and ensure that the AP is up and running (can connect without internet access) 
```
sudo reboot
```

## Data Capture  

On the Pi, run the following commands:
```
pyenv activate mitm
nohup sudo tshark -w <FILENAME> -i <OUT> &
mitmdump --mode transparent --showhost 
```
where FILENAME is the name of the traffic capture file to be created and OUT is the network interface of the wireless adapter. 

On the mobile device, disable background app refresh and close all applications. Connect the mobile device to the AP that was setup on the Raspberry Pi. 

Visit the website www.mitm.it, select the relevant icon that corresponds to the operating system of the mobile device and follow the instructions provided. 

After successfully installing the certificate, the Pi should be successfully intercepting network traffic from the mobile device. Close the browser on the mobile device and access the app to be tested. 

To terminate the capture, hit CTRL-C on the Pi and kill the tshark process. Then run 
```sudo chmod 555 <FILENAME>```

## Data Analysis 

To analyze the data collected, obtain the data collected from the Pi on a laptop. 
```
sudo scp pi@<IP>:<FILE PATH> . 
sudo scp pi@<IP>:/home/pi/.mitmproxy/sslkeylogfile.txt . 
```
whereby IP refers to the IP address of the Raspberry Pi and FILE PATH is the path to the data previously captured. 

On wireshark, open the capture file and decrypt the SSL traffic:

*Edit -> Preferences -> Protocols -> SSL -> (Pre)-Master-Secret log filename*

Set (Pre)-Master-Secret log filename to the sslketlogfile.txt that was obtained. 
Extract and save packet captures related to HTTP(S) protocol:

*File -> Export PDUs to File... (select OS Layer 7) -> Save the packet capture.* 

*Note: If you are unable to save (button is greyed out), overwrite a .pcapng file or save to the /tmp directory and it should work (it is probably a permissions issue). 

Run the following command to extract the relevant data:
```
python3 app_analyis.py <FILE PATH> <HOST IP>
```
where FILE PATH is a path to the traffic capture and HOST IP is the IP address of the device running the test. 
  
Manually analyze the output to classify the type of user data sent. 

# Web Analysis
1. Open Google Chrome.
2. From the Chrome menu bar select View > Developer > Developer Tools.
3. From the panel opened, select the Network tab.
4. Check the box Preserve log.
5. Visit the website to audit. 
6. Right-click anywhere on the grid of network requests, select Save as HAR with Content, and save the file to your computer.
7. Run the command `python3 web_analyis.py <FILE PATH>` 
8. Manually analyze the output to classify the type of user data sent. 
