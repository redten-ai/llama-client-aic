import logging
import ujson as json
import requests
import client_aic.get_cfg as get_cfg
import client_aic.models.core_user as core_user
import client_aic.tls.utils as tls_utils


log = logging.getLogger(__name__)


def create_user(
    username: str,
    email: str,
    password: str,
    cfg: dict = None,
):
    """
    create_user

    create a new user in the database
    using the rest api

    :param username: user's username
    :param email: user's email address
    :param password: user's password
    :param cfg: optional **CoreConfig** dictionary

    :returns: **CoreUser** on success
        **None** on failure
    :rtype: CoreUser or None
    """
    if not cfg:
        cfg = get_cfg.get_cfg()
    url = f'https://{cfg["endpoint"]}/user'
    (cert_file, key_file) = tls_utils.get_certs(cfg)
    verify = tls_utils.get_verify(cfg)
    debug = cfg.get("debug", False)
    log.debug(f"create user: {url}")
    s = requests.Session()
    data = {
        "username": username,
        "email": email,
        "password": password,
    }
    r = s.post(
        url,
        json.dumps(data),
        verify=verify,
        cert=(cert_file, key_file),
        timeout=5,
    )
    if r.status_code != 201:
        if debug:
            log.info(
                "\n\n"
                "non-201 response:\n"
                f"  url: {url}\n"
                f"  job_result.id: {id}\n"
                f"  ca={verify}\n"
                f"  response:\n"
                f"  code: {r.status_code}\n"
                f"  text:\n"
                f"  {r.text}\n"
            )
        if "already registered" in r.text:
            log.debug(f"found user={username} e={email}")
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
                    created_at=cur_json.get(
                        "created_at", None
                    ),
                    updated_at=cur_json.get(
                        "updated_at", None
                    ),
                )
                return cur_o
            except Exception as e:
                log.error(
                    "failed to convert "
                    "create_user response to CoreUser "
                    f'with ex="{e}"'
                )
    else:
        log.debug(f"created user={username} e={email}")
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
