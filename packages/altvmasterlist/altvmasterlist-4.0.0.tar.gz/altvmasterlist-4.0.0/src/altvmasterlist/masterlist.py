#!/usr/bin/env python3
from altvmasterlist import exceptions as error
from altvmasterlist import enum as enum
from urllib.parse import quote
from dataclasses import dataclass, field
from typing import Optional
from io import StringIO
from re import compile
from enum import Enum
import requests
import logging
import sys


"""You can find the masterlist api docs here: https://docs.altv.mp/articles/master_list_api.html"""
logger = logging.getLogger(__name__)
session = requests.session()


def request(url: str, server: any = None) -> dict | None:
    """This is the common request function to fetch remote data.

    Args:
        url (str): The Url to fetch.
        server (Server): An alt:V masterlist Server object.

    Returns:
        None: When an error occurred. But exceptions will still be logged!
        json: As data

    Raises:
        FetchError: there was an error while getting the data
    """
    # Use the User-Agent: AltPublicAgent, because some servers protect their CDN with
    # a simple User-Agent check e.g. https://luckyv.de did that before
    session.headers.clear()

    # if we get a request for a server that is not using
    # a cdn then set the same headers as the alt:V client while connecting
    # otherwise set a user-agent and Content-Type for the api
    if server and "http://" in url and not server.useCdn:
        session.headers = enum.RequestHeaders(server).to_dict()
    else:
        session.headers = {
            "User-Agent": enum.Extra.user_agent.value,
            "Content-Type": "application/json; charset=utf-8",
        }

    try:
        api_request = session.get(url, timeout=5)

        if not api_request.ok:
            raise error.FetchError(f"The request returned an error. {url}")
        else:
            return api_request.json()
    except Exception as e:
        logger.error(e)
        return None


