import sys
import urllib2
import json
import re
import xml.etree.ElementTree as ET

from downloader import Downloader

def fixup_feed_xml(feed):
    lines = feed.splitlines()
    lines[1] = '<rss xmlns:dcterms="http://purl.org/dc/terms/" xmlns:arte="http://arte.fr/" xmlns:media="http://search.yahoo.com/mrss/" xmlns:atom="http://www.w3.org/2005/Atom" version="2.0">'
    feed = '\n'.join(lines)
    return feed

def _get_download_url(url):
    ns = {'media': 'http://search.yahoo.com/mrss/'}
    feed = urllib2.urlopen("http://www.arte.tv/papi/tvguide-flow/feeds/videos/fr.xml?type=ARTE_PLUS_SEVEN&player=false").read()
    feed = fixup_feed_xml(feed)
    root = ET.fromstring(feed)
    items = root.findall(".//item")
    for item in items:
        if item.find('link').text == url:
            return item.find(".//media:content[@bitrate='800']", ns).attrib['url']

    return None

def get_all_prg():
    ns = {'media': 'http://search.yahoo.com/mrss/'}
    feed = urllib2.urlopen("http://www.arte.tv/papi/tvguide-flow/feeds/videos/fr.xml?type=ARTE_PLUS_SEVEN&player=false").read()
    feed = fixup_feed_xml(feed)
    root = ET.fromstring(feed)
    items = root.findall(".//item")
    res = []
    for item in items:
        res.append({'title': item.find('title').text,
                    'description': item.find('description').text,
                    'url': item.find('link').text,
                    'poster_url': item.find(".//media:thumbnail", ns).attrib['url'],
                    'category': item.find('category').text,
                    'duration': int(item.find(".//media:content[@bitrate='800']", ns).attrib['duration']) * 60,
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

