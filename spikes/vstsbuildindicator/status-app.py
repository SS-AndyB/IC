#!/usr/bin/env python3

import time
import vstsprojectdetails
import vstsbuildstatusmonitor
import vstsbuildqueuemonitor
import vstspullrequestmonitor
import displayotron
import trafficlights


class StatusApp:
    def __init__(self):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print (timestamp + " - starting monitoring")
        self.colourvalues = trafficlights.Colours()

        self.ALL_USED_COLOURS = (self.colourvalues.RED(),
                                 self.colourvalues.AMBER(),
                                 self.colourvalues.GREEN())

        self.display = displayotron.Display(self.colourvalues)

        # quick test on start to check that all LEDs are working
        for colour in self.ALL_USED_COLOURS:
            self.display.setcolour(colour)
            time.sleep(1)

        h2 = vstsprojectdetails.Hub2ProjectDetails()

        self.pullrequestmonitors = []

        for repo in h2.getgitrepostowatch():
            prmonitor = vstspullrequestmonitor.PullRequestMonitor(
                                    teamaccount=h2.getvstsaccount(),
                                    teamproject=h2.getteamprojectname(),
                                    repo=repo,
                                    key=h2.getapikey())

            self.pullrequestmonitors.append(prmonitor)

        self.buildmonitors = []
        
        for buildid in h2.getbuildstowatch():
            monitor = vstsbuildstatusmonitor.VstsBuildStatusMonitor(
                buildid=buildid,
                colours=self.colourvalues,
                teamaccount=h2.getvstsaccount(),
                teamproject=h2.getteamprojectname(),
                key=h2.getapikey())

            self.buildmonitors.append(monitor)

        self.monitorinterval = h2.getrefreshintervalseconds()
        #print("buildmonitors created : " + str(len(buildmonitors)))
        #print("pr monitors created : " + str(len(pullrequestmonitors)))


    def processpullrequests(self):
        # first get pull request count
        pullrequestsopen = 0
        
        for prqmonitor in self.pullrequestmonitors:
            prcount = prqmonitor.getpullrequestcount()
            # -1 denotes a problem getting the data for this repo
            if(prcount >= 0):
                pullrequestsopen += prcount
            else:
                pullrequestsopen = -1
                break

        if (pullrequestsopen >= 0):
            paddedvalue = str(pullrequestsopen) + \
                            (' ' * (6 - len(str(pullrequestsopen))))
            message = "Open PRs: " + paddedvalue
        else:
            message = "Open PRs: n/a   "

        return message


    def processbuilds(self):
        colours = self.colourvalues
        summarystatus = colours.GREEN()
        failingbuilds = ""
        failingcount = 0

        for monitor in self.buildmonitors:
            status = monitor.getstatus()

            if (status == colours.RED()):
                summarystatus = colours.RED()
                failingbuilds += monitor.getbuildname() + ":"
                failingbuilds += monitor.getbreaker() + " "
                failingcount += 1

            elif (status == colours.GREEN() and \
                    summarystatus == colours.GREEN()):
                summarystatus = colours.GREEN()

            elif (status == colours.AMBER() and \
                    summarystatus == colours.GREEN()):
                summarystatus = colours.AMBER()
        
        if (len(failingbuilds) > 0):
            message = failingbuilds
        elif (summarystatus == colours.AMBER()):
            message = ' ' * 16 + " Network Error"
        else:
            message = ' ' * 16 + " ALL BUILDS OK"

        return summarystatus, message


    def run(self):
        colours = self.colourvalues
        # try / except allows us to loop forever until ^C is pressed
        try:
            while (True):
                message = self.processpullrequests()
                
                summarystatus, buildmessage = self.processbuilds()

                displaymessage = message + buildmessage

                #self.display.setbarlevel(failingcount / len(h2.getbuildstowatch()))
                self.display.setcolour(summarystatus)
                self.display.settext(displaymessage)
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                print (timestamp + " - " +
                    "message: #" + displaymessage + "# " + summarystatus)
                print (timestamp + ' - ' + 
                       "message: #" +
                       '1' * 16 + '2' * 16 + '3' * 16)
                
                time.sleep(self.monitorinterval)

        #except Exception as e:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            print (timestamp + " - " + e)
            pass

        finally:
            self.display.clear()


def main():
    app = StatusApp()
    app.run()


if (__name__ == "__main__"):
    main()
