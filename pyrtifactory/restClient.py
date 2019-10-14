# -*- coding: utf-8 -*-

import json
import requests
from six.moves.urllib.parse import urlencode

class artifactoryRestAPI():
    
    default_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

    response = None

    def __init__(self, url, username=None, password=None, timeout=60, api_root='api', api_version='',
                 verify_ssl=True, session=None, cookies=None):
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

    def resource_url(self, resource):
        return '/'.join([self.api_root, self.api_version, resource])

    @staticmethod
    def url_joiner(url, path, trailing=None):
        url_link = '/'.join(s.strip('/') for s in [url, path])
        if trailing:
            url_link += '/'
        return url_link

    def request(self, method='GET', path='/', data=None, flags=None, params=None, headers=None,
                files=None, trailing=None):
        """
        :param method:
        :param path:
        :param data:
        :param flags:
        :param params:
        :param headers:
        :param files:
        :param trailing: bool
        :return:
        """
        url = self.url_joiner(self.url, path, trailing)
        if params or flags:
            url += '?'
        if params:
            url += urlencode(params or {})
        if flags:
            url += ('&' if params else '') + '&'.join(flags or [])
        if files is None:
            data = json.dumps(data)

        headers = headers or self.default_headers
        response = self._session.request(
            method=method,
            url=url,
            headers=headers,
            data=data,
            timeout=self.timeout,
            verify=self.verify_ssl,
            files=files
        )
        response.encoding = 'utf-8'
        try:
            if response.text:
                response_content = response.json()
            else:
                response_content = response.content
        except ValueError:
            response_content = response.content
        return response

    def get(self, path, data=None, flags=None, params=None, headers=None, not_json_response=None, trailing=None):
        """
        Get request based on the python-requests module. You can override headers, and also, get not json response
        :param path:
        :param data:
        :param flags:
        :param params:
        :param headers:
        :param not_json_response: OPTIONAL: For get content from raw requests packet
        :param trailing: OPTIONAL: for wrap slash symbol in the end of string
        :return:
        """
        answer = self.request('GET', path=path, flags=flags, params=params, data=data, headers=headers,
                              trailing=trailing)
        if not_json_response:
            return answer.content
        else:
            if not answer.text:
                return None
            try:
                return answer.json()
            except Exception as e:
                # log.error(e)
                return answer.text
