"""
build a credential dictionary
from environment variables:

- AI_USER=username
- AI_EMAIL=email@email.com
- AI_PASSWORD=abcdef

"""
import os
import logging


log = logging.getLogger(__name__)


def get_creds():
    """
    get_creds

    get the rest api credentials
    as a dictionary

    :returns: dict for the user credentials
    :rtype: dict
    """
    return {
        "u": os.getenv("AI_USER", None),
        "p": os.getenv("AI_PASSWORD", None),
        "e": os.getenv("AI_EMAIL", None),
    }
