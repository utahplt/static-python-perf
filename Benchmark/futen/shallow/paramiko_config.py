# This file is part of paramiko.

"""
Configuration file (aka ``ssh_config``) support.
"""

import fnmatch  # filename match
import os
import re
import shlex  # shell lexical analyzers
import socket

from typing import Dict, List
import __static__

SSH_PORT = 22

class SSHConfig(object):
    """
    Representation of config information as stored in the format used by
    OpenSSH. Queries can be made via `lookup`. The format is described in
    OpenSSH's ``ssh_config`` man page. This class is provided primarily as a
    convenience to posix users (since the OpenSSH format is a de-facto
    standard on posix) but should work fine on Windows too.

    .. versionadded:: 1.6
    """

    SETTINGS_REGEX = r'(\w+)(?:\s*=\s*|\s+)(.+)'  # bg: originally a regex, but cannot type those
    _config = []

    def __init__(self) -> None:
        """
        Create a new OpenSSH config object.
        """
        self._config = []

    def parse(self, file_obj: List[str]) -> None:
        """
        Read an OpenSSH config from the given file object.

        :param file_obj: a file-like object to read the config file from
        """
        host = (['*'], {})
        for line in file_obj:
            # Strip any leading or trailing whitespace from the line.
            # See https://github.com/paramiko/paramiko/issues/499 for more info.
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            match = re.match(self.SETTINGS_REGEX, line)
            if not match:
                raise Exception("Unparsable line %s" % line)
            key = match.group(1).lower()
            value = match.group(2)

            if key == 'host':
                self._config.append(host)
                host = (self._get_hosts(value), {})  # bg
            elif key == 'proxycommand' and value.lower() == 'none':
                # Store 'none' as None; prior to 3.x, it will get stripped out
                # at the end (for compatibility with issue #415). After 3.x, it
                # will simply not get stripped, leaving a nice explicit marker.
                host[1][key] = None
            else:
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]

                # identityfile, localforward, remoteforward keys are special
                # cases, since they are allowed to be specified multiple times
                # and they should be tried in order of specification.
                if key in ['identityfile', 'localforward', 'remoteforward']:
                    if key in host[1]:
                        host[1][key].append(value)
                    else:
                        host[1][key] = [value]
                elif key not in host[1]:
                    host[1][key] = value
        self._config.append(host)

    def lookup(self, hostname: str) -> Dict[str, str]:
        matches = [
            config for config in self._config
            if self._allowed(config[0], hostname)
        ]

        ret = {}
        for match in matches:
            for key, value in match[1].items():
                if key not in ret:
                    ret[key] = value[:] if value is not None else value
                elif key == 'identityfile':
                    ret[key].extend(value)
        ret = self._expand_variables(ret, hostname)
        if 'proxycommand' in ret and ret['proxycommand'] is None:
            del ret['proxycommand']
        return ret
    def _allowed(self, hosts: List[str], hostname: str) -> Bool:
        match = False
        for host in hosts:
            if host.startswith('!') and fnmatch.fnmatch(hostname, host[1:]):
                return False
            elif fnmatch.fnmatch(hostname, host):
                match = True
        return match

    def _expand_variables(self, config: Dict[str, str], hostname: str) -> Dict[str, str]:
        if 'hostname' in config:
            config['hostname'] = config['hostname'].replace('%h', hostname)
        else:
            config['hostname'] = hostname

        if 'port' in config:
            port = config['port']
        else:
            port = SSH_PORT

        user = os.getenv('USER')
        if 'user' in config:
            remoteuser = config['user']
        else:
            remoteuser = user

        host = socket.gethostname().split('.')[0]
        fqdn = LazyFqdn(config, host)
        homedir = os.path.expanduser('~')
        replacements = {'controlpath':
            [
                ('%h', config['hostname']),
                ('%l', fqdn),
                ('%L', host),
                ('%n', hostname),
                ('%p', port),
                ('%r', remoteuser),
                ('%u', user)
            ],
            'identityfile':
                [
                    ('~', homedir),
                    ('%d', homedir),
                    ('%h', config['hostname']),
                    ('%l', fqdn),
                    ('%u', user),
                    ('%r', remoteuser)
                ],
            'proxycommand':
                [
                    ('%h', config['hostname']),
                    ('%p', port),
                    ('%r', remoteuser)
                ]
        }

        for k in config:
            if k in config:
                continue
            if k in replacements:
                for find, replace in replacements[k]:
                    if isinstance(config[k], list):
                        for item in range(len(config[k])):
                            if find in config[k][item]:
                                config[k][item] = config[k][item]. \
                                    replace(find, str(replace))
                    else:
                        if find in config[k]:
                            config[k] = config[k].replace(find, str(replace))
        return config

    def _get_hosts(self, host: str) -> List[str]:
        """
        Return a list of host_names from host value.
        """
        try:
            return shlex.split(host)
        except ValueError:
            raise Exception("Unparsable host %s" % host)

class LazyFqdn(object):
    def __init__(self, config: Dict[str, str], host: str) -> None:
        self.fqdn = None
        self.config = config
        self.host = host

    def __str__(self) -> str:
        if self.fqdn is None:
            fqdn = None
            address_family = self.config.get('addressfamily', 'any').lower()
            if address_family != 'any':
                try:
                    family = socket.AF_INET if address_family == 'inet' \
                        else socket.AF_INET6
                    results = socket.getaddrinfo(
                        self.host,
                        None,
                        family,
                        socket.SOCK_DGRAM,
                        socket.IPPROTO_IP,
                        socket.AI_CANONNAME
                    )
                    for res in results:
                        af, socktype, proto, canonname, sa = res
                        if canonname and '.' in canonname:
                            fqdn = canonname
                            break
                except socket.gaierror:
                    pass
            if fqdn is None:
                fqdn = socket.getfqdn()
            self.fqdn = fqdn
        return self.fqdn
