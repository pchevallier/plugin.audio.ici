# https://docs.python.org/2.7/
import os
import sys
import urllib
import urlparse
import xbmcaddon
import xbmcgui
import xbmcplugin
import re
import urllib2
from HTMLParser import HTMLParser

def build_url(query):
    base_url = sys.argv[0]
    return base_url + '?' + urllib.urlencode(query)
    
def get_page(url):
    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
    headers = { 'User-Agent' : user_agent }
    req = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req)
    page = response.read()
    response.close()
    return page
    
def parse_page(page):
    streams = {}
    # hard coded for now
    streams['ICI Musique - Montreal'] = "http://7qmtl0.akacast.akamaistream.net/7/445/177407/v1/rc.akacast.akamaistream.net/7QMTL0"
    streams['ICI Musique - Vancouver'] = "http://7bvan0.akacast.akamaistream.net/7/286/177417/v1/rc.akacast.akamaistream.net/7BVAN0"
    return streams
    
def build_stream_list(streams):
    stream_list = []
    for city, station in sorted(streams.items()):
    	#xbmc.log('stream:' + str(city) +'=>'+ str(station), xbmc.LOGNOTICE)
        # create a list item for the label
        li = xbmcgui.ListItem(label=city)
        # set list item mediatype
        li.setInfo('video', { 'studio': 'cbc', 'mediatype': 'video' })
        # set the list item to playable
        li.setProperty('IsPlayable', 'true')
        # build the plugin url for Kodi
        url = build_url({'mode': 'stream', 'url': station, 'title': city})
        # add the current list item to a list
        stream_list.append((url, li, False))

    # add list to Kodi per Martijn
    xbmcplugin.addDirectoryItems(addon_handle, stream_list, len(stream_list))
    # set the content of the directory
    xbmcplugin.setContent(addon_handle, 'videos')
    xbmcplugin.endOfDirectory(addon_handle)
    
def play_stream(url):
    # set the path of the station to a list item
    play_item = xbmcgui.ListItem(path=url)
    # the list item is ready to be played by Kodi
    xbmcplugin.setResolvedUrl(addon_handle, True, listitem=play_item)
    
def main():
    args = urlparse.parse_qs(sys.argv[2][1:])
    mode = args.get('mode', None)
    
    #xbmc.log('ici addon: arg ' + str(sys.argv), xbmc.LOGNOTICE)
    # initial launch of add-on
    if mode is None:
        page = get_page('http://www.cbc.ca/radio/includes/stream.html')
        content = parse_page(page)
        build_stream_list(content)
    # a station from the list has been selected
    elif mode[0] == 'stream':
        play_stream(args['url'][0])
    
if __name__ == '__main__':   
    addon_handle = int(sys.argv[1])
    main()
