import urllib2

BUFFER_SIZE = 64 * 1024

class Downloader(object):
    """docstring for Downloader"""
    def __init__(self, url, filename):
        super(Downloader, self).__init__()
        self.url = url
        self.filename = filename

    def download(self):
        fout = open(self.filename, 'w')
        size = 0
        f = urllib2.urlopen(self.url)
        content_size = int(f.info()['Content-Length'])
        while size < content_size:
            transfert_size = min(BUFFER_SIZE, content_size - size)
            data = f.read(transfert_size)
            fout.write(data)
            size += transfert_size
            print "%d %d" % (size, content_size)

        fout.close()
        f.close()

if __name__ == '__main__':
    import sys
    downloader = Downloader(sys.argv[1], "toto.mp4")
    downloader.download()
