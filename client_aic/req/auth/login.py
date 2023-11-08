import os
import logging
import ujson as json
import requests
import client_aic.get_cfg as get_cfg
import client_aic.models.core_user as core_user
import client_aic.tls.utils as tls_utils


log = logging.getLogger(__name__)


def login(
    email: str,
    password: str,
    cfg: dict = None,
    creds_file_path: str = None,
    force: bool = False,
):
    """
    login

    login the user by the **email** and **password**
    on success save the credentials to the
    **creds_file_path** (environment
    variable **AI_CREDS_FILE** supported too)

    log a user into the ai core rest api
    and save the **CoreUser**
    temporary credentials locally to the
    **creds_file** path

    **Optional Settings with Env Vars**

    **Disable saving local credentials json file**

    Disable saving your credentials as a local json
    file for faster requests. By disabling this
    feature, it will force
    the client to re-login to get a valid token (which
    is a more secure mode for production workloads):

    ```bash
    export DISABLE_CRED_CACHE=1
    ```

    **Change the path to the credentials file**

    ```bash
    export AI_CREDS_FILE=path_to_creds.json
    ```

    :param email: user's email address
    :param password: user's password
    :param cfg: optional **CoreConfig** dictionary
    :param creds_file_path: path to a file
        where the user's authenticated credentials
        are saved locally for speeding up
        subsequent api requests
    :param force: flag for overwritting the
        **creds_file_path** like for
        when the **CoreUser**'s token expires

    :returns: **CoreUser** on success
        **None** on non-success
    :rtype: CoreUser or None
    """

    # if no email/password
    # it's in the creds.json
    # or its not a valid api request
    # (env vars are loaded upstream
    # CoreConfig **cfg** dictionary)
    if not email and not password:
        home_dir = os.getenv("HOME", None)
        creds_dir = f"{home_dir}/.redten"
        def_creds_path = f"{creds_dir}/creds.json"
        creds_path = os.getenv(
            "AI_CREDS_FILE",
            cfg.get("ai_creds_file", def_creds_path),
        )
        if creds_file_path:
            creds_path = creds_file_path
        if os.path.exists(creds_path):
            user_json = {}
            with open(creds_path, "r") as fp:
                user_json = json.loads(fp.read())
            user = core_user.CoreUser(
                id=user_json.get("id", -2),
                email=user_json.get("email", "not found"),
                state=user_json.get("state", -2),
                verified=user_json.get("verified", -2),
                role=user_json.get("role", "not found"),
                token=user_json.get("token", "not found"),
                msg=user_json.get("msg", "not found"),
            )
            log.debug(f"using existing creds: {creds_path}")
            return user

    # by here the cfg was already parsed by the authenticate
    # api call so the email/password are required
    if not email and not password:
        log.error(
            "invalid login - missing email and password"
        )
        return None
    if not cfg:
        cfg = get_cfg.get_cfg()
    if not email:
        log.error("invalid login - " "missing email")
        return None
    if not password:
        log.error("invalid login - " "missing password")
        return None
    url = f'https://{cfg["endpoint"]}/login'
    (cert_file, key_file) = tls_utils.get_certs(cfg)
    verify = tls_utils.get_verify(cfg)
    debug = cfg.get("debug", False)
    data = {
        "email": email,
        "password": password,
    }
    log.debug(f"login: {url} data={data} ca={verify}")
    s = requests.Session()
    r = s.post(
        url,
        json.dumps(data),
        verify=verify,
        cert=(cert_file, key_file),
        timeout=10,
    )
    if r.status_code != 201:
        if debug:
            log.error(
                "\n\n"
                "failed login:\n"
                f"url: {url}\n"
                f"data: {data}\n"
                f"ca: {verify}\n"
                f"response:\ncode: {r.status_code}\n"
                f"text:\n{r.text}\n"
            )
        if "invalid password" in r.text:
            log.error(f"invalid password for {email}")
        else:
            test_str = (
                "user does not exist " f"with email={email}"
            )
            if test_str in r.text:
                # likely not an error
                log.debug(f"no user email={email}")
            else:
                log.error(
                    f"no user email={email} "
                    f"response={r.text}"
                )
        return None
    else:
        log.debug(f"login success - {r.text}")
        try:
            user_json = json.loads(r.text)
            user = core_user.CoreUser(
                id=user_json.get("user_id", -2),
                email=user_json.get("email", "not found"),
                state=user_json.get("state", -2),
                verified=user_json.get("verified", -2),
                role=user_json.get("role", "not found"),
                token=user_json.get("token", "not found"),
                msg=user_json.get("msg", "not found"),
            )
            # disable saving creds
            # if the environment variable
            # export DISABLE_CRED_CACHE=1
            if os.getenv("DISABLE_CRED_CACHE", "0") == "0":
                user.save_creds()
            return user
        except Exception as e:
            log.error(f'failed to login with ex="{e}"')
            return None
