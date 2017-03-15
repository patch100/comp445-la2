class request:
    def __init__(self, method, directory):
        self.method = method
        self.filename = directory

    def getMethod(self):
        if hasattr(self, 'method'):
            return self.method.upper()
        else:
            return ""

    def getDirectory(self):
        if hasattr(self, 'directory'):
            return self.filename
        else:
            return ""

    def getBody(self):
        if hasattr(self, 'body'):
            return self.body
        else:
            return ""

    def getHeaders(self):
        if hasattr(self, 'headers'):
            return self.headers
        else:
            return []

    def getHeader(self, key):
        if hasattr(self, 'headers'):
            for h in self.headers:
                if key == str(h[0]):
                    return h
            return ("Accept","text/plain")
        else:
            return ("Accept", "text/plain")


    def setBody(self, body):
        self.body = body

    def addHeader(self, header):
        if hasattr(self, 'headers'):
            self.headers.append(header)
        else:
            self.headers = [header]

    def setHeaders(self, headers):
        self.headers = headers



