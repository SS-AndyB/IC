#!/usr/bin/env python3

class Hub2ProjectDetails(object):
    """docstring for Project"""

    def __init__(self):
        """
        # EmvsCorePlatform_Master_CI 39
        # EmvsEuropeanHub_Master_CI 42
        # EmvsHubCommon_Master_CI   79
        # GenericCorePlatform_Master_CI 25
        # EmvsAdminProxy_Master_CI 49
        """
        self.APIACCESSKEY = ''
        self.TEAMSERVICESACCOUNT = 'solidsoftreply-emvs'
        self.TEAMPROJECT = 'Hub'
        self.BUILDS_TO_WATCH = [25, 39, 79, 42, 49]
        self.REPOS_TO_WATCH = [ 'Generic%20Core%20Platform',
                                'Emvs%20Core%20Platform',
                                "EMVS%20Hub%20Common",
                                'Emvs%20European%20Hub',
                                'EMVS%20Administration%20Proxy']
        
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


    def getgitrepostowatch(self):
        return self.REPOS_TO_WATCH

