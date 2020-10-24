from socketserver import ForkingTCPServer, BaseRequestHandler
from server_tools import ServerTools


class Handler(BaseRequestHandler):
    def handle(self):
        st = ServerTools({'port': '8080', 'ip': 'localhost', 'root': '/', 'size': 1024})
        self.data = self.request.recv(1024)
        print(st.parseGet(self.data))
        # self.request.sendall(st.response404())


with ForkingTCPServer(('localhost', 8081), Handler) as server:
    server.allow_reuse_address = True
    server.serve_forever()
