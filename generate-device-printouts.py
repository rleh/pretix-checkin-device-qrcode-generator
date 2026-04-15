#!/usr/bin/env python3

import argparse
import requests
import os

from jinja2 import Environment, FileSystemLoader

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--pretix-url", required=True, help="Base URL of the Pretix instance, e.g. 'https://shop.myorg.eu'")
parser.add_argument("-t", "--token", required=True, help="Token for Pretix API authentication, see https://docs.pretix.eu/dev/api/tokenauth.html")
parser.add_argument("-o", "--organizer", required=True, help="name of organizer in pretix")
parser.add_argument("-e", "--event", required=True, help="name of the event in pretix")
parser.add_argument("-p", "--device-name-prefix", required=True, help="This plus a incrementing number will show up as the name in the device list")
parser.add_argument("-g", "--gate", default="", help="Id of the gate to limit access to")
parser.add_argument("-n", "--number", required=True, type=int, help="Number of QR codes to generate")
#parser.add_argument("-v", "--verbose", action="store_true")
args = parser.parse_args()

token = args.token
baseurl = args.pretix_url

request_headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json",
}


entries = list()

for i in range(args.number):

    name = f"{args.device_name_prefix}-{i:03}"
    request_body = {
        "name": name,
        "all_events": False,
        "limit_events": [f"{args.event}"],
        "security_profile":"pretixscan",
        "gate":f"{args.gate}"
    }

    r = requests.post(f"{baseurl}/api/v1/organizers/{args.organizer}/devices/", headers=request_headers, json=request_body)

    if r.status_code != 201:
        print(r.url + " returned HTTP status code " + str(r.status_code))
        raise Exception

    # print(r.json())

    qr_data = {
        "handshake_version": 1,
        "url": baseurl,
        "token": r.json()["initialization_token"],
    }
    l = {
        "qrdata": str(qr_data).replace("{", "\\{").replace("}", "\\}"),
        "token": r.json()["initialization_token"],
        "name": name,
    }
    entries.append(l)

printout_data = dict()

printout_data["url"] = baseurl
printout_data["event"] = args.event
printout_data["entries"] = entries

dir = os.path.dirname(os.path.realpath(__file__))
tex = Environment(loader=FileSystemLoader(dir)).get_template("printout-template.tex").render(data=printout_data)
with open(str(dir) + "/generated.tex","w+") as f:
    f.write(tex)

