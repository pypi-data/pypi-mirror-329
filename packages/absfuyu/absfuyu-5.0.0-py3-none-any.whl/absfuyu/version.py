"""
Absfuyu: Version
----------------
Package versioning module

Version: 2.1.1
Date updated: 14/04/2024 (dd/mm/yyyy)
"""

__all__ = [
    # Options
    "ReleaseOption",
    "ReleaseLevel",
    # Class
    "Version",
    "Bumper",
    "PkgVersion",
]


import json
import re
import subprocess
from typing import List, Tuple, TypedDict, Union
from urllib.error import URLError
from urllib.request import Request, urlopen

from absfuyu.logger import logger


class ReleaseOption:
    """
    ``MAJOR``, ``MINOR``, ``PATCH``
    """

    MAJOR: str = "major"
    MINOR: str = "minor"
    PATCH: str = "patch"

    def all_option() -> List[str]:  # type: ignore
        """Return a list of release options"""
        return [__class__.MAJOR, __class__.MINOR, __class__.PATCH]  # type: ignore


class ReleaseLevel:
    """
    ``FINAL``, ``DEV``, ``RC``
    """

    FINAL: str = "final"
    DEV: str = "dev"
    RC: str = "rc"  # Release candidate

    def all_level() -> List[str]:  # type: ignore
        """Return a list of release levels"""
        return [__class__.FINAL, __class__.DEV, __class__.RC]  # type: ignore


class VersionDictFormat(TypedDict):
    """
    Format for the ``version`` section in ``config``

    :param major: Major changes
    :param minor: Minor changes
    :param patch: Patches and fixes
    :param release_level: Release level
    :param serial: Release serial
    """

    major: int
    minor: int
    patch: int
    release_level: str
    serial: int


