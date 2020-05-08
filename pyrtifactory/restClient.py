# -*- coding: utf-8 -*-

import json
import logging
import requests
from six.moves.urllib.parse import urlencode


log = logging.getLogger(__name__)


class artifactoryRestAPI():
    default_headers = {'Content-Type': 'application/json'}

    response = None

    def __init__(self, url, username=None, password=None, timeout=60, api_root='api',
                 api_version='', verify_ssl=True, session=None, cookies=None):
        self.url = url
        self.username = username
        self.password = password
        self.timeout = int(timeout)
        self.verify_ssl = verify_ssl
        self.api_root = api_root
        self.api_version = api_version
        self.cookies = cookies

        if session is None:
            self._session = requests.Session()
        else:
            self._session = session

        if username and password:
            self._create_basic_session(username, password)

    def _create_basic_session(self, username, password):
        self._session.auth = (username, password)

    @staticmethod
    def url_joiner(url, path, trailing=None):
        url_link = '/'.join(s.strip('/') for s in [url, path])

        if trailing:
            url_link += '/'

        return url_link

    def request(self, method='GET', path='/', data=None, flags=None, params=None, headers=None,
                trailing=None, repo=None):
        """
        :param method:
        :param path:
        :param data:
        :param flags:
        :param params:
        :param headers:
        :param trailing: bool
        :param repo:
        :return:
        """
        url = self.url_joiner(self.url, path, trailing)

        if repo:
            url += '/' + repo

        if params or flags:
            url += '?'

        if params:
            url += urlencode(params or {})

        if flags:
            url += ('&' if params else '') + '&'.join(flags or [])

        data = None if not data else json.dumps(data)

        headers = headers or self.default_headers
        response = self._session.request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            timeout=self.timeout,
            verify=self.verify_ssl,
        )

        response.encoding = 'utf-8'

        try:
            if response.text:
                response_content = response.json()
            else:
                response_content = response.content
        except ValueError:
            response_content = response.content

        if response.status_code == 200:
            log.debug('Received: {0}\n {1}'.format(response.status_code, response_content))

        return response

    def get(self, path, data=None, flags=None, params=None, headers=None, not_json_response=None,
            trailing=None, repo=None):
        """
        Get request based on the python-requests module.
        You can override headers, and also, get not json response.
        :param path:
        :param data:
        :param flags:
        :param params:
        :param headers:
        :param not_json_response: OPTIONAL: For get content from raw requests packet
        :param trailing: OPTIONAL: for wrap slash symbol in the end of string
        :param repo:
        :return:
        """
        answer = self.request('GET', path=path, flags=flags, params=params, data=data,
                              headers=headers, trailing=trailing, repo=repo)

        if not_json_response:
            return answer.content
        else:
            if not answer.text:
                return None

            try:
                return answer.json()
            except Exception as e:
                log.error(e)
                return answer.text

    def post(self, path, data=None, headers=None, params=None, trailing=None, repo=None):
        response = self.request('POST', path=path, data=data, headers=headers, params=params,
                                trailing=trailing, repo=repo)
        try:
            return response
        except ValueError:
            log.debug('Received response with no content')
            return None

    def put(self, path, data=None, headers=None, trailing=None, params=None, repo=None,
            not_json_response=None, only_code=None):
        response = self.request('PUT', path=path, data=data, headers=headers, params=params,
                                trailing=trailing, repo=repo)

        if not_json_response:
            return response.text
        elif only_code:
            return response.status_code
        else:
            try:
                return response.json()
            except Exception as e:
                log.error(e)
                return response.text

    def delete(self, path, data=None, headers=None, params=None, trailing=None, repo=None):
        """
        Deletes resources at given paths.
        :rtype: dict
        :return: Empty dictionary to have consistent interface.
        Some of REST resources don't return any content.
        """
        response = self.request('DELETE', path=path, data=data, headers=headers, params=params,
                                trailing=trailing, repo=repo)
        # if self.advanced_mode:
        #     return response
        try:
            return response.text
        except ValueError:
            log.debug('Received response with no content')
            return None
