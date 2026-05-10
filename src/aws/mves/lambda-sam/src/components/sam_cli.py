import os
import subprocess
import time
from typing import Literal
import requests

class SamCli:
    _command: Literal["api", "lambda"] = None
    _lambda_endpoint: str = None
    _process: subprocess.Popen = None

    def __init__(self, command: Literal["api", "lambda"]):
        self._command = command
        if command == "api":
            self._lambda_endpoint = os.getenv("SAM_API_URL")
        elif command == "lambda":
            self._lambda_endpoint = os.getenv("SAM_LAMBDA_URL")

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def start(self):
        """
        Starts the SAM local API or Lambda in the background.
        """
        self._process = subprocess.Popen(
            ["sam", "local", f"start-{self._command}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        self._wait_api()

    def close(self):
        """
        Stops the SAM local process.
        """
        if self._process:
            self._process.terminate()
            self._process.wait()

    def _wait_api(self):
        """
        Wait for the SAM local process to be ready.
        """
        max_retries = 30
        for retry in range(max_retries):
            try:
                requests.get(self._lambda_endpoint)
                break
            except requests.exceptions.ConnectionError:
                time.sleep(1)
                if retry == max_retries - 1:
                    self.close()
                    raise RuntimeError(f"SAM local {self._command} failed to start")
