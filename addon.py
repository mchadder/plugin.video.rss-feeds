import xbmcplugin, xbmcgui, xbmcaddon, urllib2, sys, urlparse
import xml.etree.ElementTree as etree

FEEDS = { "OWASP Uploads": { "url":"http://gdata.youtube.com/feeds/base/users/OWASPGLOBAL/uploads?alt=rss",
                             "img":"https://yt3.ggpht.com/-DYIhxCnD52Q/AAAAAAAAAAI/AAAAAAAAAAA/1oqAUTc5Jm8/s100-c-k-no/photo.jpg" },
          "OWASP AppSec Tutorials": { "url":"http://gdata.youtube.com/feeds/base/users/AppsecTutorialSeries/uploads?alt=rss",
                               "img":"https://yt3.ggpht.com/-DYIhxCnD52Q/AAAAAAAAAAI/AAAAAAAAAAA/1oqAUTc5Jm8/s100-c-k-no/photo.jpg" },
          "DEFCON Conference":{ "url":"http://gdata.youtube.com/feeds/base/users/DEFCONConference/uploads?alt=rss",
                                "img":"http://i1.ytimg.com/i/6Om9kAkl32dWlDSNlDS9Iw/mq1.jpg?v=51719028" },
          "SecurityTube": { "url":"http://gdata.youtube.com/feeds/base/users/TheSecurityTube/uploads?alt=rss",
                            "img":"https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcSHKtoYWyTShWr9a4jAvnCmgkqFRRg39BaBDQaxA1KB34rBead8" }
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

def addYoutubeLink(title, url, id):
    paramArray = url.split("?")[1].split("&")
    for param in paramArray:
        name, value = param.split("=")
        if name == "v":
            id = value;

    addLink(title, "plugin://plugin.video.youtube?path=/root/video&action=play_video&videoid=%s"%id, "http://img.youtube.com/vi/%s/hqdefault.jpg"%id)

def showLinks(feed):
   try:
       xml = urllib2.urlopen(feed).read()
       root = etree.fromstring(xml)
       for itm in root.findall("./channel/item"):
           for itmelems in itm:
               if itmelems.tag == "title":
                   title = itmelems.text
               elif itmelems.tag == "link":
                   link = itmelems.text
           addYoutubeLink(title, link, id)
   except Exception as e:
       addLink("%s"%e,"")

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
