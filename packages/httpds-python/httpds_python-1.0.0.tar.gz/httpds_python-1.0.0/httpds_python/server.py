import http.server
import ssl
import argparse
import sys

VERSION = "1.0.0"

class CORSHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        super().end_headers()


def main():
    parser = argparse.ArgumentParser(description="Simple HTTPS server with CORS support.")
    parser.add_argument('port', type=int, help="Port number to run the server on.")
    parser.add_argument('--key', '-k', required=True, help="Path to the SSL key file.")
    parser.add_argument('--cert', '-c', required=True, help="Path to the SSL certificate file.")
    parser.add_argument('--version', '-v', action='version', version=f'%(prog)s {VERSION}', help="Show version")

    args = parser.parse_args()

    port = args.port
    key_path = args.key
    cert_path = args.cert

    try:
        httpd = http.server.HTTPServer(('0.0.0.0', port), CORSHTTPRequestHandler)
        httpd.socket = ssl.wrap_socket(httpd.socket,
                                       keyfile=key_path,
                                       certfile=cert_path,
                                       server_side=True)

        print(f"Serving HTTPS on port {port} with CORS enabled...")
        httpd.serve_forever()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

