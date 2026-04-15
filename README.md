# pretix-checkin-device-qrcode-generator

A tool to mass-generate QR-codes for pretixSCAN initialization.

## Usage

```bash
./generate-device-printouts.py --help
usage: generate-device-printouts.py [-h] -u PRETIX_URL -t TOKEN -o ORGANIZER -e EVENT -p DEVICE_NAME_PREFIX [-g GATE] -n NUMBER

options:
  -h, --help            show this help message and exit
  -u, --pretix-url PRETIX_URL
                        Base URL of the Pretix instance, e.g. 'https://shop.myorg.eu'
  -t, --token TOKEN     Token for Pretix API authentication, see https://docs.pretix.eu/dev/api/tokenauth.html
  -o, --organizer ORGANIZER
                        name of organizer in pretix
  -e, --event EVENT     name of the event in pretix
  -p, --device-name-prefix DEVICE_NAME_PREFIX
                        This plus a incrementing number will show up as the name in the device list
  -g, --gate GATE       Id of the gate to limit access to
  -n, --number NUMBER   Number of QR codes to generate
```

Example:
```bash
./generate-device-printouts.py -u https://shop.myorg.eu/ -t mu5aqua4yie2queimeith1nahwaK3feicheuQuashaiVaeC4geo1eich1queitem -o team -e party -p guestlist -n 2
```
