import usocket

def request(method, url, data=None, json=None, headers={}, stream=None):
    _, _, host, path = url.split('/', 3)
    addr = usocket.getaddrinfo(host, 80)[0][-1]
    s = usocket.socket()
    s.connect(addr)
    s.send('{} /{} HTTP/1.0\r\nHost: {}\r\n\r\n'.format(method, path, host))
    resp = b""
    while True:
        data = s.recv(100)
        if data:
            resp += data
        else:
            break
    s.close()
    return resp

def get(url, **kw):
    return request("GET", url, **kw)
