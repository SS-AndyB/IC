#!/usr/bin/env python3

import time
import vstsbuildstatusmonitor
import displayotron
import trafficlights

"""
# EmvsCorePlatform_Master_CI 39
# EmvsEuropeanHub_Master_CI 42
# GenericCorePlatform_Master_CI 25
# EmvsAdminProxy_Master_CI 49
"""

APIACCESSKEY = ''
TEAMSERVICESACCOUNT = 'solidsoftreply-emvs'
TEAMPROJECT = 'Hub'
BUILDS_TO_WATCH = [25, 39, 42, 49]
REFRESH_INTERVAL_SECONDS = 30


def main():
    colourvalues = trafficlights.Colours()

    ALL_USED_COLOURS = (colourvalues.RED(),
                        colourvalues.AMBER(),
                        colourvalues.GREEN())

    display = displayotron.Display(colourvalues)

    # quick test on start to check that all LEDs are working
    for colour in ALL_USED_COLOURS:
        display.setcolour(colour)
        time.sleep(1)

    monitors = []
    for buildid in BUILDS_TO_WATCH:
        monitor = vstsbuildstatusmonitor.VstsBuildStatusMonitor(
            buildid=buildid,
            colours=colourvalues,
            teamaccount=TEAMSERVICESACCOUNT,
            teamproject=TEAMPROJECT,
            key=APIACCESSKEY)

        monitors.append(monitor)

    print("monitors : " + str(len(monitors)))

    # try / except allows us to loop forever until ^C is pressed
    try:
        while (True):
            summarystatus = colourvalues.GREEN()
            failingbuilds = ""
            failingcount = 0
            for monitor in monitors:
                status = monitor.getstatus()
                #print(monitor.getlastrequesturi())
                if (status == colourvalues.RED()):
                    summarystatus = colourvalues.RED()
                    failingbuilds += monitor.getbuildname() + ":" + monitor.getbreaker() + " "
                    failingcount += 1
                elif (status == colourvalues.GREEN() and summarystatus == colourvalues.GREEN()):
                    summarystatus = colourvalues.GREEN
                elif (status == colourvalues.AMBER() and summarystatus == colourvalues.GREEN()):
                    summarystatus = colourvalues.AMBER()

            message = ""
            if (len(failingbuilds) > 0):
                message = failingbuilds
            elif (summarystatus == colourvalues.AMBER()):
                message = "                " + " Network Error"
            else:
                message = "                " + " ALL BUILDS OK"
            display.setbarlevel(failingcount / len(BUILDS_TO_WATCH))
            display.setcolour(summarystatus)
            display.settext(message)
            time.sleep(REFRESH_INTERVAL_SECONDS)

    #except Exception as e:
        print(e)
        pass

    finally:
        display.clear()


if (__name__ == "__main__"):
    main()
