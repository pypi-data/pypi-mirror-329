import http.server
import ssl
import argparse
import sys
import os

VERSION = "1.0.1"

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()


def main():
    parser = argparse.ArgumentParser(
        description="Simple HTTPS server with CORS support.",
        epilog="Usage example: httpds-python <port> --hostname <hostname> --key /path/to/key.pem --cert /path/to/cert.pem --path /path/to/files"
    )
    parser.add_argument('port', type=int, help="Port number to run the server on.")
    parser.add_argument('--hostname', '-H', default='0.0.0.0', help="Hostname or IP address to bind to (default: 0.0.0.0).")
    parser.add_argument('--key', '-k', required=True, help="Path to the SSL key file.")
    parser.add_argument('--cert', '-c', required=True, help="Path to the SSL certificate file.")
    parser.add_argument('--path', '-p', default=os.getcwd(), help="Path to the directory to serve (default: current directory).")
    parser.add_argument('--version', '-v', action='version', version=f'%(prog)s {VERSION}', help="Show version")

    args = parser.parse_args()

    port = args.port
    hostname = args.hostname
    key_path = args.key
    cert_path = args.cert
    file_path = args.path

    # Change to the specified directory
    os.chdir(file_path)

    try:
        httpd = http.server.HTTPServer((hostname, port), CORSHTTPRequestHandler)
        httpd.socket = ssl.wrap_socket(httpd.socket,
                                       keyfile=key_path,
                                       certfile=cert_path,
                                       server_side=True)

        print(f"Serving HTTPS on {hostname}:{port} with CORS enabled and serving files from: {file_path}")
        httpd.serve_forever()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

