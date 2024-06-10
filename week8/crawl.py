import ssl
import urllib.request as req
from urllib.parse import urljoin
import json
import csv


# Disable SSL certificate verification
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Load JSON file 1
json1_src = "https://www.ntu.edu.tw/"
with req.urlopen(json1_src, context=ssl_context) as response:
    json1_data = json.load(response)

print(json1_data)

