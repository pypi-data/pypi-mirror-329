import click
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import threading
import json
import secrets
from typing import Optional
import os
import stat
from datetime import datetime, timedelta
import ssl
from pathlib import Path
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# Store the authentication token
auth_token: Optional[str] = None

class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle the callback from the authentication page"""
        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        """Handle the POST callback from Auth0"""
        if self.path.startswith('/callback'):
            # Get the length of the POST data
            content_length = int(self.headers['Content-Length'])
            # Read the POST data
            post_data = self.rfile.read(content_length).decode('utf-8')
            # Parse the form data
            form_data = urllib.parse.parse_qs(post_data)
            
            # Get the token from the form data
            global auth_token
            auth_token = form_data.get('access_token', [None])[0]
            
            # Send response to browser
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            response_content = """
            <html>
                <body>
                    <script>
                        window.close();
                        document.body.innerHTML = '<p>Authentication complete. You can close this window.</p>';
                    </script>
                </body>
            </html>
            """
            self.wfile.write(response_content.encode())
        else:
            self.send_response(404)
            self.end_headers()

def create_self_signed_cert(config_dir: Path) -> tuple[str, str]:
    """Create a self-signed certificate for local HTTPS"""
    cert_path = config_dir / "cert.pem"
    key_path = config_dir / "key.pem"
    
    if not cert_path.exists() or not key_path.exists():
        # Generate key and self-signed certificate
        # Generate private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )

        # Generate certificate
        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, 'localhost')
        ])

        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([x509.DNSName('localhost')]),
            critical=False,
        ).sign(private_key, hashes.SHA256())

        # Write private key
        with open(key_path, 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        # Write certificate
        with open(cert_path, 'wb') as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))

        # Set file permissions
        key_path.chmod(0o600)
        cert_path.chmod(0o600)

    return str(cert_path), str(key_path)

def start_auth_server(port: int = 8081) -> HTTPServer:
    """Start the local authentication server with HTTPS"""
    config_dir = Path(os.path.expanduser("~/.config/amds"))
    config_dir.mkdir(parents=True, exist_ok=True)
    cert_path, key_path = create_self_signed_cert(config_dir)
    
    server = HTTPServer(('localhost', port), AuthHandler)
    
    # Configure SSL
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_cert_chain(cert_path, key_path)
    server.socket = ssl_context.wrap_socket(server.socket, server_side=True)
    
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    return server

def get_config_path() -> str:
    """Get the path to the config directory and create it if it doesn't exist"""
    config_dir = os.path.expanduser("~/.config/amds")
    os.makedirs(config_dir, exist_ok=True)
    return os.path.join(config_dir, "config.json")

def is_token_valid(config: dict) -> bool:
    """Check if the stored token is still valid"""
    if 'expiration_time' not in config:
        return False
    
    try:
        expiration_time = datetime.fromisoformat(config['expiration_time'])
        return datetime.utcnow() < expiration_time
    except (ValueError, TypeError):
        return False

@click.command()
@click.option('--port', default=8081, help='Port for the authentication server')
def login(port: int):
    """CLI command to initiate the login process"""
    # Generate a state parameter for security
    state = secrets.token_urlsafe(16)
    
    # Auth0 configuration
    AUTH0_DOMAIN = "auth.amdatascience.com"
    AUTH0_CLIENT_ID = "FNaQyrcrgtlYSmBnASDKwMGHtezACTuC"
    # Ensure the redirect URI is properly formatted without any special characters
    REDIRECT_URI = f"https://localhost:{port}/callback".strip()
    
    # Construct the authentication URL for Auth0
    auth_url = (
        f"https://{AUTH0_DOMAIN}/authorize"
        f"?response_type=token"
        f"&response_mode=form_post"
        f"&client_id={AUTH0_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"  # Remove urllib.parse.quote since Auth0 will handle the encoding
        f"&scope=openid profile email"
        f"&state={state}"
    )
    
    # Start the local server
    server = start_auth_server(port)
    
    # Open the browser
    click.echo("Opening browser for authentication...")
    webbrowser.open(auth_url)
    
    # Wait for authentication to complete
    while auth_token is None:
        click.echo("Waiting for authentication...", nl=False)
        click.echo("\r", nl=False)
    
    # Shutdown the server
    server.shutdown()
    server.server_close()
    
    # Store the token securely
    if auth_token:
        click.echo("Authentication successful!")
        config_path = get_config_path()
        
        # Set expiration time to 12 hours from now
        expiration_time = datetime.utcnow() + timedelta(hours=12)
        
        config = {
            'auth_token': auth_token,
            'expiration_time': expiration_time.isoformat()
        }
        
        # Write config with restricted permissions (600)
        with open(config_path, 'w') as f:
            json.dump(config, f)
        
        # Set file permissions to user read/write only
        os.chmod(config_path, stat.S_IRUSR | stat.S_IWUSR)
        
        click.echo(f"Token stored in {config_path}")
    else:
        click.echo("Authentication failed!")
