# Usage: python3 web_analyze.py <file path> 
# Example: python3 web_analyze.py /Users/ruixin/Desktop/cs/capstone/tracker-analyzer/data/www.tumblr.com.har

import json 
from urllib.parse import urlparse, unquote
from tracker import Tracker, http_headers, http2_headers
import sys

class WebTracker(Tracker):
	'''
	A subclass of Tracker that extracts the relevant information
	from a HAR file. 
	'''

	def update(self, entry):
		'''
		Implements the update method of the parent Tracker class. 

		@params:
			entry is a json object that corresponds to a network request.
				  It is an element of the entries list in a HAR file. 
		'''
		url_unparsed = entry["request"]["url"]
		if url_unparsed[:5] == "https":
			self.isSSL = True
		url = urlparse(entry["request"]["url"])
		self.domain = url.netloc
		q = unquote(url.query)
		if q not in self.uris and url.query != "":
			self.uris.append(q)
		cookies = entry["request"]["cookies"]
		for cookie in cookies:
			new_c = cookie["name"] + "=" + cookie["value"]
			if new_c not in self.cookies:
				self.cookies.append(new_c)
		if entry["request"]["method"] == "POST":
			self.update_data(entry)
		headers = entry["request"]["headers"]
		for header in headers:
			if header["name"].lower() not in http_headers \
			and header["name"].lower() not in http2_headers: 
				h = header["name"].lower() + ": " + header["value"]
				if h not in self.headers:
					self.headers.append(h)

	def update_data(self, entry):
		'''
		Gets the data sent in a POST request (both the text sent as well
		as the parameters of of the request). Updates the data attribute
		of the object. 

		@params:
			entry is a json object that corresponds to a network request.
				  It is an element of the entries list in a HAR file. 
		'''
		if "postData" in entry["request"].keys():
			postData = entry["request"]["postData"]
			text = unquote(postData["text"])
			#params = postData["params"]
			if text != "" and text not in self.data:
				self.data.append(text)

def get_existing_tracker(trackers, ip):
	'''
	Returns the tracker in list @param trackers that has @param ip.
	If such a tracker does not exist, return None. 
	'''
	for tracker in trackers:
		if tracker.get_ip() == ip:
			return tracker
	return None

def analyze_web(path):
	'''
	Parses the HAR file and extracts a list of trackers. If a tracker 
	with a corresponding IP already exists in the list, adds the entry 
	information to the existing tracker object. Prints out the list
	of trackers. 

	@params:
		path is the file path to the HAR file (json object).
	'''
	with open(path, 'r+') as f:
	    data = json.load(f)
	entries = data["log"]["entries"]
	trackers = []
	for entry in entries:
		server_ip = entry["serverIPAddress"]
		t = get_existing_tracker(trackers, server_ip)
		if t is not None: 
			t.update(entry)
		else:
			new_t = WebTracker(server_ip, entry)
			trackers.append(new_t)
	print(*trackers, sep = "\n") 

if __name__ == "__main__":
	analyze_web(sys.argv[1])
