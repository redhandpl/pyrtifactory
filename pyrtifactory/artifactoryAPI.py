# -*- coding: utf-8 -*-

import json

from .restClient import artifactoryRestAPI

class artifactoryAPI(artifactoryRestAPI):
    def getTasks(self):
        """
        Get Background Tasks.
        Retrieves list of background tasks currently scheduled or running in Artifactory.
        Task can be in one of few states: scheduled, running, stopped, cancelled. Running task also shows the task start time.
        """
        return(self.get('api/tasks'))
        
    def getRepositories(self, params=None):
        """
        Get Repositories.
        Returns a list of minimal repository details for all repositories of the specified type.
        Usage: GET /api/repositories[?type=repositoryType (local|remote|virtual|distribution)][&packageType=maven|gradle|ivy|sbt|helm|cocoapods|opkg|rpm|nuget|cran|gems|npm|bower|debian|composer|pypi|docker|vagrant|gitlfs|go|yum|conan|chef|puppet|generic]
        params = {'type': 'local', 'packageType': 'docker'}
        """
        return(json.dumps(self.get('api/repositories', params=params)))
