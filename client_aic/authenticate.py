import logging
import uuid
import client_aic.get_cfg as get_cfg
import client_aic.req.auth.login as login
import client_aic.req.user.create_user as create_user
import client_aic.req.user.get_user as get_user


log = logging.getLogger(__name__)


def authenticate(
    username: str = None,
    email: str = None,
    password: str = None,
    auto_create: bool = True,
    cfg: dict = None,
):
    """
    authenticate

    helper for authenticating as a new or
    existing user based off either the
    username/password/email or **CoreConfig**
    cfg dictionary. requires using
    credentials from one or the other.

    :param username: optional username
    :param email: optional email
    :param password: optional password
    :param auto_create: optional flag for
        creating a user if they do not exist
        already and the default is **True**
    :param cfg: optional **CoreConfig** dictionary

    :returns: **CoreUser** if success
        **None** if non-success
    :rtype: CoreUser
    """
    if not cfg:
        cfg = get_cfg.get_cfg()
    cfg_user = cfg.get("user", {})

    use_username = username
    use_password = password
    use_email = email
    if len(cfg_user) > 0:
        if not username:
            use_username = cfg_user.get("u", username)
        if not password:
            use_password = cfg_user.get("p", password)
        if not email:
            use_email = cfg_user.get("e", email)

    user = None
    try:
        user = login.login(
            email=email,
            password=password,
            cfg=cfg,
            # force = support for saving a new token
            # locally again in case the old one expired
            force=False,
        )
        if not user:
            if not use_username:
                use_uuid = str(uuid.uuid4()).replace(
                    "-", ""
                )
                use_username = f"rt.2023.{use_uuid}"
            if auto_create:
                log.debug(
                    f"creating user email={use_email}"
                )
                create_user.create_user(
                    username=use_username,
                    password=use_password,
                    email=use_email,
                    cfg=cfg,
                )
            log.debug(
                "trying to login with force "
                f"user with email={use_email}"
            )
            user = login.login(
                email=use_email,
                password=use_password,
                cfg=cfg,
                # force = support for saving a new token
                # locally again in case the old one expired
                force=True,
            )
            log.debug("validating access with token")
            found_user = get_user.get_user(
                id=user.id,
                user=user,
                cfg=cfg,
            )
            if not found_user:
                log.error(
                    f"failed to get user.id={user.id}"
                )
                return None
        # end of login
        log.debug("done")
    except Exception as e:
        log.error(
            f'failed to auth user={email} with e="{e}"'
        )
    return user
