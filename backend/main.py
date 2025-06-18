from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json
from .auth import register_user, authenticate, create_otp, verify_otp


class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode()
        data = parse_qs(body)

        if self.path == '/register':
            user_id = register_user(
                data.get('username', [''])[0],
                data.get('email', [''])[0],
                data.get('phone', [''])[0],
                data.get('password', [''])[0],
                data.get('role', ['student'])[0]
            )
            otp = create_otp(user_id, 'email')
            self._set_headers()
            self.wfile.write(json.dumps({'user_id': user_id, 'email_otp': otp}).encode())
        elif self.path == '/verify-email':
            success = verify_otp(int(data.get('user_id', ['0'])[0]), data.get('code', [''])[0], 'email')
            if success:
                self._set_headers()
                self.wfile.write(json.dumps({'status': 'verified'}).encode())
            else:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'invalid code'}).encode())
        elif self.path == '/login':
            ok = authenticate(data.get('username', [''])[0], data.get('password', [''])[0])
            if ok:
                self._set_headers()
                self.wfile.write(json.dumps({'status': 'success'}).encode())
            else:
                self._set_headers(401)
                self.wfile.write(json.dumps({'error': 'invalid credentials'}).encode())
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'not found'}).encode())


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server running on port {port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
