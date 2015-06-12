import sys
import urllib2
import json
import re

from downloader import Downloader

bitrate2index = {"800": "HTTP_MP4_MQ_1",
                 "1500": "HTTP_MP4_EQ_1",
                 "2200": "HTTP_MP4_SQ_1"}

def _get_download_url(url, bitrate="800"):
    res = re.search('http://www.arte.tv/guide/fr/([\d-]+)/', url)
    if res:
        json_url = "http://arte.tv/papi/tvguide/videos/stream/player/F/%s_PLUS7-F/ALL/ALL.json" % res.group(1)
        playlist = json.loads(urllib2.urlopen(json_url).read())
        #print json.dumps(playlist['videoJsonPlayer']["VSR"][bitrate2index[bitrate]], sort_keys=True, indent=4, separators=(',', ': '))
        return playlist['videoJsonPlayer']["VSR"][bitrate2index[bitrate]]['url']
    res = re.search('vid=([\d-]+)', url)
    if res:
        json_url = "http://arte.tv/papi/tvguide/videos/stream/player/F/%s_PLUS7-F/ALL/ALL.json" % res.group(1)
        playlist = json.loads(urllib2.urlopen(json_url).read())
        #print json.dumps(playlist['videoJsonPlayer']["VSR"][bitrate2index[bitrate]], sort_keys=True, indent=4, separators=(',', ': '))
        return playlist['videoJsonPlayer']["VSR"][bitrate2index[bitrate]]['url']

    return ""

def get_all_prg():
    raw = urllib2.urlopen("http://www.arte.tv/guide/fr/plus7.json?page=1&per_page=1000").read()
    videos = json.loads(raw)['videos']
    res = []
    for video in videos:
        res.append({'title': video['title'],
                    'description': video['desc'],
                    'url': video['url'],
                    'poster_url': video['image_url'],
                    'category': 'unknown',
                    'duration': video['duration'] * 60,
                    'channel': 'arte'})

    return json.dumps(res, sort_keys=True, indent=4, separators=(',', ': '))

def get_download_url(url):
    return _get_download_url(url)

def download_prg(url, output_filename):
    download_url = _get_download_url(url)
    downloader = Downloader(download_url, output_filename)
    downloader.download()

if __name__ == '__main__':
    if len(sys.argv) == 1:
        json_res = get_all_prg()
        print json_res
    elif len(sys.argv) == 2:
        url = sys.argv[1]
        print get_download_url(url)
    elif len(sys.argv) == 3:
        url = sys.argv[1]
        output_filename = sys.argv[2]
        download_prg(url, output_filename)

