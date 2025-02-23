import requests
from json import JSONDecodeError
from ownerrez_wrapper.model import Result
import base64
from typing import List, Dict
import logging
import datetime
from ownerrez_wrapper.constants import BASEURL as hosturl
from ownerrez_wrapper.exceptions import OwnerrezApiException

class RestAdapter(object):
    def __init__(self,username, token):
        """
        Initialize the RestAdapter object with the OwnerRez username and token
        :param username: OwnerRez username
        :param token: OwnerRez token
        """
        auth_string = f"{username}:{token}"
        auth_bytes = auth_string.encode('ascii')
        auth_b64 = base64.b64encode(auth_bytes).decode('ascii')
        self.headers = {
            'User-Agent': 'OwnerRezAPI',
            'Content-Type': 'application/json',
            'Authorization': f'Basic {auth_b64}'
        }
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)

    def _do_request(self, http_method, endpoint, ep_params, data: Dict = None):
        """
        Make a request to the OwnerRez API
        :param http_method: HTTP method to use
        :param endpoint: API endpoint to call
        :param ep_params: Dictionary of parameters to pass to the endpoint
        :param data: Dictionary of data to pass in the request body
        :return: Result object
        """
        
        full_url = f"{hosturl}/{endpoint.lstrip('/')}"
        log_line_pre = f"method={http_method}, url={full_url}, params={ep_params}"
        log_line_post = ', '.join((log_line_pre, "success={}, status_code={}, message={}"))
        
        # Make the request
        try:
            self._logger.debug(msg = log_line_pre)
            response = requests.request(method=http_method, url=full_url, headers=self.headers, params=ep_params, json=data)
        
        # If the request fails, log the error and raise an exception
        except requests.exceptions.RequestException as e:
            self._logger.error(msg=(str(e)))
            raise OwnerrezApiException("Request failed") from e
        
        # Check status code first
        is_success = 299 >= response.status_code >= 200     # 200 to 299 is OK
        if not is_success:
            self._logger.error(msg=log_line_post.format(False, response.status_code, response.reason))
            raise OwnerrezApiException(f"{response.status_code}: {response.reason}")

        # Try to parse the response as JSON only for successful responses
        try:
            data_out = response.json()
        except (ValueError, TypeError, JSONDecodeError) as e:
            self._logger.error(msg=log_line_post.format(False, response.status_code, e))
            raise OwnerrezApiException("Bad JSON in response") from e

        
        return Result(status=response.status_code, message=response.reason, data=data_out)

    def get(self, endpoint: str, ep_params: Dict = None) -> Result:
        """
        Make a GET request to the OwnerRez API
        :param endpoint: API endpoint to call
        :param ep_params: Dictionary of parameters to pass to the endpoint
        :return: Result object
        """
        return self._do_request(http_method='GET', endpoint=endpoint, ep_params=ep_params)