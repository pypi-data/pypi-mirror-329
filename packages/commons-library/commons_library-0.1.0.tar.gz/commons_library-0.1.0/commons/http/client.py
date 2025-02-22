from typing import Optional

import httpx

from commons.media.images import Image


class GravatarClient:
    @staticmethod
    def fetch(email_hash: str, size: int) -> Optional[Image]:
        try:
            response = httpx.get(f'https://www.gravatar.com/avatar/{email_hash}?s={size}')

            if response and response.content:
                return Image(data=response.content).convert()
        except ConnectionError:
            # TODO: put warning here
            return None


class GiphyClient:
    @staticmethod
    def fetch(**kwargs) -> Optional[Image]:
        try:
            item_hash = kwargs['key']

            response = httpx.get(f"https://media.giphy.com/media/{item_hash}/giphy.gif")

            if response and response.content:
                return Image(data=response.content, media_type=response.headers['Content-Type'])
        except ConnectionError:
            # TODO: put a warning here
            return None


