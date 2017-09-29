# Author: Laura Ekstrand (laura@jlekstrand.net)
# Adapted from an example of socketserver.
# https://docs.python.org/3.5/library/socketserver.html
import http.server
import socketserver
import threading
import socket
import requests

##  Text methods
# Remove integers
def removeIntegers(text):
    for i in range(10):
        text = text.split(str(i))
        text = ''.join(text)
    return text

# De-duplicate chars
def deDuplicate(text):
    # Have to use a dictionary instead of a 26-element array
    # because I can't guarantee that all the chars are alphabetic.
    # I'm in utf-8.
    # Otherwise, the array would be more performant.
    d = dict()
    for char in text:
        d[char] = 1
    text = ''.join(sorted(d.keys()))
    return text


##  The server.
class ThreadingHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    pass

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):

        # When reading the data, you have to have the content_length,
        # otherwise the server will pause forever trying to read more bytes.
        # Then, the client hangs (= REALLY BAD THING).
        content_length = int(self.headers['Content-Length'])
        with self.rfile as f:
            data = f.read(content_length);

        # Print the thread I'm on
        cur_thread = threading.current_thread()
        response_str = "{}: {}".format(cur_thread.name, data)
        print(response_str)

        # Open the urls and do the string processing.
        url_list = str(data, 'utf-8').split(',')
        ret = ''
        for url in url_list:
            if (url != ''):
                r = requests.get(url)
                print("{} : {}".format(url, r.text[:100]))
                ret += r.text
        ret = removeIntegers(ret)
        ret = deDuplicate(ret)
        ret = ret.strip()
        print("Result = {}".format(ret))
        retdata = bytes(ret, 'utf-8')

        # # reply
        self.send_response_only(202)
        self.end_headers()
        self.wfile.write(retdata) # You have to wait to do this until after sending the response headers.

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    server = ThreadingHTTPServer((HOST, PORT), MyHandler)

    # Start a thread with the server, then that thread can spawn one new one each
    # time I get a new request
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True # Stops abruptly at shutdown.
    server_thread.start()
    print("Server loop running on port {} in thread: {}".format(PORT, server_thread.name))
    server_thread.join()
