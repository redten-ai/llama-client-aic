"""
Use environment variables to enable tls

- AI_API_CA=./tls/ca/ca.pem
- AI_API_CERT=./tls/api/server.pem
- AI_API_KEY=./tls/api/server-key.pem

by default uses Let's Encrypt and supports
self-signed tls certs/key/ca

"""
import os
import logging


log = logging.getLogger(__name__)


def get_tls():
    """
    get_tls

    return a dictionary for the ca, cert and key from
    environment variables:

    - AI_API_CA
    - AI_API_CERT
    - AI_API_KEY

    :returns: dict for any self-signed tls assets
    :rtype: dict
    """
    if os.getenv("USE_LOCAL", "0") == "1":
        return {
            "ca": os.getenv("AI_API_CA", None),
            "cert": os.getenv(
                "AI_API_CERT",
                "./tls/api/server.pem",
            ),
            "key": os.getenv(
                "AI_API_KEY",
                ",/tls/api/server-key.pem",
            ),
        }
    else:
        return {
            "ca": os.getenv("AI_API_CA", None),
            "cert": os.getenv("AI_API_CERT", None),
            "key": os.getenv("AI_API_KEY", None),
        }
