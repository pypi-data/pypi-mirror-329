"""
This module contains a subset of //tobikodata/tcloud/auth.py that only is
concerened with the ability to load and refresh a tcloud JWT token.  It also
providers a PublicHttpClient child class that uses tcloud JWT tokens to
authenticate.  There is code duplication between this and tcloud due to the
isolation that tcloud needs.
"""

import os
import stat
import time
import typing as t
from pathlib import Path

from authlib.integrations.requests_client import OAuth2Session
from httpx import Auth, HTTPStatusError, Request, Response
from rich.console import Console
from rich.theme import Theme
from ruamel.yaml import YAML

from tobikodata.http_client.public import PublicHttpClient

# Yaml
yaml = YAML()

# This is duplicated from tcloud in order to avoid pulling in tcloud deps into
# http client
SCOPE = os.environ.get("TCLOUD_SCOPE", "tbk:scope:projects")
"""The scopes to request from the tobiko auth service"""

TCLOUD_PATH = Path(os.environ.get("TCLOUD_HOME", Path.home() / ".tcloud"))
"""The location of the tcloud config folder"""

CLIENT_ID = os.environ.get("TCLOUD_CLIENT_ID", "f695a000-bc5b-43c2-bcb7-8e0179ddff0c")
"""The OAuth client ID to use"""

CLIENT_SECRET = os.environ.get("TCLOUD_CLIENT_SECRET")
"""The OAuth client secret to use for the client credentials (service-to-service) flow"""

TOKEN_URL = os.environ.get("TCLOUD_TOKEN_URL", "https://cloud.tobikodata.com/auth/token")
"""The OAuth token endpoint to use"""

THEME = Theme(
    {
        "info": "bright_white",
        "dim": "white",
        "error": "red",
        "success": "green",
        "url": "bright_blue",
        "key": "bright_yellow",
        "provider": "bright_magenta",
        "tobiko": "#FF5700",
    }
)
"""The Rich console theme to use in the CLI"""


