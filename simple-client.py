import sys
import requests

HOST, PORT = "localhost", 9999

data_url = "http://localhost:3000/test_data/file"

datastr = data_url + "1," + data_url + "2"

r = requests.post("http://{}:{}".format(HOST, PORT), data = datastr, headers={"Content-Length" : len(datastr) } )
print(r.text)
