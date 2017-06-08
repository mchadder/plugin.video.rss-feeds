import xbmcplugin, xbmcgui, xbmcaddon, urllib2, sys, urlparse
import xml.etree.ElementTree as etree

FEEDS = { 
          "DEFCON":{ "url":"https://www.youtube.com/feeds/videos.xml?channel_id=UC6Om9kAkl32dWlDSNlDS9Iw"},
          "BSides DC 2016": { "url":"https://www.youtube.com/feeds/videos.xml?channel_id=UCVImyGhRATNFGPmJfxaq1dw"},
          "EuroPython 2016": { "url":"https://www.youtube.com/feeds/videos.xml?playlist_id=PL8uoeex94UhE3FDvjacSlHFffoNEoPzzm" },
          "AppSec EU 2016": { "url":"https://www.youtube.com/feeds/videos.xml?playlist_id=PLpr-xdpM8wG-Kf1_BOnT2LFZU8_SXfpKL" },
          "EuroPython 2015": { "url":"https://www.youtube.com/feeds/videos.xml?playlist_id=PL8uoeex94UhGGUH0mFb-StlZ1WYGWiJfP" },
          "PyCon 2017": { "url":"https://www.youtube.com/feeds/videos.xml?channel_id=UCrJhliKNQ8g0qoE_zvL8eVg"},
          "PyCon 2016": { "url":"https://www.youtube.com/feeds/videos.xml?channel_id=UCwTD5zJbsQGJN75MwbykYNw"},
          "PyCon 2015": { "url":"https://www.youtube.com/feeds/videos.xml?channel_id=UCgxzjK6GuOHVKR_08TT4hJQ"},
          "IEEE Symposium on Security and Privacy": { "url":"https://www.youtube.com/feeds/videos.xml?channel_id=UC6pXMS7qre9GZW7A7FVM90Q" },
          "Nginx": {"url":"https://www.youtube.com/feeds/videos.xml?channel_id=UCy6gt7XvGJ3AGpSon2pS4nQ" },
          "OWASP": {"url":"https://www.youtube.com/feeds/videos.xml?channel_id=UCe8j61ABYDuPTdtjItD2veA" },
          "MongoDB": { "url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCK_m2976Yvbx-TyDLw7n1WA" },
          "TWiT - Security Now!": { "url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCNbqa_9xihC8yaV2o6dlsUg" },
          "TWiT - The Tech Guy": { "url":"https://www.youtube.com/feeds/videos.xml?channel_id=UCWAAgw0UiWLZqyA6eJzhbug" },
          "TWiT - The New Screensavers": { "url":"https://www.youtube.com/feeds/videos.xml?channel_id=UCFP9Euhwi3GqbQmWS-M-0hA" },
          "USENIX": {"url":"https://www.youtube.com/feeds/videos.xml?channel_id=UC4-GrpQBx6WCGwmwozP744Q"}
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
  url = [u for u in urls if "youtube.com" in u]
  id = ""
  try:
    url = url[0]
    paramArray = url.split("?")[1].split("&")
    for param in paramArray:
      name, value = param.split("=")
      if name == "v":
          id = value;

    addLink(title, "plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=%s"%id, "http://img.youtube.com/vi/%s/hqdefault.jpg"%id)
  except Exception as e:
    addLink(name="NOT youtube! %s"%title)

def processFeeds(feed_data, feed_type):
  if feed_type=='RSS':
    # Process an RSS feed first (channel/item)
    for itm in feed_data.findall("./channel/item"):
      title = ""
      urls = []
      for itmelems in itm:
        if itmelems.tag == "title":
          title = itmelems.text
        elif itmelems.tag == "link":
          urls.append(itmelems.text)
        elif itmelems.tag == "enclosure":
          urls.append(itmelems.attrib["url"])

      addVideoLink(title=title, urls=urls)
  elif feed_type=='ATOM':
    # Check for a possible ATOM feed
    ns = {"atom":"http://www.w3.org/2005/Atom"}
    for itm in feed_data.findall("./atom:entry",ns):
      urls = []
      title = ""
      for itmelems in itm:
        if itmelems.tag == "{%s}title"%ns["atom"]:
          title = itmelems.text
        elif itmelems.tag == "{%s}link"%ns["atom"]:
          urls.append(itmelems.attrib["href"])

      addVideoLink(title=title, urls=urls)

def showLinks(feed):
   try:
     xml = urllib2.urlopen(feed).read()
     root = etree.fromstring(xml)
       
     processFeeds(feed_data=root, feed_type="RSS")
     processFeeds(feed_data=root, feed_type="ATOM")
   except Exception as e:
       addLink(name="%s (%s)"%(e,"ShowLinks"))

def showFeeds():
   for key in FEEDS:
       addDir(name=key, path=key)

try:
    params = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)

    try:
        path = params["path"][0]
        showLinks(feed=FEEDS[path]["url"])
    except:
        showFeeds()

except Exception as e:
    addLink(name="%s"%e)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
