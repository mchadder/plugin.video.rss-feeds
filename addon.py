import xbmcplugin, xbmcgui, xbmcaddon, urllib2, sys, urlparse
import xml.etree.ElementTree as etree

FEEDS = { 
          "SecurityTube": { "url":"http://www.youtube.com/feeds/videos.xml?channel_id=UCBRNlyf9lURksAEnM-pyQdA",
                            "img":"https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcSHKtoYWyTShWr9a4jAvnCmgkqFRRg39BaBDQaxA1KB34rBead8" },
          "PyVideo.org": { "url":"http://pyvideo.org/video/rss",
                           "img":"https://duckduckgo.com/i/a61af354.png" }
        }

def addLink(name, url, img="DefaultVideo.png"):
    li = xbmcgui.ListItem(name, iconImage=img)
    li.setProperty("IsPlayable", "true")
    li.setInfo(type="Video", infoLabels={"Title":"%s"%name, "Plot":"Hello there", "Tagline":"Label222", "PlotOutline":"Hellodingle"})
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
       urls = []
       title = ""
       # Process an RSS feed first (channel/item)
       for itm in root.findall("./channel/item"):
         for itmelems in itm:
             if itmelems.tag == "title":
               title = itmelems.text
             elif itmelems.tag == "link":
               urls.append(itmelems.text)
             elif itmelems.tag == "enclosure":
               urls.append(itmelems.attrib["url"])
           
         addVideoLink(title, urls)
       
       urls = []
       title = ""
       # Check for a possible ATOM feed
       ns = {"atom":"http://www.w3.org/2005/Atom"}
       for itm in root.findall("./atom:entry",ns):
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
