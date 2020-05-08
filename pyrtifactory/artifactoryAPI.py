# -*- coding: utf-8 -*-

import json

from .restClient import artifactoryRestAPI


class artifactoryAPI(artifactoryRestAPI):
    def getTasks(self):
        """
        Description: Get Background Tasks.
        Retrieves list of background tasks currently scheduled or running in Artifactory.
        Task can be in one of few states: scheduled, running, stopped, cancelled. Running task also shows the task start time.
        """
        return(self.get('api/tasks'))

    def createRepository(self, repo, data):
        """
        Description: Creates a new repository in Artifactory with the provided configuration. Supported by local, remote and virtual repositories.
        Usage: PUT /api/repositories/{repoKey}
        repo = repoKey

        If a repository with the specified repoKey already exists, the call fails with a 400 response.
        Missing values are set to the default values as defined by the consumed type spec.
        For a repository to be identified as Smart Remote Repository, you need to set the “enabled” flag to true under “contentSynchronisation” (under Repository Configuration JSON).
        Repository Configuration JSON: https://www.jfrog.com/confluence/display/JFROG/Repository+Configuration+JSON
        """
        return(self.put('api/repositories', repo=repo, data=data, not_json_response=True))

    def deleteRepository(self, repo):
        """
        Description: Removes a repository configuration together with the whole repository content. Supported by local, remote and virtual repositories.
        Usage: DELETE /api/repositories/{repoKey}
        repo = repoKey
        """
        return(self.delete('api/repositories', repo=repo))

    def getRepositories(self, params=None):
        """
        Description: Get Repositories.
        Returns a list of minimal repository details for all repositories of the specified type.
        Usage: GET /api/repositories[?type=repositoryType (local|remote|virtual|distribution)][&packageType=maven|gradle|ivy|sbt|helm|cocoapods|opkg|rpm|nuget|cran|gems|npm|bower|debian|composer|pypi|docker|vagrant|gitlfs|go|yum|conan|chef|puppet|generic]
        params = {'type': 'local', 'packageType': 'docker'}
        """
        return(json.dumps(self.get('api/repositories', params=params)))

    def getReplication(self, repo=None):
        """
        Description: Returns the replication configuration for the given repository key, if found. If repoKey not provided will return all replications.
        Usage: GET /api/replications/{repoKey}
        repo = repoKey
        """
        return(json.dumps(self.get('api/replications', repo=repo)))

    def updateReplication(self, repo, data):
        """
        Description: Update existing replication configuration for given repository key, if found.
        Usage: POST /api/replications/{repoKey}
        repo = repoKey
        """
        return(self.post('api/replications', repo=repo, data=data))

    def setReplication(self, repo, data):
        """
        Description: Add or replace replication configuration for given repository key.
        Usage: PUT /api/replications/{repoKey}
        repo = repoKey
        """
        return(self.put('api/replications', repo=repo, data=data, only_code=True))

    def getStatus(self):
        """
        Description: Get a simple status response about the state of Artifactory
        Returns 200 code with an 'OK' text if Artifactory is working properly, if not will return an HTTP error code with a reason.
        """
        return(self.get('api/system/ping', not_json_response=True))