class Version:
    """Version"""

    def __init__(
        self,
        major: Union[int, str],
        minor: Union[int, str],
        patch: Union[int, str],
        release_level: str = ReleaseLevel.FINAL,
        serial: Union[int, str] = 0,
    ) -> None:
        """
        Create ``Version`` instance

        :param major: Major change
        :type major: int | str
        :param minor: Minor change
        :type minor: int | str
        :param patch: Patch
        :type patch: int | str
        :param release_level: Release level: ``final``|``rc``|``dev``
        :type release_level: str
        :param serial: Serial for release level ``rc``|``dev``
        :type serial: int | str
        """
        self.major: int = major if isinstance(major, int) else int(major)
        self.minor: int = minor if isinstance(minor, int) else int(minor)
        self.patch: int = patch if isinstance(patch, int) else int(patch)
        self.release_level: str = release_level
        self.serial: int = serial if isinstance(serial, int) else int(serial)

    def __str__(self) -> str:
        return self.version

    def __repr__(self) -> str:
        if self.release_level.startswith(ReleaseLevel.FINAL):
            return f"{self.__class__.__name__}(major={self.major}, minor={self.minor}, patch={self.patch})"
        else:
            return (
                f"{self.__class__.__name__}("
                f"major={self.major}, minor={self.minor}, patch={self.patch}, "
                f"release_level={self.release_level}, serial={self.serial})"
            )

    def __format__(self, format_spec: str) -> str:
        """
        Change format of an object.
        Avaiable option: ``full``

        Usage
        -----
        >>> print(f"{<object>:<format_spec>}")
        >>> print(<object>.__format__(<format_spec>))
        >>> print(format(<object>, <format_spec>))

        Example:
        --------
        >>> test = Version(1, 0, 0)
        >>> print(f"{test:full}")
        1.0.0.final0
        """
        # Logic
        if format_spec.lower().startswith("full"):
            return f"{self.major}.{self.minor}.{self.patch}.{self.release_level}{self.serial}"

        # Else
        return self.__str__()

    @property
    def version(self) -> str:
        """
        Return version string

        Example:
        --------
        >>> test = Version(1, 0, 0)
        >>> test.version
        1.0.0
        >>> str(test) # test.__str__()
        1.0.0

        >>> test_serial = Version(1, 0, 0, "dev", 1)
        >>> test_serial.version
        1.0.0.dev1
        """
        if self.release_level.startswith(ReleaseLevel.FINAL):
            return f"{self.major}.{self.minor}.{self.patch}"
        else:
            return f"{self.major}.{self.minor}.{self.patch}.{self.release_level}{self.serial}"

    @classmethod
    def from_tuple(
        cls, iterable: Union[Tuple[int, int, int], Tuple[int, int, int, str, int]]
    ):
        """
        Convert to ``Version`` from a ``tuple``

        Parameters
        ----------
        iterable : tuple[int, int, int] | tuple[int, int, int, str, int]
            Version tuple in correct format

        Returns
        -------
        Version
            Version

        Raises
        ------
        ValueError
            Wrong tuple format


        Example:
        --------
        >>> test = Version.from_tuple((1, 0, 0))
        >>> test.version
        1.0.0
        """
        if len(iterable) == 5:
            return cls(
                iterable[0], iterable[1], iterable[2], iterable[3], iterable[4]
            )  # Full
        elif len(iterable) == 3:
            return cls(iterable[0], iterable[1], iterable[2])  # major.minor.patch only
        else:
            raise ValueError("iterable must have len of 5 or 3")

    @classmethod
    def from_str(cls, version_string: str):
        """
        Convert to ``Version`` from a ``str``

        Parameters
        ----------
        version_string : str
            | Version str in correct format
            | ``<major>.<minor>.<patch>``
            | ``<major>.<minor>.<patch>.<release level><serial>``

        Returns
        -------
        Version
            Version

        Raises
        ------
        ValueError
            Wrong version_string format


        Example:
        --------
        >>> test = Version.from_str("1.0.0")
        >>> test.version
        1.0.0
        """
        short_ver_pattern = re.compile(r"\b(\d)+\.(\d+)\.(\d+)\b")
        long_ver_pattern = re.compile(r"\b(\d)+\.(\d+)\.(\d+)\.(dev|rc|final)(\d+)\b")
        ver = version_string.lower().strip()

        long_ver = re.search(long_ver_pattern, ver)
        if long_ver:
            return cls.from_tuple(long_ver.groups())  # type: ignore

        short_ver = re.search(short_ver_pattern, ver)
        if short_ver:
            return cls.from_tuple(short_ver.groups())  # type: ignore

        raise ValueError("Wrong version_string format")

    def to_dict(self) -> VersionDictFormat:
        """
        Convert ``Version`` into ``dict``

        Returns
        -------
        VersionDictFormat
            Version dict


        Example:
        --------
        >>> test = Version(1, 0, 0)
        >>> test.to_dict()
        {
            "major": 1,
            "minor": 0,
            "patch": 0,
            "release_level": "final",
            "serial": 0
        }
        """
        out: VersionDictFormat = {
            "major": self.major,
            "minor": self.minor,
            "patch": self.patch,
            "release_level": self.release_level,
            "serial": self.serial,
        }
        return out


class Bumper(Version):
    """Version bumper"""

    def _bump_ver(self, release_option: str) -> None:
        """
        Bumping major, minor, patch
        """

        if release_option.startswith(ReleaseOption.MAJOR):
            self.major += 1
            self.minor = 0
            self.patch = 0
        elif release_option.startswith(ReleaseOption.MINOR):
            self.minor += 1
            self.patch = 0
        else:
            self.patch += 1

    def bump(
        self, *, option: str = ReleaseOption.PATCH, channel: str = ReleaseLevel.FINAL
    ) -> None:
        """
        Bump current version (internally)

        Parameters
        ----------
        option : str
            Release option
            (Default: ``"patch"``)

        channel : str
            Release channel
            (Default: ``"final"``)


        Example:
        --------
        >>> test = Bumper(1, 0, 0)
        >>> test.version
        1.0.0
        >>> test.bump()
        >>> test.version
        1.0.1
        """
        # Check conditions - use default values if fail
        if option not in ReleaseOption.all_option():
            logger.warning(f"Available option: {ReleaseOption.all_option()}")
            option = ReleaseOption.PATCH
        if channel not in ReleaseLevel.all_level():
            logger.warning(f"Available level: {ReleaseLevel.all_level()}")
            channel = ReleaseLevel.FINAL
        logger.debug(f"Target: {option} {channel}")

        # Bump ver
        if channel.startswith(ReleaseLevel.FINAL):  # Final release level
            if self.release_level in [
                ReleaseLevel.RC,
                ReleaseLevel.DEV,
            ]:  # current release channel is dev or rc
                self.release_level = ReleaseLevel.FINAL
                self.serial = 0
            else:
                self.serial = 0  # final channel does not need serial
                self._bump_ver(option)

        elif channel.startswith(ReleaseLevel.RC):  # release candidate release level
            if self.release_level.startswith(
                ReleaseLevel.DEV
            ):  # current release channel is dev
                self.release_level = ReleaseLevel.RC
                self.serial = 0  # reset serial
            elif channel == self.release_level:  # current release channel is rc
                self.serial += 1
            else:  # current release channel is final
                self.release_level = channel
                self.serial = 0  # reset serial
                self._bump_ver(option)

        else:  # dev release level
            if channel == self.release_level:  # current release channel is dev
                self.serial += 1
            else:  # current release channel is final or rc
                self.release_level = channel
                self.serial = 0
                self._bump_ver(option)


