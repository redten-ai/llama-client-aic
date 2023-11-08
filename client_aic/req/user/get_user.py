"""
get the user record from the db
"""

import logging
import ujson as json
import requests
import client_aic.get_cfg as get_cfg
import client_aic.models.core_user as core_user
import client_aic.tls.utils as tls_utils


log = logging.getLogger(__name__)


def get_user(
    id: int,
    user: core_user.CoreUser,
    cfg: dict = None,
):
    """
    get_user

    get the user from the db by the
    **CoreUser.id**

    :param id: user's id
    :param CoreUser user: authenticated user
        that is making this request
    :param cfg: optional - **CoreConfig** dictionary

    :returns: **CoreUser** on success
        **None** on failure
    :rtype: CoreUser or None
    """
    if not cfg:
        cfg = get_cfg.get_cfg()
    url = f'https://{cfg["endpoint"]}/user/{id}'
    (cert_file, key_file) = tls_utils.get_certs(cfg)
    verify = tls_utils.get_verify(cfg)
    debug = cfg.get("debug", False)
    log.debug(f"get user: {url}")
    s = requests.Session()
    s.headers.update({"Bearer": f"{user.token}"})
    r = s.get(
        url,
        verify=verify,
        cert=(cert_file, key_file),
        timeout=5,
    )
    if r.status_code != 200:
        if debug:
            log.info(
                "\n\n"
                "non-200 response:\n"
                f"  url: {url}\n"
                f"  job_result.id: {id}\n"
                f"  ca={verify}\n"
                f"  response:\n"
                f"  code: {r.status_code}\n"
                f"  text:\n"
                f"  {r.text}\n"
            )
        return None
    else:
        log.debug(f"got user.id={id}")
        try:
            cur_json = json.loads(r.text)
            cur_o = core_user.CoreUser(
                id=cur_json.get("id", None),
                email=cur_json.get("email", None),
                state=cur_json.get("state", None),
                verified=cur_json.get("verified", None),
                role=cur_json.get("role", None),
                token=cur_json.get("token", None),
                msg=cur_json.get("msg", None),
                created_at=cur_json.get("created_at", None),
                updated_at=cur_json.get("updated_at", None),
            )
            return cur_o
        except Exception as e:
            log.error(
                "failed to convert response to CoreUser "
                f'with ex="{e}"'
            )
    return None
