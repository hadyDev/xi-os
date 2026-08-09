from wifi import support as wifi_support
if wifi_support:
    import socket
    import ssl
import garbage

class Session:
    def __init__(self, host, port, agent):
        self.host = host
        self.port = port
        self.agent = agent
        self.s = None
        self.headers = {}
        self.cookies = {}
    
    
    def _connect(self):
        addr_info = socket.getaddrinfo(self.host, self.port)[0][-1]
        s = socket.socket()
        s.connect(addr_info)
        s = ssl.wrap_socket(s, server_hostname = self.host)
        self.s = s
    
    
    def _close(self):
        if self.s:
            try:
                self.s.close()
            except:
                pass
        self.s = None
    
    
    def request(self, method, url, keepalive = False, getbody = True, data = None, **kwargs):
        garbage.collect()
        if not self.s:
            self._connect()
        
        # merge headers
        headers = {"Host": self.host, "Connection": "keep-alive", "User-Agent": ("Deimos/1.0" if not self.agent else self.agent)}
        headers.update(self.headers)
        if "headers" in kwargs:
            headers.update(kwargs["headers"])
            _ = kwargs.pop("headers")
        
        # add cookies to header
        if self.cookies:
            cookie_header = "; ".join((k + "=" + v for k, v in self.cookies.items()))
            headers["Cookie"] = cookie_header
        
        # make the request
        rq = method + " " + url + " HTTP/1.1\r\n"
        for k, v in headers.items():
            rq += k + ": " + v + "\r\n"
        
        if data:
            rq += "Content-Length: " + (str((len(data)))) + "\r\n"
        
        rq += "\r\n"
        
        rq = rq.encode()
        
        # parse data
        if data:
            if isinstance(data, str):
                data = data.encode()
            rq += data
        
        print(rq)
        
        # send the request
        self.s.write(rq)
        
        # get the response
        resp = b""
        while True:
            chunk = self.s.readline()
            if not chunk or chunk == b"\r\n":
                break
            resp += chunk
        resp = resp.decode()
        body = b""
        
        headers = {}
        status_line = " -1"
        for line in resp.split("\r\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                headers[k.strip()] = v.strip()
            elif line.startswith("HTTP/"):
                status_line = line
            
        status = int(status_line.split(" ")[1])
        
        # capture cookies
        for k, v in headers.items():
            if k.lower() == "set-cookie":
                cookie = v.split(";", 1)[0]
                ck, cv = cookie.split("=", 1)
                self.cookies[ck.strip()] = cv.strip()
        
        # determine body reading mode
        garbage.collect()
        clen = headers.get("Content-Length")
        if clen:
            l = int(clen)
            chunk = b""
            while len(chunk) < l:
                chunk = self.s.read(l - len(chunk))
            if getbody:
                body += chunk
        elif headers.get("Transfer-Encoding") == "chunked":
            while True:
                line = self.s.readline()
                if not line:
                    break
                csize = line.strip().split(b";")[0]
                if not csize:
                    continue
                csize = int(csize, 16)
                if csize == 0:
                    self.s.readline()
                    break
                chunk = b""
                while len(chunk) < csize:
                    if getbody:
                        chunk += self.s.read(csize - len(chunk))
                    else:
                        self.s.read(csize - len(chunk))
                if getbody:
                    body += chunk
                self.s.readline()
        else:
            pass
            # @.s.settimeout(1)
            # try
            #     while True
            #         part = @.s.read(512)
            #         if not part; break;.
            #         body += part
            #     .
            # .catch OSError;;
            # .finally
            #     @.s.settimeout(5)
            # .
        
        print("RESP")
        print(resp)
        
        if not keepalive:
            print("closing connection")
            self._close()
        
        return {"status": status, "headers": headers, "body": body, "response": resp}
    
    
    def get(self, url, **kwargs):
        return self.request("GET", url, **kwargs)
    
    def post(self, url, data = None, **kwargs):
        return self.request("POST", url, data = data, **kwargs)
    
    
    def close(self):
        return self._close()
    

