"""
create a config object that holds
regularly-used values:

- endpoint
- tls/mtls
- auth creds

"""
import logging
import client_aic.config.core_config as core_config


log = logging.getLogger(__name__)


def get_cfg():
    """
    get_cfg

    build a common configuration for
    all client requests and shared state

    :returns: dictionary for the **CoreConfig**
    :rtype: dict
    """
    cfg = core_config.CoreConfig()
    log.debug(f"using cfg={cfg.get_cfg()}")
    return cfg.get_cfg()
