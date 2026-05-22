from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
import urllib.request
import urllib.error
import socket
import threading
import os

# Disable proxy for the proxy itself to avoid infinite loops
proxy_handler = urllib.request.ProxyHandler({})
opener = urllib.request.build_opener(proxy_handler)
urllib.request.install_opener(opener)

class PastebinProxy(BaseHTTPRequestHandler):
    def handle_request(self):
        url = self.path
        if url.startswith("/"):
            # If it's a relative path, we might be in trouble as a proxy, 
            # but let's try to handle the "prefix" use case too.
            if url.startswith("/http"):
                url = url.lstrip("/")
            else:
                # If it's just /foo, and we are a proxy, we should check Host header
                host = self.headers.get("Host")
                if host:
                    url = f"http://{host}{url}"
                else:
                    self.send_error(400, "Bad Request: No host specified")
                    return

        # Rewrite pastebin URLs
        if "pastebin.com" in url:
            url = url.replace("pastebin.com", "pastebinp.com")

        try:
            # Read request body if present
            content_length = int(self.headers.get('Content-Length', 0))
            req_body = self.rfile.read(content_length) if content_length > 0 else None

            # Copy headers, but remove some that might cause issues
            headers = {k: v for k, v in self.headers.items() if k.lower() not in ("host", "proxy-connection", "connection", "transfer-encoding")}
            headers["User-Agent"] = "Mozilla/5.0"
            
            req = urllib.request.Request(url, data=req_body, headers=headers, method=self.command)
            with urllib.request.urlopen(req, timeout=30) as r:
                self.send_response(r.status)
                for key, val in r.headers.items():
                    # Do not pass through Transfer-Encoding as urllib has already decoded it
                    if key.lower() not in ("transfer-encoding",):
                        self.send_header(key, val)
                self.end_headers()
                
                # Stream the response body
                while True:
                    chunk = r.read(16384)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
        except Exception as e:
            self.send_response(502)
            self.end_headers()
            self.wfile.write(f"Proxy Error: {str(e)}".encode())

    def do_GET(self): self.handle_request()
    def do_POST(self): self.handle_request()
    def do_PUT(self): self.handle_request()
    def do_DELETE(self): self.handle_request()
    def do_HEAD(self): self.handle_request()
    def do_OPTIONS(self): self.handle_request()

    def do_CONNECT(self):
        # Tunnel HTTPS connections directly
        host, _, port = self.path.partition(":")
        port = int(port) if port else 443
        try:
            remote = socket.create_connection((host, int(port)), timeout=15)
            self.send_response(200, "Connection Established")
            self.end_headers()

            def pipe(src, dst):
                try:
                    while True:
                        chunk = src.read(8192)
                        if not chunk:
                            break
                        dst.write(chunk)
                        dst.flush()
                except:
                    pass

            client_read = self.connection.makefile("rb", buffering=0)
            client_write = self.connection.makefile("wb", buffering=0)
            remote_read = remote.makefile("rb", buffering=0)
            remote_write = remote.makefile("wb", buffering=0)

            t1 = threading.Thread(target=pipe, args=(client_read, remote_write), daemon=True)
            t2 = threading.Thread(target=pipe, args=(remote_read, client_write), daemon=True)
            t1.start(); t2.start()
            # In ThreadingHTTPServer, we can join here and it will only block this connection's thread
            t1.join(); t2.join()
        except Exception as e:
            try:
                self.send_response(502)
                self.end_headers()
            except:
                pass

    def log_message(self, *args):
        pass

if __name__ == "__main__":
    print("Starting Threading Proxy on 127.0.0.1:8080...")
    ThreadingHTTPServer(("127.0.0.1", 8080), PastebinProxy).serve_forever()
