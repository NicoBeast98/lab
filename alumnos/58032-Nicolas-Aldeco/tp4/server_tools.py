class ServerTools():

    def __init__(self, argms):
        self.document_root = argms.root[0]
        self.port = argms.port[0]
        self.size = argms.size[0]
        self.ip = argms.ip[0]

        self.prot_ip = 'IPv4'
        if argms.ip[0].find(':') != -1:
            self.prot_ip = 'IPv6'

    def response404(self):
        pass
