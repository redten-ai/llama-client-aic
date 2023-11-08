import os
import ujson as json
import logging


log = logging.getLogger(__name__)


class CoreUser:
    """## CoreUser"""

    def __init__(
        self,
        id: int,
        email: str,
        state: int,
        verified: int,
        role: str,
        token: str,
        msg: str,
        created_at: str = None,
        updated_at: str = None,
    ):
        """
        __init__

        user representation for the rest api

        :param id: user primary key
            value from the db
        :param email: user's email address
        :param state: is the user
            active/inactive/banned
        :param verified: has the user
        :param role: user's role
        :param token: auth token for
            user to access resources using
            the rest api
        :param msg: debugging message
            from the rest api
        :param created_at: utc timestamp creation date
        :param updated_at: utc timestamp last update
        """
        self.id = id
        self.email = email
        self.state = state
        self.verified = verified
        self.role = role
        self.token = token
        self.msg = msg
        self.auth_header = None
        home_dir = os.getenv("HOME", None)
        self.creds_dir = f"{home_dir}/.redten"
        self.creds_path = f"{self.creds_dir}/creds.json"
        self.created_at = created_at
        self.updated_at = updated_at

    def show(self):
        """
        show

        debugging helper

        :returns: None
        :rtype: None
        """
        log.info(
            f"name={self.name} email={self.email} "
            f"s={self.state} v={self.verified} "
            f"r={self.role} t={self.token} "
            f"m={self.msg}"
            ""
        )

    def get_auth_header(self):
        """
        get_auth_header

        build the HTTP rest api auth
        header using the **self.token**
        member

        :returns: HTTP header string to use for an
            authenticated **CoreUser**
        :rtype: str
        """
        if not self.auth_header:
            self.auth_header = f"Bearer: {self.token}"
        return self.auth_header

    def save_creds(self):
        """
        save_creds

        save credentials to a local file
        to request subsequent api calls faster

        :returns: None
        :rtype: None
        """
        log.debug(f"saving creds to: {self.creds_path}")
        if not os.path.exists(self.creds_dir):
            os.makedirs(self.creds_dir)
        config = {
            "id": self.id,
            "email": self.email,
            "state": self.state,
            "verified": self.verified,
            "role": self.role,
            "token": self.token,
        }
        with open(self.creds_path, "w") as fp:
            fp.write(json.dumps(config))
        log.debug(f"saved creds to: {self.creds_path}")
