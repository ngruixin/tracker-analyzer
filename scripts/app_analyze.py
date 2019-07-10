import pyshark
from pprint import pprint
from hpack import Encoder, Decoder
from tracker import Tracker, http_headers, http2_headers

class AppTracker(Tracker):
	'''
	A subclass of Tracker that extracts the relevant information
	from a pcap traffic capture. 
	'''

	def update(self, packet):
		'''
		Implements the update method of the parent Tracker class.

		@params:
			packet is a network packet captured. 
		'''
		layer = packet.layers[1].layer_name
		if layer == "http": 
			print(packet.http.user_agent)
			self.update_http(packet)
		elif layer == "http2" and "HEADER" in packet.http2.stream:
			self.update_http2(packet)
		#TODO: figure out how to extract post data http2

	def update_http(self, packet):
		'''
		Updates the AppTracker with the relevant information (domain 
		name, cookies, post data, and uri query parameters) from the 
		http packet capture.

		@params:
			packet is a http packet. 
		'''
		fields = packet.http.field_names
		if "host" in fields: 
			self.domain = packet.http.host 
		if "cookie" in fields: 
			c = packet.http.cookie
			if c not in self.cookies:
				self.cookies.append(c)
		if "file_data" in fields: 
			data = packet.http.file_data
			if data not in self.data:
				self.data.append(data)
		if "request_uri_query" in fields: 
			uri = packet.http.request_uri_query
			if uri not in self.uris:
				self.uris.append(uri)
		#for i in range(len(fields)):
		#	field = fields[i]
		#	if field not in http2_headers \
		#	and field not in http2_headers:
		#	h = field + ": " + packet.http
		#	self.headers.append()
		#TODO: include custom header information

	def update_http2(self, packet):
		'''
		Decodes the http2 header and updates the AppTracker with 
		the relevant information (domain name, cookies, post data, 
		custom headers, and uri query parameters) from the http2
		packet capture. Ignores any packet that fails to decode. 

		@params:
			packet is a http2 header packet. 
		'''
		try: 
			d = Decoder()
			decoded_headers = d.decode(bytes.fromhex(packet.http2.headers.raw_value))
			#print(decoded_headers)
			for (key, value) in decoded_headers:
				if key == ":authority":
					self.domain = value
				elif key == ":path":
					idx = value.find('?')
					if idx != -1:
						params = value[idx+1:]
						if params not in self.uris:
							self.uris.append(params)
				elif key == "cookie":
					if value not in self.cookies:
						self.cookies.append(value)
				elif key.lower() not in http_headers \
				and key.lower() not in http2_headers: 
					h = key.lower() + ": " + value
					if h not in self.headers:
						self.headers.append(h)
				elif key == "user_agent":
					print(value)
		except Exception as e:
			#print(e)
			pass

def get_existing_tracker(trackers, ip):
	'''
	Returns the tracker in list @param trackers that has @param ip.
	If such a tracker does not exist, return None. 
	'''
	for tracker in trackers:
		if tracker.get_ip() == ip:
			return tracker
	return None

def analyze_app(path, host_ip):
	'''
	Parses the pcap file and extracts a list of trackers. Ignores 
	packets corresponding to the local host IP. If a tracker with 
	a corresponding IP already exists in the list, adds the packet 
	information to the existing tracker object. Prints out the list
	of trackers. 

	@params:
		path is the file path to the pcap file.
		host_ip is the IP address of the host machine.
	'''
	cap = pyshark.FileCapture(path)
	#pprint(vars(cap[0]))
	#pprint(vars(cap[0].http2))
	trackers = []
	for packet in cap:
		server_ip = packet.exported_pdu.ipv4_dst
		src_ip = packet.exported_pdu.ipv4_src
		if src_ip != host_ip:
			continue
		layer = packet.layers[1].layer_name
		if layer == "http2" or layer == "http":
			t = get_existing_tracker(trackers, server_ip)
			if t is None:
				t = AppTracker(server_ip, packet)
				trackers.append(t)
			else:
				t.update(packet)
	print(*trackers, sep = "\n") 

if __name__ == "__main__":
	analyze_app('/Users/ruixin/Desktop/kali/instagram.pcapng', "192.168.10.10")
