#!/usr/bin/env python3

import argparse
import logging
import sys

from . import ip
from . import route53 as r53
from . import cloudflare as cf


def route53_command(args, ip_address):
    if r53.update_dns(
        hosted_zone=args.hosted_zone_id,
        name=args.name,
        ip=ip_address
    ):
        logging.info(f"IP on {args.hosted_zone_id} for {args.name} updated to {ip_address}.")
    else:
        logging.info(f"IP on {args.hosted_zone_id} for {args.name} failed to update to {ip_address}.")
        

def cloudflare_command(args, ip_address):
    if cf.update_dns(
        domain=args.domain,
        name=args.name,
        ip=ip_address
    ):
        logging.info(f"IP on {args.domain} for {args.name} updated to {ip_address}.")
    else:
        logging.info(f"IP on {args.domain} for {args.name} failed to update to {ip_address}.")

def main():
    parser = argparse.ArgumentParser(
        description="DNSupdater: Update an AWS R53 Hosted Zone or Cloudflare domain with your current IP"
    )
    parser.add_argument("-l", "--log", dest="logLevel",
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help="set the logging level", default="INFO")

    parser.add_argument("-n", "--name", type=str, required=True, help="record name")
    parser.add_argument("-i", "--ip", type=str,
                        help='IP address. If not provided ifconfig.co will be queried.')

    subparsers = parser.add_subparsers(required=True, title='subcommands', 
                                       help='select DNS provider')
    parser_r53 = subparsers.add_parser("route53", aliases=['r53'], help="R53 provider")
    parser_r53.set_defaults(func=route53_command)
    parser_r53.add_argument("--hosted-zone-id", type=str, required=True, help="hosted zone ID")

    parser_cloudflare = subparsers.add_parser("cloudflare", aliases=['cf'], help="Cloudflare provider")
    parser_cloudflare.add_argument("--domain", type=str, required=True, help="CF Domain")
    parser_cloudflare.set_defaults(func=cloudflare_command)

    args = parser.parse_args()

    logging.basicConfig(level=args.logLevel)

    if args.ip:
        if not ip.is_ipv4(args.ip):
            sys.exit("Provided IP address is invalid. Use a valid IPv4.")
            
        ip_address = args.ip
    else:
        ip_address = ip.get()
    if not ip_address:
        sys.exit("IP cannot be retrieved.")

    args.func(args, ip_address)

if __name__== "__main__":
  main()