@dataclass
class Server:
    playersCount: int = field(default=0, metadata={"description": "Current player count"})
    maxPlayersCount: int = field(default=0, metadata={"description": "Player limit"})
    passworded: bool = field(default=False, metadata={"description": "Password protected"})
    port: int = field(default=0, metadata={"description": "Server game port"})
    language: str = field(default="en", metadata={"description": "Two letter country code"})
    useEarlyAuth: bool = field(default=False, metadata={"description": "Server is using early auth (https://docs.altv.mp/articles/earlyauth.html)"})
    earlyAuthUrl: str = field(default="", metadata={"description": "Early auth URL (usually a login screen)"})
    useCdn: bool = field(default=False, metadata={"description": "Server is using a CDN (https://docs.altv.mp/articles/cdn.html)"})
    cdnUrl: str = field(default="", metadata={"description": "CDN URL"})
    useVoiceChat: bool = field(default=False, metadata={"description": "Server is using the built-in voice chat (https://docs.altv.mp/articles/voice.html)"})
    version: str = field(default="", metadata={"description": "Server version"})
    branch: str = field(default="", metadata={"description": "Server branch (release, rc, dev)"})
    available: bool = field(default=False, metadata={"description": "Server is online"})
    banned: bool = field(default=False)
    name: str = field(default="", metadata={"description": "Server name"})
    publicId: str = field(default=None, metadata={"description": "The server ID."})
    vanityUrl: str = field(default="")
    website: str = field(default="", metadata={"description": "Server website"})
    gameMode: str = field(default="", metadata={"description": "Gamemode provided by the server"})
    description: str = field(default="", metadata={"description": "Description provided by the server"})
    tags: str = field(default="", metadata={"description": "Tags provided by the server"})
    lastTimeUpdate: str = field(default="", metadata={"description": "Time string with format 2024-02-12T16:22:24.195392493Z"})
    verified: bool = field(default=False, metadata={"description": "alt:V verified server"})
    promoted: bool = field(default=False, metadata={"description": "Promoted server"})
    visible: bool = field(default=False, metadata={"description": "Visible in server list"})
    hasCustomSkin: bool = field(default=False, metadata={"description": "Defines if the server has a custom launcher skin"})
    bannerUrl: str = field(default="")
    address: str = field(default="", metadata={"description": "Connection address for the client, can be URL + port or IP + port"})
    group: Optional[enum.Group] = field(default=None, metadata={"description": "Server group info"})
    masterlist_icon_url: Optional[str] = field(default=None, metadata={"description": "Server icon shown on masterlist"})
    masterlist_banner_url: Optional[str] = field(default=None, metadata={"description": "Banner shown when you click on the server in the masterlist"})

    def __post_init__(self):
        self.fetch_data()

    def fetch_data(self):
        try:
            temp_data = request(enum.MasterlistUrls.specific_server.value.format(self.publicId))
        except error.FetchError as e:
            logger.error(f"there was an error fetching server data: {self.publicId} {e}")
            return

        if temp_data:
            for key, value in temp_data.items():
                if hasattr(self, key):
                    setattr(self, key, value)
            if "group" in temp_data and temp_data["group"]:
                self.group = enum.Group(**temp_data["group"])

    def __init__(self, server_id: str, no_fetch: bool = False) -> None:
        self.publicId = server_id
        if not no_fetch:
            self.fetch_data()

    def update(self) -> None:
        """Update the server data using the api."""
        self.__post_init__()

    def get_max(self, time: str = "1d") -> dict | None:
        """Maximum - Returns maximum data about the specified server (TIME = 1d, 7d, 31d)

        Args:
            time (str): The timerange of the data. Can be 1d, 7d, 31d.

        Returns:
            None: When an error occurs
            dict: The maximum player data

        Raises:
            FetchError: there was an error while getting the data
            NoPublicID: the server has no publicID
        """
        if not self.publicId:
            logger.warning("server got no masterlist publicID")
            raise error.NoPublicID(f"The server got no publicID")
        else:
            try:
                tmp_data = request(enum.MasterlistUrls.specific_server_maximum.value.format(self.publicId, time))
                return tmp_data
            except error.FetchError as e:
                logger.error(f"there was an error while getting max stats: {e}")
                raise error.FetchError(f"there was an error while getting max stats: {e}")

    def get_avg(
        self, time: str = "1d", return_result: bool = False
    ) -> dict | int | None:
        """Averages - Returns averages data about the specified server (TIME = 1d, 7d, 31d)

        Args:
            time (str): The timerange of the data. Can be 1d, 7d, 31d.
            return_result (bool): Define if you want the overall average.

        Returns:
            None: When an error occurs
            dict: The maximum player data
            int: Overall average of defined timerange

        Raises:
            FetchError: there was an error while getting the data
            NoPublicID: the server has no publicID
        """
        if not self.publicId:
            logger.warning("server got not masterlist publicID")
            raise error.NoPublicID(f"The server got no publicID")
        else:
            average_data = request(
                enum.MasterlistUrls.specific_server_average.value.format(self.publicId, time)
            )

            if not average_data:
                raise error.FetchError(f"There was an error while fetching data for {self.publicId} {time} {return_result}")

            if return_result:
                players_all = 0
                for entry in average_data:
                    players_all = players_all + entry["c"]
                result = players_all / len(average_data)
                return round(result)
            else:
                return average_data

    @property
    def connect_json(self) -> dict | None:
        """This function fetched the connect.json of an alt:V server.

        Returns:
            None: When an error occurred. But exceptions will still be logged!
            dict: The connect.json

        Raises:
            FetchError: there was an error while getting the data
        """
        if not self.available or self.passworded:
            raise error.FetchError(f"{self.publicId} is offline or password protected.")

        if self.publicId:
            if not self.useCdn:
                # server is on masterlist but not using a cdn
                cdn_request = request(f"http://{self.address}/connect.json", self)
            else:
                # server is on masterlist and using a cdn
                match self.cdnUrl:
                    case _ if ":80" in self.cdnUrl:
                        cdn_request = request(
                            f"http://{self.cdnUrl.replace(':80', '')}/connect.json", self
                        )
                    case _ if ":443" in self.cdnUrl:
                        cdn_request = request(
                            f"https://{self.cdnUrl.replace(':443', '')}/connect.json", self
                        )
                    case _:
                        cdn_request = request(f"{self.cdnUrl}/connect.json", self)
        else:
            # server is not on masterlist
            logger.info("getting connect.json by ip")
            cdn_request = request(f"{self.address}:{self.port}/connect.json", self)

        if cdn_request is None:
            raise error.FetchError(f"There was an error while fetching connect.json for {self.publicId}")
        else:
            return cdn_request

    @property
    def permissions(self) -> enum.Permissions | None:
        """This function returns the Permissions defined by the server. https://docs.altv.mp/articles/permissions.html

        Returns:
            None: When an error occurred. But exceptions will still be logged!
            Permissions: The permissions of the server.

        Raises:
            FetchError: there was an error while getting the data
        """

        class Permission(Enum):
            screen_capture = "Screen Capture"
            webrtc = "WebRTC"
            clipboard_access = "Clipboard Access"
            optional = "optional-permissions"
            required = "required-permissions"

        try:
            connect_json = self.connect_json
        except error.FetchError as e:
            logger.error(e)
            raise error.FetchError(f"couln't get permissions {e} ")

        optional = connect_json[Permission.optional.value]
        required = connect_json[Permission.required.value]

        permissions = enum.Permissions()

        # Define a list of permission attributes to check
        permission_keys = [
            "screen_capture",
            "webrtc",
            "clipboard_access"
        ]

        # Assign values for optional permissions
        for key in permission_keys:
            if key in optional:
                setattr(permissions.Optional, key, optional[key])
            if key in required:
                setattr(permissions.Required, key, required[key])

        return permissions

    def get_dtc_url(self, password=None) -> str | None:
        """This function gets the direct connect protocol url of an alt:V Server.
        (https://docs.altv.mp/articles/connectprotocol.html)

        Args:
            password (str): The password of the server.

        Returns:
            None: When an error occurred. But exceptions will still be logged!
            str: The direct connect protocol url.
        """
        with StringIO() as dtc_url:
            if self.useCdn:
                tmp_url = quote(self.cdnUrl, safe='')
                if "http" not in self.cdnUrl:
                    dtc_url.write(f"altv://connect/http://{tmp_url}")
                else:
                    dtc_url.write(f"altv://connect/{tmp_url}")
            else:
                dtc_url.write(f"altv://connect/{quote(self.address, safe='')}")

            if self.passworded and password is None:
                logger.warning(
                    "Your server is password protected but you did not supply a password for the Direct Connect Url."
                )
            if password is not None:
                dtc_url.write(f"?password={quote(password, safe='')}")

            return dtc_url.getvalue()


