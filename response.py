import time


class response:

    def __init__(self, status, content_type, data):
        self.status = status
        self.content_type = content_type
        self.data = data
        self.content_length = len(data)

    def getContentLength(self):
        if hasattr(self, 'content_length'):
            return str(self.content_length)
        else:
            return "0"

    def getStatus(self):
        if hasattr(self, 'status'):
            return self.status
        else:
            return "400 Bad Request"

    def getContentType(self):
        if hasattr(self, 'content_type'):
            return "Content-Type: " + self.content_type + ";\r\n"
        else:
            return "Content-Type: text/html\r\n"

    def getData(self):
        if hasattr(self, 'data'):
            return "\r\n" + self.data
        else:
            return ""

    def toString(self):
        return "HTTP/1.0 " + self.getStatus() + "\r\n" + "Date: " + time.strftime("%a, %d %b %Y %H:%M:%S %Z\r\n") + "Accept-Ranges: bytes\r\n" + "Content-Length: " + self.getContentLength() + "\r\n" + "Keep-Alive: timeout=10, max=100\r\n" + self.getContentType() + self.getData()

