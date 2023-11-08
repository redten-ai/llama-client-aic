"""
core configuration object
for all client api requests
"""
import logging
import client_aic.config.get_creds as get_creds
import client_aic.config.get_tls as get_tls
import client_aic.config.get_api_address as get_api_address


log = logging.getLogger(__name__)


class CoreConfig:
    """CoreConfig"""

    def __init__(self):
        """
        __init__

        contstructor
        """
        self.cfg = {
            "user": get_creds.get_creds(),
            "tls": get_tls.get_tls(),
            "endpoint": get_api_address.get_api_address(),
        }

    def get_cfg(self):
        """
        get_cfg

        get the internal dictionary

        :returns: dictionary **self.cfg**
        :rtype: dict
        """
        if self.cfg:
            return self.cfg
        else:
            log.debug("config={}", self.cfg)
            return {
                "user": get_creds.get_creds(),
                "tls": get_tls.get_tls(),
                "endpoint": get_api_address.get_api_address(),
            }

    def get_endpoint(self):
        """
        get_endpoint

        get the api endpoint address

        :returns: dictionary **self.cfg**
        :rtype: dict
        """
        if self.cfg:
            return self.cfg.get(
                "endpoint",
                get_api_address.get_api_address(),
            )
        else:
            return get_api_address.get_api_address()

    def show(self):
        """
        show

        helper function for debugging
        """
        log.debug("config={}", self.cfg)
