"""
helpers for common tls lookups
into the **CoreConfig** dictionary
"""

import logging


log = logging.getLogger(__name__)


def get_ca(cfg: dict):
    """
    get_ca

    :param cfg: existing config dict

    :return str: path to certificate authority (CA)
        file

    :returns: path to the CA file
    :rtype: str
    """
    ca_file = cfg["tls"]["ca"]
    return ca_file


def get_certs(cfg: dict):
    """
    get_certs

    :param cfg: existing config dict

    :returns: tuple where (
        **cert_file**, **key_file**
        ) for the client key/certificate files
    :rtype: tuple
    """
    cert_file = cfg["tls"]["cert"]
    key_file = cfg["tls"]["key"]
    return (cert_file, key_file)


def get_verify(cfg: dict):
    """
    get_verify

    :param cfg: existing config dict

    :returns: path to certificate authority
        file
    :rtype: tuple
    """
    verify = cfg["tls"].get("ca", None)
    if not verify:
        log.debug(
            "tls config - no ca set - verify disabled"
        )
    return verify
