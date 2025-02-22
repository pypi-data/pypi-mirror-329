"""Connection session management"""
# pylint: disable=arguments-differ

from urllib3.util import Retry
import requests
from requests.adapters import HTTPAdapter


class SessionConnect(requests.Session):
    """Session connection handling"""
    def __init__(self,
                 url='api.seeqc.cloud',
                 default_timeout=(5, 30)):
        super().__init__()
        self.default_timeout = default_timeout
        self.url = url
        retries = Retry(total=3, backoff_factor=.2, status_forcelist=[502, 503, 504])
        self.mount('https://', HTTPAdapter(max_retries=retries))

    def request(self, method, url, **kwargs):
        """Overload the session request"""
        if "timeout" not in kwargs:
            kwargs["timeout"] = self.default_timeout
        return super().request(method, self.url + url, **kwargs)

    def update_urls(self, url):
        """Update the base url"""
        self.url = url
