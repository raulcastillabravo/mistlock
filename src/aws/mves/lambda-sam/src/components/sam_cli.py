import os
import subprocess
import time
import requests

class SamCli:
    _api_url: str = None
    _process: subprocess.Popen = None

    def __init__(self):
        self._api_url = os.getenv("SAM_API_URL")

    def start_api(self):
        """
        Starts the SAM local API in the background.
        """
        self._process = subprocess.Popen(
            ["sam", "local", "start-api"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        self._wait_api()

    def stop_api(self):
        """
        Stops the SAM local API.
        """
        if self._process:
            self._process.terminate()
            self._process.wait()

    def _wait_api(self):
        """
        Wait for the SAM local API to be ready.
        """
        max_retries = 30
        for retry in range(max_retries):
            try:
                requests.get(self._api_url)
                break
            except requests.exceptions.ConnectionError:
                time.sleep(1)
                if retry == max_retries - 1:
                    self.stop_api()
                    raise RuntimeError("SAM local API failed to start")
