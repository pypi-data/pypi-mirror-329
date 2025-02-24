import ipaddress
import requests


def get():
    r = requests.get('http://ifconfig.co/ip')
    if r.status_code == 200:
        return r.text.strip()
    else:
        return None
    

def is_ipv4(string):
    try:
        ipaddress.IPv4Network(string)
        return True
    except ValueError:
        return False