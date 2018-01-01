import xbmcplugin, xbmcgui, urllib2, sys
import xml.etree.ElementTree as etree
from urlparse import parse_qsl

YOUTUBE_PLUGIN="plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=%s"
FEED_TYPES=["RSS", "RDF", "ATOM"]
FEEDS = {
          "Python": {
            "EuroPython 2017": "https://www.youtube.com/feeds/videos.xml?playlist_id=PL8uoeex94UhG9QAoRICebFpeKK2M0Herh",
            "EuroPython 2016": "https://www.youtube.com/feeds/videos.xml?playlist_id=PL8uoeex94UhE3FDvjacSlHFffoNEoPzzm",
            "EuroPython 2015": "https://www.youtube.com/feeds/videos.xml?playlist_id=PL8uoeex94UhGGUH0mFb-StlZ1WYGWiJfP",
            "PyCon 2017": "https://www.youtube.com/feeds/videos.xml?channel_id=UCrJhliKNQ8g0qoE_zvL8eVg",
            "PyCon 2016": "https://www.youtube.com/feeds/videos.xml?channel_id=UCwTD5zJbsQGJN75MwbykYNw",
            "PyCon 2015": "https://www.youtube.com/feeds/videos.xml?channel_id=UCgxzjK6GuOHVKR_08TT4hJQ"
          },
          "AppSec": {
            "AppSec EU 2016": "https://www.youtube.com/feeds/videos.xml?playlist_id=PLpr-xdpM8wG-Kf1_BOnT2LFZU8_SXfpKL",
            "IEEE Symposium on Security and Privacy": "https://www.youtube.com/feeds/videos.xml?channel_id=UC6pXMS7qre9GZW7A7FVM90Q",
            "OWASP": "https://www.youtube.com/feeds/videos.xml?channel_id=UCe8j61ABYDuPTdtjItD2veA"
          },
          "Hacking": {
            "CCC - 34C3": "https://media.ccc.de/updates.rdf",
            "DEFCON":"https://www.youtube.com/feeds/videos.xml?channel_id=UC6Om9kAkl32dWlDSNlDS9Iw",
            "BSides DC 2016": "https://www.youtube.com/feeds/videos.xml?channel_id=UCVImyGhRATNFGPmJfxaq1dw",
            "USENIX": "https://www.youtube.com/feeds/videos.xml?channel_id=UC4-GrpQBx6WCGwmwozP744Q",
            "Black Hat": "https://www.youtube.com/feeds/videos.xml?user=BlackHatOfficialYT",
            "Black Hat USA 2017": "https://www.youtube.com/feeds/videos.xml?playlist_id=PLH15HpR5qRsUyGhBVRDKGrHyQC5G4jQyd"
          },
          "Database": {
            "AskTOM TV": "https://www.youtube.com/feeds/videos.xml?playlist_id=PLJMaoEWvHwFKP7uF4l1pXIqMEJ_RatDSq",
            "Oracle Developers": "https://www.youtube.com/feeds/videos.xml?channel_id=UCdDhYMT2USoLdh4SZIsu_1g",
            "MongoDB": "https://www.youtube.com/feeds/videos.xml?channel_id=UCK_m2976Yvbx-TyDLw7n1WA"
          },
          "Linux": {
            "Linux Training Academy": "https://www.youtube.com/feeds/videos.xml?user=linuxtrainingacademy"
          },
          "Nginx": {
            "Nginx": "https://www.youtube.com/feeds/videos.xml?channel_id=UCy6gt7XvGJ3AGpSon2pS4nQ",
            "Nginx Inc.": "https://www.youtube.com/feeds/videos.xml?user=NginxInc"
          }
        }

def addLink(name, url="", img="DefaultVideo.png"):
    li = xbmcgui.ListItem(name, iconImage=img)
    li.setProperty("IsPlayable", "true")
    li.setInfo(type="Video", infoLabels={"Title":"%s"%name})
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=li, isFolder=False)

def addDir(name, path, img="DefaultFolder.png"):
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
      addLink(name=title, url=YOUTUBE_PLUGIN%id)
    elif ".mp4" in u:
      addLink(name=title, url=u)

def processFeeds(feed_data, feed_type):
  ns = {"atom":"http://www.w3.org/2005/Atom",
        "rdf":"http://purl.org/rss/1.0/"}

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
    for itm in feed_data.findall("./atom:entry", ns):
      title=""
      urls=[]
      for itmelems in itm:
        if itmelems.tag == "{%s}title"%ns["atom"]:
          title = itmelems.text
        elif itmelems.tag == "{%s}link"%ns["atom"]:
          urls.append(itmelems.attrib["href"])
      addVideoLink(title=title, urls=urls)
  elif feed_type=='RDF':
    for itm in feed_data.findall("./rdf:item", ns):
      title=""
      urls=[]
      for itmelems in itm:
        if itmelems.tag == "{%s}title"%ns["rdf"]:
          title = itmelems.text
        elif itmelems.tag == "{%s}link"%ns["rdf"]:
          urls.append(itmelems.text)
      addVideoLink(title=title, urls=urls)

def showLinks(feed):
   try:
     xml = urllib2.urlopen(feed).read()
     root = etree.fromstring(xml)

     for ft in FEED_TYPES:
       processFeeds(feed_data=root, feed_type=ft)
   except Exception as e:
       addLink(name="%s (%s)"%(e,"ShowLinks"))

def showFeeds(path):
   if path in FEEDS:
     for key in FEEDS[path]:
       addDir(name=key, path="%s:%s"%(path,key))
   elif path == "":
     for key in FEEDS:
       addDir(name=key, path=key)
   else:
     category,feed = path.split(":")
     showLinks(feed=FEEDS[category][feed])

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

    showFeeds(path=path)
  except Exception as e:
    addLink(name="ERROR: %s"%e)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
