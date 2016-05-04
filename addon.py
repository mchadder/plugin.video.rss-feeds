import xbmcplugin, xbmcgui, xbmcaddon, urllib2, sys, urlparse
import xml.etree.ElementTree as etree

FEEDS = { 
          "PyVideo.org": { "url":"http://pyvideo.org/video/rss",
                           "img": None },
          "IEEE Symposium on Security and Privacy": { "url":"https://www.youtube.com/feeds/videos.xml?channel_id=UC6pXMS7qre9GZW7A7FVM90Q",
                                                      "img":None },
          "Nginx": {"url":"https://www.youtube.com/feeds/videos.xml?channel_id=UCy6gt7XvGJ3AGpSon2pS4nQ",
                    "img":None},
          "OWASP": {"url":"https://www.youtube.com/feeds/videos.xml?channel_id=UCe8j61ABYDuPTdtjItD2veA",
                    "img":None},
          "OWASP AppSec Tutorial Series": { "url": "https://www.youtube.com/feeds/videos.xml?channel_id=UC5xIEA6L0C2IG3iWgs8M2cA",
                                            "img": None },
          "MongoDB": { "url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCK_m2976Yvbx-TyDLw7n1WA",
                       "img": None },
          "Security Now!": { "url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCNbqa_9xihC8yaV2o6dlsUg",
                             "img": None },
          "Dan Boneh - Cryptography Lectures": { "url": "https://www.youtube.com/feeds/videos.xml?playlist_id=PL9oqNDMzcMClAPkwrn5dm7IndYjjWiSYJ",
                                                 "img": None }
        }

def addLink(name, url, img="DefaultVideo.png"):
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
    addLink("NOT youtube! %s"%title, "", "")

def showLinks(feed):
   try:
       xml = urllib2.urlopen(feed).read()
       root = etree.fromstring(xml)
       
       # Process an RSS feed first (channel/item)
       for itm in root.findall("./channel/item"):
         title = ""
         urls = []
         for itmelems in itm:
             if itmelems.tag == "title":
               title = itmelems.text
             elif itmelems.tag == "link":
               urls.append(itmelems.text)
             elif itmelems.tag == "enclosure":
               urls.append(itmelems.attrib["url"])
           
         addVideoLink(title, urls)
       
       # Check for a possible ATOM feed
       ns = {"atom":"http://www.w3.org/2005/Atom"}
       for itm in root.findall("./atom:entry",ns):
         urls = []
         title = ""
         for itmelems in itm:
           if itmelems.tag == "{%s}title"%ns["atom"]:
             title = itmelems.text
           elif itmelems.tag == "{%s}link"%ns["atom"]:
             urls.append(itmelems.attrib["href"])

         addVideoLink(title, urls)
   except Exception as e:
       addLink("%s (%s)"%(e,"ShowLinks()"),"")

def showFeeds():
   for key in FEEDS:
       addDir(key,key,FEEDS[key]["img"])

try:
    params = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query)

    try:
        path = params["path"][0]
        showLinks(FEEDS[path]["url"])
    except:
        showFeeds()

except Exception as e:
    addLink("%s"%e, "")

xbmcplugin.endOfDirectory(int(sys.argv[1]))
