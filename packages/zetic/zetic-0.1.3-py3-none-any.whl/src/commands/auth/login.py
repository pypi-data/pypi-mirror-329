import click
import http.server
import webbrowser
import urllib.parse
from urllib.parse import urlparse, parse_qs
import socketserver
from ...constants import constants
from ...client import client
from ...config import set
from termcolor import colored
import time
import threading
import sys
import socket
import atexit


def save_login_file(token: str) -> None:
    """Save token to config file"""
    set("token", token)


class TCPServerReuse(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        # Set socket options to allow reuse of the address
        self.allow_reuse_address = True
        super().__init__(server_address, RequestHandlerClass, bind_and_activate)

    def server_close(self):
        # Ensure the socket is properly closed
        super().server_close()
        self.socket.close()


class LoginHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.local_url = kwargs.pop('local_url')
        self.save_login_file = kwargs.pop('save_login_file')
        super().__init__(*args, **kwargs)

    def close_server(self):
        def shutdown():
            time.sleep(1)
            # Properly shutdown and close the server
            self.server.shutdown()
            self.server.server_close()
            sys.exit(0)

        threading.Thread(target=shutdown).start()

    def do_GET(self):
        if self.path == "/":
            # Handle root path
            callback = f"{self.local_url}/callback"
            encoded_cb = urllib.parse.quote(callback)
            self.send_response(302)
            self.send_header('Location', f"{constants.WEB_URL}/auth/cli?cb={encoded_cb}")
            self.end_headers()

        elif self.path.startswith('/callback'):
            # Handle callback
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            token = query_params.get('token', [None])[0]

            if not token:
                self.send_response(302)
                self.send_header('Location', '/fail')
                self.end_headers()
            else:
                self.save_login_file(token)
                self.send_response(302)
                self.send_header('Location', '/success')
                self.end_headers()

        elif self.path == "/success":
            # Handle success
            print(colored("Successfully logged in (1hour)", "green"))
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Successfully login(1 hour)")
            self.close_server()

        elif self.path == "/fail":
            # Handle failure
            print(colored("Login failed", "red"))
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Login failed")
            self.close_server()

        else:
            # Handle unknown paths
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Something is wrong!")
            self.close_server()

    def log_message(*args):
        pass


def find_free_port():
    """Find an available port by creating a temporary socket."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


def cleanup_server(server):
    """Cleanup function to ensure server is properly closed"""
    try:
        server.shutdown()
        server.server_close()
        print("Server cleaned up successfully")
    except Exception:
        pass


def login_with_browser():
    """Handle browser-based login flow"""
    server = None
    try:
        port = find_free_port()
        local_url = f"http://localhost:{port}"

        def handler(*args):
            return LoginHandler(
                *args,
                local_url=local_url,
                save_login_file=save_login_file,
            )

        # Use our custom TCPServer with address reuse
        server = TCPServerReuse(("localhost", port), handler)

        # Register cleanup function
        atexit.register(lambda: cleanup_server(server))

        # callback = f"{local_url}/callback"
        # encoded_cb = urllib.parse.quote(callback)
        # target_url = f"{constants.WEB_URL}/auth/cli?cb={encoded_cb}"
        # Open browser and start server
        webbrowser.open(local_url)
        server.serve_forever()

    except Exception as e:
        print(f"Error: {e}")
        if server:
            cleanup_server(server)


def login_without_browser():
    """Handle non-browser login flow"""
    click.echo(click.style("Copy below URL to login", fg='green'))
    click.echo("")
    click.echo(click.style(f"{constants.WEB_URL}/auth/cli?noBrowser=true", fg='green'))
    click.echo("")

    code = click.prompt("Verification code", type=str)

    try:
        response = client.get("/auth/me", headers={"Authorization": f"Bearer {code}"})
        if response.status_code == 200:
            click.echo(click.style("Successfully logged in (1hour)", fg='green'))
        else:
            click.echo(click.style("Login failed", fg='red'))
    except Exception as e:
        click.echo(click.style(f"Login failed: {str(e)}", fg='red'))


@click.command()
@click.option('--no-browser', is_flag=True, help='Login without browser')
@click.option('--debug', '-d', is_flag=True, help='Output extra debugging')
def login(no_browser, debug):
    """Login to the service"""
    try:
        if not no_browser:
            login_with_browser()
        else:
            login_without_browser()
    except Exception as e:
        if debug:
            click.echo(click.style(f"Debug error: {str(e)}", fg='red'))
        else:
            click.echo(click.style("Login failed", fg='red'))
