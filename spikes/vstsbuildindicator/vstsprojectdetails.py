#!/usr/bin/env python3

class Hub2ProjectDetails(object):
    """docstring for Project"""

    def __init__(self):
        """
        # EmvsCorePlatform_Master_CI 39
        # EmvsEuropeanHub_Master_CI 42
        # GenericCorePlatform_Master_CI 25
        # EmvsAdminProxy_Master_CI 49
        """
        self.APIACCESSKEY = ''
        self.TEAMSERVICESACCOUNT = 'solidsoftreply-emvs'
        self.TEAMPROJECT = 'Hub'
        self.BUILDS_TO_WATCH = [25, 39, 42, 49]
        self.REFRESH_INTERVAL_SECONDS = 10


    def getapikey(self):
        return self.APIACCESSKEY


    def getvstsaccount(self):
        return self.TEAMSERVICESACCOUNT


    def getteamprojectname(self):
        return self.TEAMPROJECT


    def getbuildstowatch(self):
        return self.BUILDS_TO_WATCH


    def getrefreshintervalseconds(self):
        return self.REFRESH_INTERVAL_SECONDS

