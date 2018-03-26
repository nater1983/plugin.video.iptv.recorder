import xbmcaddon
import xbmc, xbmcgui, xbmcvfs
import requests
import base64
import time, datetime

servicing = False
#xbmc.log("SERVER")

def Service():
    global servicing
    if servicing:
        return
    servicing = True
    #xbmc.log("SERVICE",xbmc.LOGERROR)
    xbmc.executebuiltin('XBMC.RunPlugin(plugin://plugin.video.iptv.recorder/full_service)')
    time.sleep(2)
    servicing = False

if __name__ == '__main__':
    #TODO enable Web Server, startServer does not enable it
    ADDON = xbmcaddon.Addon('plugin.video.iptv.recorder')
    try:
        if ADDON.getSetting('service') == 'true':
            monitor = xbmc.Monitor()
            xbmc.log("[plugin.video.iptv.recorder] service started...", xbmc.LOGERROR)
            if ADDON.getSetting('service.startup') == 'true':
                time.sleep(int(ADDON.getSetting('service.delay')))
                Service()
                ADDON.setSetting('last.update', str(time.time()))
            while not monitor.abortRequested():
                if ADDON.getSetting('service.type') == '1':
                    interval = int(ADDON.getSetting('service.interval'))
                    waitTime = 3600 * interval
                    ts = ADDON.getSetting('last.update') or "0.0"
                    lastTime = datetime.datetime.fromtimestamp(float(ts))
                    now = datetime.datetime.now()
                    nextTime = lastTime + datetime.timedelta(seconds=waitTime)
                    td = nextTime - now
                    timeLeft = td.seconds + (td.days * 24 * 3600)
                    xbmc.log("[plugin.video.iptv.recorder] Service waiting for interval %s" % waitTime, xbmc.LOGERROR)
                elif ADDON.getSetting('service.type') == '2':
                    next_time = ADDON.getSetting('service.time')
                    if next_time:
                        hour,minute = next_time.split(':')
                        now = datetime.datetime.now()
                        next_time = now.replace(hour=int(hour),minute=int(minute),second=0,microsecond=0)
                        if next_time < now:
                            next_time = next_time + datetime.timedelta(hours=24)
                        td = next_time - now
                        timeLeft = td.seconds + (td.days * 24 * 3600)
                if timeLeft <= 0:
                    timeLeft = 1
                xbmc.log("[plugin.video.iptv.recorder] Service waiting for %d seconds" % timeLeft, xbmc.LOGERROR)
                if timeLeft and monitor.waitForAbort(timeLeft):
                    break
                xbmc.log("[plugin.video.iptv.recorder] Service now triggered...", xbmc.LOGERROR)
                Service()
                now = time.time()
                ADDON.setSetting('last.update', str(now))

    except:
        pass

