#!/usr/bin/env python3

import argparse
import requests
import os

from jinja2 import Environment, FileSystemLoader

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--token", required=True)
parser.add_argument("-e", "--event", required=True)
parser.add_argument("-p", "--prefix", required=True)
parser.add_argument("-n", "--number", required=True, type=int)
parser.add_argument("--pretix-url", default="https://booking.asta.rwth-aachen.de")
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

    name = f"{args.prefix}-{i:03}"
    request_body = {
        "name": name,
        "all_events": False,
        "limit_events": [f"{args.event}"],
        "security_profile":"pretixscan",
    }

    r = requests.post(baseurl + "/api/v1/organizers/asta/devices/", headers=request_headers, json=request_body)

    if r.status_code != 201:
        raise Exception

    # print(r.json())

    qr_data = {
        "handshake_version": 1,
        "url": "https://booking.asta.rwth-aachen.de",
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

