#!/usr/bin/env python3

import time
import vstsprojectdetails
import vstsbuildstatusmonitor
import vstsbuildqueuemonitor
import displayotron
import trafficlights



def main():
    h2 = vstsprojectdetails.Hub2ProjectDetails()

    colourvalues = trafficlights.Colours()

    ALL_USED_COLOURS = (colourvalues.RED(),
                        colourvalues.AMBER(),
                        colourvalues.GREEN())

    display = displayotron.Display(colourvalues)

    # quick test on start to check that all LEDs are working
    for colour in ALL_USED_COLOURS:
        display.setcolour(colour)
        time.sleep(1)

    queuemonitor = vstsbuildqueuemonitor.QueueStatusMonitor(
                                teamaccount=h2.getvstsaccount(), 
                                key=h2.getapikey())

    buildmonitors = []
    
    for buildid in h2.getbuildstowatch():
        monitor = vstsbuildstatusmonitor.VstsBuildStatusMonitor(
            buildid=buildid,
            colours=colourvalues,
            teamaccount=h2.getvstsaccount(),
            teamproject=h2.getteamprojectname(),
            key=h2.getapikey())

        buildmonitors.append(monitor)

    print("buildmonitors created : " + str(len(buildmonitors)))

    # try / except allows us to loop forever until ^C is pressed
    try:
        while (True):
            summarystatus = colourvalues.GREEN()
            failingbuilds = ""
            failingcount = 0
            for monitor in buildmonitors:
                status = monitor.getstatus()
                #print(monitor.getlastrequesturi())
                if (status == colourvalues.RED()):
                    summarystatus = colourvalues.RED()
                    failingbuilds += monitor.getbuildname() + ":"
                    failingbuilds += monitor.getbreaker() + " "
                    failingcount += 1
                elif (status == colourvalues.GREEN() and \
                      summarystatus == colourvalues.GREEN()):
                    summarystatus = colourvalues.GREEN
                elif (status == colourvalues.AMBER() and \
                      summarystatus == colourvalues.GREEN()):
                    summarystatus = colourvalues.AMBER()
            queuelength = queuemonitor.getqueuelength()

            if(queuelength >= 0):
                message = "Build queue: $  ".replace('$',str(queuelength))
            else:
                message = "Build queue: n/a"

            if (len(failingbuilds) > 0):
                message += failingbuilds
            elif (summarystatus == colourvalues.AMBER()):
                message += "                " + " Network Error"
            else:
                message += "                " + " ALL BUILDS OK"
            display.setbarlevel(failingcount / len(h2.getbuildstowatch()))
            display.setcolour(summarystatus)
            display.settext(message)
            time.sleep(h2.getrefreshintervalseconds())

    #except Exception as e:
        print(e)
        pass

    finally:
        display.clear()


if (__name__ == "__main__"):
    main()
