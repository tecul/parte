import urllib2
import subprocess

class Curl(object):
	"""docstring for Curl"""
	def __init__(self, url, filename, timeout = 0):
		super(Curl, self).__init__()
		self.url = url
		self.filename = filename
		self.timeout = timeout
	
	def _getContentSize(self):
		return urllib2.urlopen(self.url).info()['Content-Length']

	def download(self):
		contentSize = self._getContentSize()
		cmd = ['curl', self.url, '-O', self.filename]
		p = subprocess.Popen(cmd, stderr=subprocess.PIPE, universal_newlines=True)
		print "here"
		output = p.stderr
		print output
		print "here2"
		for line in iter(output.readline, ""):
			print line,

if __name__ == '__main__':
	import sys
	curl = Curl(sys.argv[1], "toto.mp4")
	curl.download()
