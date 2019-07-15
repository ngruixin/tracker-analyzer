#!/bin/bash

# Adapted from: https://github.com/sebastianzillessen/WiFi-AP-Raspberry-Pi-3/blob/master/install.sh
# Usage: sudo ./install_ap.sh or sudo ./install_ap.sh <SSID> <PASSPHRASE> <IP_RANGE> <IN> <OUT>

# set name of access point to connect to (default: RDRTesting)
SSID="${1:-RDRTesting}"

# set password of access point to connect to (default: RDRTesting)
PASSPHRASE="${2:-RDRTesting}"

# set ip range assigned to devices connected to access point (default: 192.168.10.0/255)
IP_RANGE="${3:-192.168.10}"

# set network interface for incoming internet connection (default: eth0)
IN="${4:-eth0}"

# set network interface on which the wireless access point is hosted (default: wlan1)
OUT="${5:-wlan1}"


echo "Setting up your wireless access point with the following configurations:"
echo " SSID: $SSID"
echo " PASSPHRASE: $PASSPHRASE"
echo " IP-Address: $IP_RANGE.1"
echo " IP-Range: $IP_RANGE.0"
echo " Incomming network interface: $IN"
echo " WiFi interface: $OUT"

# update 
apt-get update

# install required modules 
apt-get -y install hostapd isc-dhcp-server iptables

# check if network interfaces are available

if ! ifconfig -a | grep "$OUT"; then
  echo "$OUT not found, exiting";
  exit -1
fi
if ! ifconfig -a | grep "$IN"; then
  echo "$IN not found, exiting";
  return -1
fi

# modify dhcp.conf
sed -i.bak 's/option domain-name/\#option domain-name/g' /etc/dhcp/dhcpd.conf
sed -i 's/option domain-name-servers ns1.example.org, ns2.example.org;/\#option domain-name-servers ns1.example.org, ns2.example.org;/g' /etc/dhcp/dhcpd.conf
sed -i 's/#authoritative;/authoritative;/g' /etc/dhcp/dhcpd.conf

# add ip addresses 
CONF="
subnet $IP_RANGE.0 netmask 255.255.255.0 {
  range $IP_RANGE.10 $IP_RANGE.20;
  option broadcast-address $IP_RANGE.255;
  option routers $IP_RANGE.1;
  default-lease-time 600;
  max-lease-time 7200;
  option domain-name "local-network";
  option domain-name-servers 8.8.8.8, 8.8.4.4;
}
"
echo "$CONF" >> /etc/dhcp/dhcpd.conf

# set where DHCP runs (for IPv4)
sed -i.bak "s/\(INTERFACESv4 *= *\).*/\1\"$OUT\"/" /etc/default/isc-dhcp-server

# set static ip address for interface on $OUT
INTERF_CONF="
auto lo
iface lo inet loopback

auto $IN
iface $IN inet dhcp

allow-hotplug $OUT
iface $OUT inet static
  address $IP_RANGE.1
  netmask 255.255.255.0
"
echo "$INTERF_CONF" > /etc/network/interfaces

sudo systemctl disable dhcpcd
sudo systemctl enable networking

# setup hostapd.conf
CONF_HOST="ssid=$SSID
wpa_passphrase=$PASSPHRASE
driver=nl80211
interface=$OUT
hw_mode=g
channel=6
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
rsn_pairwise=CCMP"
echo "$CONF_HOST" > /etc/hostapd/hostapd.conf

# deamon config
sed -i.bak 's/#DAEMON_CONF=""/DAEMON_CONF="\/etc\/hostapd\/hostapd.conf"/g' /etc/default/hostapd

# start up config 
sed -i.bak 's/#DAEMON_CONF=""/DAEMON_CONF="\/etc\/hostapd\/hostapd.conf"/g' /etc/init.d/hostapd

# add ip-forward=1
sudo sysctl -w net.ipv4.ip_forward=1
sudo sysctl -w net.ipv4.conf.all.send_redirects=0
sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"

#start wireless network 
sudo ifconfig $OUT up 

# test access point
echo "Installation complete!"

# start access point and dhcp server 
sudo service isc-dhcp-server start
sudo systemctl unmask hostapd
sudo service hostapd start

# enable acecss point on start up 
sudo update-rc.d hostapd enable 
sudo update-rc.d isc-dhcp-server enable


