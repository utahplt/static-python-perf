#import sys
#import argparse
import os
from paramiko_config import SSHConfig
import __static__
from typing import Dict, Tuple, List

NO_PORT = "-1" #bg

def parse(lines: List[str]) -> SSHConfig:
    parser = SSHConfig()
    parser.parse(lines)
    return parser

def get_netloc(entry: Tuple[List[str], Dict[str, str]], parser: SSHConfig) -> Tuple[str, str]:
    hostname = "".join(entry[0])  # bg
    if hostname == "*":
        return ("*", NO_PORT)
    port = parser.lookup(hostname).get('port')
    return (hostname, port)


def get_netlocs(lines: List[str]) -> Dict[str, str]:
    parser = parse(lines)
    entries = parser._config
    netlocs = {}
    for entry in entries:
        netloc = get_netloc(entry, parser)
        if not netloc:
            continue
        hostname, port = netloc
        if port != NO_PORT:
            netlocs[hostname] = port
    return netlocs

def execute(lines: List[str], template_file: str) -> str:
    netlocs = get_netlocs(lines)

    # bg simplified
    dirpath, filename = os.path.split(template_file)
    template_context = [
        (hostname, '%s:%s' % (hostname, port))
        for hostname, port in netlocs.items()
    ]
    return str(sorted(template_context, key=lambda x: x[0]))