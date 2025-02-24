import sys
import json
import requests
from requests.models import PreparedRequest, Response
import click
from .constants import constants
from .config import get


class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self._setup_interceptors()

    def _setup_interceptors(self):
        """Setup request and response interceptors"""
        old_send = self.session.send

        def new_send(prep: PreparedRequest, **kwargs) -> Response:
            # Request interceptor
            try:
                prep = self._request_interceptor(prep)
            except Exception as e:
                return self._handle_error(e)

            # Make the request
            try:
                response = old_send(prep, **kwargs)
                # Response interceptor
                return self._response_interceptor(response)
            except Exception as e:
                return self._handle_error(e)

        self.session.send = new_send

    def _request_interceptor(self, request: PreparedRequest) -> PreparedRequest:
        """Handle request interception"""
        # Get token synchronously (we're in a sync context)
        token = get("token")

        # Check if login is required
        if request.url and request.url.endswith("login") and not token:
            click.echo(click.style("You don't have credentials. Run login first", fg='yellow'))
            sys.exit(1)

        # Add authorization header
        if token:
            request.headers["Authorization"] = f"Bearer {token}"

        # Debug logging
        if request.body:
            click.echo(click.style("request: " + json.dumps(request.body), fg='green'), err=True)

        return request

    def _response_interceptor(self, response: Response) -> Response:
        """Handle response interception"""
        return response

    def _handle_error(self, error: Exception) -> Response:
        """Handle request/response errors"""
        click.echo(click.style("Error occurred: ", fg='red')
                   + click.style(str(error), fg='white'), err=True)
        raise error

    def _prepare_request(self, method: str, path: str, **kwargs) -> PreparedRequest:
        """Prepare request with base URL"""
        url = f"{self.base_url}{path}"
        request = requests.Request(method, url, **kwargs)
        return self.session.prepare_request(request)

    def get(self, path: str, **kwargs) -> Response:
        """Make GET request"""
        prep = self._prepare_request("GET", path, **kwargs)
        return self.session.send(prep)

    def post(self, path: str, **kwargs) -> Response:
        """Make POST request"""
        prep = self._prepare_request("POST", path, **kwargs)
        return self.session.send(prep)


# Create client instance
client = Client(constants.API_URL)
