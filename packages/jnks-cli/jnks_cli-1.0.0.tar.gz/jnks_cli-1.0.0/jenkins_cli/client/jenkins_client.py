"""Jenkins client implementation"""
import jenkins
import logging
import json
import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from requests.exceptions import ConnectionError, SSLError, Timeout

class JenkinsClient:
    def __init__(self, host, username, token):
        self.host = host
        self.username = username
        self.token = token
        self._client = None

    @property
    def client(self):
        if not self._client:
            if self.host.startswith('https://'):
                urllib3.disable_warnings(InsecureRequestWarning)
                logging.debug("SSL verification warnings disabled for HTTPS connection")
                
                # Monkey patch the requests verify parameter
                old_request = requests.Session.request
                def new_request(self, method, url, **kwargs):
                    kwargs['verify'] = False
                    return old_request(self, method, url, **kwargs)
                requests.Session.request = new_request
            
            try:
                self._client = jenkins.Jenkins(
                    self.host,
                    username=self.username,
                    password=self.token,
                    timeout=30
                )
            except Exception as e:
                logging.debug(f"Error initializing Jenkins client: {str(e)}")
                raise

        return self._client

    def test_connection(self):
        """Test connection to Jenkins server"""
        try:
            user = self.client.get_whoami()
            logging.debug(f"Successfully connected as user: {user['fullName']}")
            return True
        except jenkins.JenkinsException as e:
            logging.debug(f"Jenkins error: {str(e)}")
            return False
        except (ConnectionError, SSLError) as e:
            logging.debug(f"Connection error: {str(e)}")
            return False
        except Timeout:
            logging.debug("Connection timed out")
            return False
        except Exception as e:
            logging.debug(f"Unexpected error: {str(e)}")
            return False