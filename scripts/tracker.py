# list of standard http header
# from https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers
http_headers = [
	"Age",
	"Cache-Control",
	"Clear-Site-Data",
	"Expires",
	"Pragma",
	"Warning",
	"Accept-CH",
	"Accept-CH-Lifetime",
	"Early-Data",
	"Content-DPR",
	"DPR",
	"Save-Data",
	"Viewport-Width",
	"Width",
	"Last-Modified",
	"ETag",
	"If-Match",
	"If-None-Match",
	"If-Modified-Since",
	"If-Unmodified-Since",
	"Vary",
	"Connection",
	"Keep-Alive",
	"Accept",
	"Accept-Charset",
	"Accept-Encoding",
	"Accept-Language",
	"Expect",
	"Max-Forwards",
	"Cookie",
	"Set-Cookie",
	"Cookie2",
	"Set-Cookie2",
	"Access-Control-Allow-Origin",
	"Access-Control-Allow-Credentials",
	"Access-Control-Allow-Headers",
	"Access-Control-Allow-Methods",
	"Access-Control-Expose-Headers",
	"Access-Control-Max-Age",
	"Access-Control-Request-Headers",
	"Access-Control-Request-Method",
	"Origin",
	"Timing-Allow-Origin",
	"X-Permitted-Cross-Domain-Policies",
	"DNT",
	"Tk",
	"Content-Disposition",
	"Content-Length",
	"Content-Type",
	"Content-Encoding",
	"Content-Language",
	"Content-Location",
	"Forwarded",
	"X-Forwarded-For",
	"X-Forwarded-Host",
	"X-Forwarded-Proto",
	"Via",
	"Location",
	"From",
	"Host",
	"Referer",
	"Referrer-Policy",
	"User-Agent",
	"Allow",
	"Server",
	"Accept-Ranges",
	"Range",
	"If-Range",
	"Content-Range",
	"Cross-Origin-Resource-Policy",
	"Content-Security-Policy",
	"Content-Security-Policy-Report-Only",
	"Expect-CT",
	"Public-Key-Pins",
	"Public-Key-Pins-Report-Only",
	"Strict-Transport-Security",
	"Upgrade-Insecure-Requests",
	"X-Content-Type-Options",
	"X-Download-Options",
	"X-Powered-By",
	"X-XSS-Protection",
	"Last-Event-ID",
	"NEL",
	"Ping-From",
	"Ping-To",
	"Report-To",
	"Transfer-Encoding",
	"TE",
	"Trailer",
	"Sec-WebSocket-Key",
	"Sec-WebSocket-Extensions",
	"Sec-WebSocket-Accept",
	"Sec-WebSocket-Protocol",
	"Sec-WebSocket-Version",
	"Accept-Push-Policy",
	"Accept-Signature",
	"Alt-Svc",
	"Date",
	"Large-Allocation",
	"Push-Policy",
	"Retry-After",
	"Signature",
	"Signed-Headers",
	"Server-Timing",
	"SourceMap",
	"Upgrade",
	"X-DNS-Prefetch-Control",
	"X-Firefox-Spdy",
	"X-Pingback",
	"X-Requested-With",
	"X-Robots-Tag",
	"X-UA-Compatible"
]

http2_headers = [
	":method", 
	":authority",
	":scheme",
	":path",
	":status"
]

# http header names in lower case 
http_headers = [x.lower() for x in http_headers]

class Tracker:
	'''
	A representation of a first- or third-party domain along with the
	data that is being sent to the domain. 

	@params:
		 self.domain is the hostname that receives the network request
		 self.ip is the ip address of the domain 
		 self.uris is a list of URI paths made to the domain
		 self.cookies is a list of cookies that are sent to the domain
		 self.data is a list of post data that is sent to the domain 
		 self.headers is a list of headers included in the network
		 	request that is not a standard http header  
	'''

	def __init__(self, ip, entry):
		'''
		Creates a tracker object with the corresponding attributes
		using fields in @param entry. Only updates self.data if the
		@param entry refers to a POST request. 

		@params:
			entry is a object that contains the trackers information. 
		'''
		self.domain = ""
		self.ip = ip
		self.uris = []
		self.cookies = []
		self.data = []
		self.headers = []
		self.isSSL = False
		self.update(entry)

	def get_ip(self):
		'''
		Returns the IP address of the tracker. 
		'''
		return self.ip 

	def update(self, entry):
		'''
		Updates the tracker's list of URIs, cookies and data with 
		values from @param entry. Abstract method that should be 
		implemented by child class, raises an exception otherwise. 

		@params:
			entry is a object that contains the trackers information. 
		'''
		raise NotImplementedError


	def str_list(self, l):
		'''
		Returns a prettified string representation of list @param l
		'''
		s = "["
		for i in range(len(l)):
			if i != len(l) - 1:
				s += "\n	" + str(l[i]) + ", "
			else: 
				s += "\n	" + str(l[i]) + "\n"
		s += "]"
		return s

	def __str__(self): 
		'''
		Overrides the default string representation of the object. 
		'''
		s = "Domain: " + self.domain + " (" + self.ip + ") \n" + \
			"URI Params: " + self.str_list(self.uris) + "\n" + \
			"Cookies: " + self.str_list(self.cookies) + "\n" + \
			"Post Data: " + self.str_list(self.data) + "\n" + \
			"Custom Headers: " + self.str_list(self.headers) + "\n" + \
			"Is Encrypted: " + str(self.isSSL) + "\n"
		return s