from pathlib import Path
from typing import Optional

from httpx import URL, get


class Resource:
    """
    Represents a resource that can be either a local file as well as a remote data.
    """
    # todo: improve this implementation
    url: URL
    path: Optional[Path] = None
    _data: Optional[bytes] = None

    def __init__(self, location: str | Path = 'memory', data: bytes = None):
        location = str(location).strip()

        self.url: URL = URL(location)
        self.path = Path(location)
        self._data = data

    def is_remote(self) -> bool:
        """
        Check whether a location is remote or local
        """
        return not self.url.scheme == 'memory' and self.url.is_absolute_url

    def is_local(self) -> bool:
        return self.url.scheme == 'memory' or self.url.is_relative_url

    def exists(self) -> bool:
        if self.is_local():
            return self.path.exists()
        elif self.is_remote():
            return bool(self.read())
        else:
            return bool(self._data)

    def scheme(self) -> str:
        return self.url.scheme

    def filename(self) -> Optional[str]:
        return self.path.name

    def read(self) -> Optional[bytes]:
        """
        Read content from a resource.

        Be aware that might be unsafe to read remote content that you might not trust.
        """
        data: Optional[bytes] = None

        if not self._data:
            try:
                if self.is_remote():
                    response = get(self.url, headers={
                        'Accept-Encoding': 'utf-8'
                    })

                    if response:
                        self._data = response.read()
                elif self.exists():
                    self._data = self.path.read_bytes()
            except FileNotFoundError:
                pass

        return self._data