class PkgVersion:
    """
    Package Version
    """

    def __init__(self, package_name: str) -> None:
        self.package_name = package_name

    # Check for update
    @staticmethod
    def _fetch_data_from_server(link: str):
        """Fetch data from API"""
        req = Request(link)
        try:
            response = urlopen(req)
            # return response
        except URLError as e:
            if hasattr(e, "reason"):
                logger.error("Failed to reach server.")
                logger.error("Reason: ", e.reason)
            elif hasattr(e, "code"):
                logger.error("The server couldn't fulfill the request.")
                logger.error("Error code: ", e.code)
        except Exception:
            logger.error("Fetch failed!")
        else:
            return response.read().decode()

    def _get_latest_version_legacy(self) -> str:
        """
        Load data from PyPI's RSS -- OLD
        """
        rss = f"https://pypi.org/rss/project/{self.package_name}/releases.xml"
        xml_file: str = self._fetch_data_from_server(rss)
        ver = xml_file[
            xml_file.find("<item>") : xml_file.find(
                "</item>"
            )  # noqa: E203
        ]  # First item
        version = ver[
            ver.find("<title>") + len("<title>") : ver.find(
                "</title>"
            )  # noqa: E203
        ]
        return version

    def _load_data_from_json(self, json_link: str) -> dict:
        """
        Load data from api then convert to json
        """
        json_file: str = self._fetch_data_from_server(json_link)
        return json.loads(json_file)  # type: ignore

    def _get_latest_version(self) -> str:
        """
        Get latest version from PyPI's API
        """
        link = f"https://pypi.org/pypi/{self.package_name}/json"
        ver: str = self._load_data_from_json(link)["info"]["version"]
        logger.debug(f"Latest: {ver}")
        return ver

    def _get_update(self):
        """
        Run pip upgrade command
        """
        cmd = f"pip install -U {self.package_name}".split()
        return subprocess.run(cmd)

    def check_for_update(
        self,
        *,
        force_update: bool = False,
    ) -> None:
        """
        Check for latest update

        :param force_update: Auto update the package when run (Default: ``False``)
        :type force_update: bool
        """

        try:
            latest = self._get_latest_version()
        except Exception:
            latest = self._get_latest_version_legacy()

        try:
            import importlib

            _pk = importlib.__import__(self.package_name)
            current: str = _pk.__version__
        except Exception:
            current = ""

        logger.debug(f"Current: {current} | Lastest: {latest}")

        if current == latest:
            print(f"You are using the latest version ({latest})")
        else:
            if force_update:
                print(f"Newer version ({latest}) available. Upgrading...")
                try:
                    self._get_update()
                except Exception:
                    print(
                        f"""
                    Unable to perform update.
                    Please update manually with:
                    pip install -U {self.package_name}=={latest}
                    """
                    )
            else:
                print(
                    f"Newer version ({latest}) available. Upgrade with:\npip install -U {self.package_name}=={latest}"
                )
