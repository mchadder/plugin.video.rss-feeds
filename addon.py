import xbmcplugin, xbmcgui, xbmcaddon, urllib2, sys
import xml.etree.ElementTree as etree
from urlparse import parse_qsl

FEEDS = {
          "CCC - 34C3": "https://media.ccc.de/updates.rdf",
          "DEFCON":"https://www.youtube.com/feeds/videos.xml?channel_id=UC6Om9kAkl32dWlDSNlDS9Iw",
          "BSides DC 2016": "https://www.youtube.com/feeds/videos.xml?channel_id=UCVImyGhRATNFGPmJfxaq1dw",
          "EuroPython 2016": "https://www.youtube.com/feeds/videos.xml?playlist_id=PL8uoeex94UhE3FDvjacSlHFffoNEoPzzm" ,
          "AppSec EU 2016": "https://www.youtube.com/feeds/videos.xml?playlist_id=PLpr-xdpM8wG-Kf1_BOnT2LFZU8_SXfpKL" ,
          "EuroPython 2015": "https://www.youtube.com/feeds/videos.xml?playlist_id=PL8uoeex94UhGGUH0mFb-StlZ1WYGWiJfP" ,
          "PyCon 2017": "https://www.youtube.com/feeds/videos.xml?channel_id=UCrJhliKNQ8g0qoE_zvL8eVg",
          "PyCon 2016": "https://www.youtube.com/feeds/videos.xml?channel_id=UCwTD5zJbsQGJN75MwbykYNw",
          "PyCon 2015": "https://www.youtube.com/feeds/videos.xml?channel_id=UCgxzjK6GuOHVKR_08TT4hJQ",
          "IEEE Symposium on Security and Privacy": "https://www.youtube.com/feeds/videos.xml?channel_id=UC6pXMS7qre9GZW7A7FVM90Q",
          "Nginx": "https://www.youtube.com/feeds/videos.xml?channel_id=UCy6gt7XvGJ3AGpSon2pS4nQ",
          "OWASP": "https://www.youtube.com/feeds/videos.xml?channel_id=UCe8j61ABYDuPTdtjItD2veA",
          "MongoDB":  "https://www.youtube.com/feeds/videos.xml?channel_id=UCK_m2976Yvbx-TyDLw7n1WA",
          "TWiT - Security Now!":  "https://www.youtube.com/feeds/videos.xml?channel_id=UCNbqa_9xihC8yaV2o6dlsUg",
          "TWiT - The Tech Guy": "https://www.youtube.com/feeds/videos.xml?channel_id=UCWAAgw0UiWLZqyA6eJzhbug",
          "TWiT - The New Screensavers": "https://www.youtube.com/feeds/videos.xml?channel_id=UCFP9Euhwi3GqbQmWS-M-0hA",
          "USENIX": "https://www.youtube.com/feeds/videos.xml?channel_id=UC4-GrpQBx6WCGwmwozP744Q"
        }

def addLink(name, url="", img="DefaultVideo.png"):
    li = xbmcgui.ListItem(name, iconImage=img)
    li.setProperty("IsPlayable", "true")
    li.setInfo(type="Video", infoLabels={"Title":"%s"%name})
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=li, isFolder=False)

def addDir(name,path,img="DefaultFolder.png"):
    u=sys.argv[0]+"?path=%s"%path
    li=xbmcgui.ListItem(name, iconImage=img)
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=li,isFolder=True)

def addVideoLink(title, urls):
  for u in urls:
    if "youtube.com" in u:
      id = ""
      paramArray = u.split("?")[1].split("&")
      for param in paramArray:
        name,value = param.split("=")
        if name == "v":
          id = value
      addLink(name=title, url="plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=%s"%id)
    elif ".mp4" in u:
      addLink(name=title, url=u)

def processFeeds(feed_data, feed_type):
  if feed_type=='RSS':
    for itm in feed_data.findall("./channel/item"):
      title=""
      urls=[]
      for itmelems in itm:
        if itmelems.tag == "title":
          title = itmelems.text
        elif itmelems.tag == "link":
          urls.append(itmelems.text)
        elif itmelems.tag == "enclosure":
          urls.append(itmelems.attrib["url"])
      addVideoLink(title=title, urls=urls)
  elif feed_type=='ATOM':
    ns = {"atom":"http://www.w3.org/2005/Atom"}
    for itm in feed_data.findall("./atom:entry",ns):
      title=""
      urls=[]
      for itmelems in itm:
        if itmelems.tag == "{%s}title"%ns["atom"]:
          title = itmelems.text
        elif itmelems.tag == "{%s}link"%ns["atom"]:
          urls.append(itmelems.attrib["href"])
      addVideoLink(title=title, urls=urls)
  elif feed_type=='RDF':
    ns = {"rss":"http://purl.org/rss/1.0/"}
    for itm in feed_data.findall("./rss:item", ns):
      title=""
      urls=[]
      for itmelems in itm:
        if itmelems.tag == "{%s}title"%ns["rss"]:
          title = itmelems.text
        elif itmelems.tag == "{%s}link"%ns["rss"]:
          urls.append(itmelems.text)
      addVideoLink(title=title, urls=urls)

def showLinks(feed):
   try:
     xml = urllib2.urlopen(feed).read()
     root = etree.fromstring(xml)

     processFeeds(feed_data=root, feed_type="RSS")
     processFeeds(feed_data=root, feed_type="ATOM")
     processFeeds(feed_data=root, feed_type="RDF")
   except Exception as e:
       addLink(name="%s (%s)"%(e,"ShowLinks"))

def showFeeds():
   for key in FEEDS:
       addDir(name=key, path=key)

def getDictVal(d, v):
  try:
    return d[v]
  except:
    return ""

if __name__ == '__main__':
  try:
    paramstring = sys.argv[2]
    params = dict(parse_qsl(paramstring[1:]))

    path = getDictVal(d=params, v="path")

    if path == "":
      showFeeds()
    else:
      showLinks(feed=FEEDS[path])

  except Exception as e:
    addLink(name="%s"%e)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