class SSOAuth:
    """
    This class handles the OAuth flows and CLI process for refreshing an ID
    Token from tcloud.  Authentication initially must be done with tcloud.
    """

    @staticmethod
    def _auth_yaml_path() -> Path:
        if not TCLOUD_PATH.exists():
            TCLOUD_PATH.mkdir(parents=True, exist_ok=True)
        return TCLOUD_PATH / "auth.yaml"

    @staticmethod
    def _delete_auth_yaml() -> None:
        """
        Removes the auth.yaml file if it exists.
        """
        auth_path = SSOAuth._auth_yaml_path()

        if auth_path.exists() and os.access(auth_path, os.W_OK):
            os.remove(auth_path)

    @staticmethod
    def _load_auth_yaml() -> t.Optional[t.Dict]:
        """
        Loads the full auth.yaml file that might exist in the CLI config folder.
        """
        auth_path = SSOAuth._auth_yaml_path()

        if auth_path.exists() and os.access(auth_path, os.R_OK):
            with auth_path.open("r") as fd:
                return yaml.load(fd.read())

        return None

    @staticmethod
    def _save_auth_yaml(data: t.Dict) -> None:
        """
        Saves the given dictionary to auth.yaml

        Args:
            data: The dictionary to save
        """
        auth_path = SSOAuth._auth_yaml_path()

        with auth_path.open("w") as fd:
            yaml.dump(data, fd)
        os.chmod(auth_path, stat.S_IWUSR)

    def __init__(self) -> None:
        self.console = Console(theme=THEME)
        self.session = OAuth2Session(CLIENT_ID, CLIENT_SECRET, scope=SCOPE)
        self.tokenInfo = SSOAuth._load_auth_yaml()

    def id_token(self) -> t.Optional[str]:
        """
        Returns the id_token needed for SSO.  Will return the one saved on disk,
        unless it's expired.  If the token on disk is expired, it will try to
        refresh it.
        """

        if self.tokenInfo:
            # If we are within 5 minutes of expire time, run refresh
            if self.tokenInfo.get("expires_at", 0.0) > (time.time() + 300):
                # We have a current token on disk, return it
                return self.tokenInfo["id_token"]

            else:
                # Our token is expired, refresh it if possible
                try:
                    refreshed_token = self.refresh_token()

                    if refreshed_token:
                        return refreshed_token

                    # We failed to refresh, logout
                    SSOAuth._delete_auth_yaml()

                except Exception:
                    # We failed to refresh, logout
                    SSOAuth._delete_auth_yaml()

        # Can we use client credentials?
        if CLIENT_SECRET:
            return self.login_with_client_credentials()

        return None

    def login_with_client_credentials(self) -> t.Optional[str]:
        self.session.fetch_token(
            TOKEN_URL,
            grant_type="client_credentials",
        )
        return self._create_token_info(self.session.token)["id_token"]

    def refresh_token(self) -> t.Optional[str]:
        # Can we use client credentials?
        if CLIENT_SECRET:
            return self.login_with_client_credentials()

        if not self.tokenInfo:
            self.console.print("Not currently authenticated", style="error")
            return None

        current_refresh_token = self.tokenInfo["refresh_token"]

        if not current_refresh_token:
            self.console.print("Refresh token not available", style="error")
            return None

        self.console.print(
            "[info]Refreshing your authentication token[/info] :arrows_counterclockwise:"
        )
        self.session.refresh_token(
            TOKEN_URL, refresh_token=current_refresh_token, scope=self.tokenInfo["scope"]
        )

        return self._create_token_info(self.session.token)["id_token"]

    def _create_token_info(self, token: t.Dict) -> t.Dict:
        self.tokenInfo = {
            "scope": token["scope"],
            "token_type": token["token_type"],
            "expires_at": token["expires_at"],
            "access_token": token["access_token"],
            "id_token": token["id_token"],
        }

        if "refresh_token" in token:
            self.tokenInfo["refresh_token"] = token["refresh_token"]

        SSOAuth._save_auth_yaml(self.tokenInfo)

        return self.tokenInfo


class SSORequestAuth(Auth):
    def __init__(self, id_token: str) -> None:
        self.id_token = id_token

    def auth_flow(self, request: Request) -> t.Generator[Request, Response, None]:
        request.headers["Authorization"] = f"Bearer {self.id_token}"
        yield request


UNAUTHENTICATED_MESSAGE = 'You are not authenticated. Please either specify a token in your project config, or run "tcloud auth login" if using Tobiko Cloud single sign on.'


class AuthHttpClient(PublicHttpClient):
    """
    This client retries on authentication failures using the TCloud token if available
    """

    def __init__(self, sso: t.Optional[SSOAuth] = None, *args: t.Any, **kwargs: t.Any):
        self.sso = sso or SSOAuth()
        super().__init__(*args, **kwargs)

    def _call(self, *args: t.Any, **kwargs: t.Any) -> Response:
        old_auth = self._client.auth
        has_auth = old_auth or ("headers" in kwargs and "Authorization" in kwargs["headers"])

        if CLIENT_SECRET or not has_auth:
            # Since we don't have a token configured, let's see if we already
            # have a token, if so use it
            id_token = self.sso.id_token()
            if id_token:
                self._client.auth = SSORequestAuth(id_token)

        try:
            response = super()._call(*args, **kwargs)
            if response.status_code == 401:
                response.raise_for_status()
            return response
        except HTTPStatusError as e:
            if e.response.status_code == 401:
                raise HTTPStatusError(
                    UNAUTHENTICATED_MESSAGE, request=e.request, response=e.response
                )
            raise e
        except self.error_class as e:
            if e.status_code == 401:
                raise self.error_class(UNAUTHENTICATED_MESSAGE, status_code=401)
            raise e
        finally:
            self._client.auth = old_auth
