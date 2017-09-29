import requests
import random
import threading
import sys

HOST, PORT = "localhost", 9999

data_url = "http://localhost:3000/test_data/file"

max_file_count = 9
max_file_name = 9
nthreads = int(sys.argv[1])

def client_method():
    fnames = ''
    nfiles = random.randrange(2, max_file_count)
    for i in range(nfiles):
        fname = data_url + str(random.randrange(1, max_file_name + 1))
        if i != 0:
            fnames += ','
        fnames += fname
    print(fnames)
    r = requests.post("http://{}:{}".format(HOST, PORT), data = fnames, headers={"Content-Length" : str(len(fnames)) } )
    print(r.text)

# Make threads doing this.
for i in range(nthreads):
    th = threading.Thread(target=client_method)
    th.daemon = False
    th.start()