def get_server_stats() -> dict | None:
    """Statistics - Player Count across all servers & The amount of servers online

    Returns:
        None: When an error occurs
        dict: The stats

    Raises:
        FetchError: there was an error while getting the data
    """
    try:
        tmp_data = request(enum.MasterlistUrls.all_server_stats.value)
        return tmp_data
    except error.FetchError as e:
        logger.error(f"error while getting server stats: {e}")
        raise error.FetchError(f"error while getting server stats: {e}")


def get_servers() -> list[Server] | None:
    """Generates a list of all servers that are currently online.
    Note that the server objects returned are not complete!

    Returns:
        None: When an error occurs
        list: List object that contains all servers.

    Raises:
        FetchError: there was an error while getting the data
    """
    return_servers = []
    try:
        servers = request(enum.MasterlistUrls.all_servers.value)
    except error.FetchError as e:
        raise error.FetchError(f"failed to get servers: {e}")

    server_attributes = [
        "playersCount", "maxPlayersCount", "passworded", "language",
        "useEarlyAuth", "earlyAuthUrl", "useCdn", "cdnUrl", "useVoiceChat",
        "version", "branch", "available", "banned", "name", "publicId",
        "vanityUrl", "website", "gameMode", "description", "tags",
        "lastTimeUpdate", "verified", "promoted", "visible", "hasCustomSkin",
        "bannerUrl", "address", "group", "masterlist_icon_url",
        "masterlist_banner_url"
    ]

    for server in servers:
        tmp_server = Server(server["publicId"], no_fetch=True)
        for attr in server_attributes:
            setattr(tmp_server, attr, server[attr])
        return_servers.append(tmp_server)

    return return_servers


def validate_id(server_id: any) -> bool:
    """Validate a server id

    Args:
        server_id (any): The id you want to check.

    Returns:
        bool: True = valid, False = invalid
    """
    regex = compile(r"^[\da-zA-Z]{7}$")
    return isinstance(server_id, str) and regex.match(server_id) is not None


if __name__ == "__main__":
    print("This is a Module!")
    sys.exit()
