"""
get the rest api address from the
environment variables:

- AI_API=api.redten.io:443
- AI_ENV=dev

"""

import os
import logging


log = logging.getLogger(__name__)


def get_api_address():
    """
    get_api_address

    get the api address for the job backend

    :returns: string for the api endpoint address
    :rtype: str
    """
    if os.getenv("USE_LOCAL", "0") == "1":
        return os.getenv("AI_API", "0.0.0.0:3000")
    else:
        env_name = os.getenv("AI_ENV", "dev")
        base_url = os.getenv("AI_API", "api.redten.io")
        return f"{base_url}/v1/{env_name}"
