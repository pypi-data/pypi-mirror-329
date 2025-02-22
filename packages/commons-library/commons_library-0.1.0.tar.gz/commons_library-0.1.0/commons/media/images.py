from io import BytesIO
from pathlib import Path
from typing import Optional

from commons.http import Resource
from commons import media_type as mime_type


class Processor:
    def __init__(self, data: bytes):
        from PIL import Image

        self.data = data
        self.image = Image.open(BytesIO(data))  # Create an Image based on an in-memory image bytestream
        self.buffer = BytesIO()

    def compress(self):
        self.image.save(self.buffer, self.image.format, optimize=True, quality=9)

        return self

    def convert(self, to_type: str = mime_type.IMAGE_WEBP):
        _type = to_type

        match _type:
            case mime_type.IMAGE_WEBP:
                self.image.save(self.buffer, "WEBP")
            case mime_type.APPLICATION_PDF:
                import img2pdf
                self.buffer.write(img2pdf.convert(self.data))
            case _:
                raise ValueError(f'\'{to_type}')

        return self

    def get(self):
        self.buffer.seek(0)  # Move the bytestream pointer to the beginning

        return self.buffer.read()


class Image(Resource):
    alt: str = None
    width: int = None
    height: int = None
    _media_type: str = None
    _data: bytes = None

    def __init__(self, location: str | Path = 'memory',
                 alt: str = None,
                 width: int = None,
                 height: int = None,
                 data: bytes = None,
                 media_type: str = None):
        super().__init__(location)
        self.alt = alt
        self.width = width if (width and width > 0) else None
        self.height = height if (height and height > 0) else None
        self._data = data
        self._media_type = media_type

    def convert(self, to_type: str = mime_type.IMAGE_WEBP):
        return Image(data=Processor(self.read()).convert(to_type).get())

    @property
    def md5(self):
        from hashlib import md5
        return md5(str(self.read()).encode()).hexdigest()

    @property
    def media_type(self) -> str:
        """
        Loads an image and checks its format. Be careful on loading remote images
        """
        if self._media_type:
            return self._media_type
        else:
            import mimetypes
            if self.is_remote():
                self._media_type = mimetypes.guess_type(str(self.url))[0]
            elif self.is_local():
                self._media_type = mimetypes.guess_file_type(self.path)[0]

            return self._media_type

    def compress(self):
        return Image(data=Processor(self.read()).compress().get())

    def copy_to(self, destination: Path, optimize: bool = False, preserve_filename: bool = True) -> Path | None:
        """
        Copy an image to a destiny and optionally optimize by converting JPG and PNG to WEBP.
        """
        img: Optional[bytes] = None
        target: Optional[Path] = None

        if self.is_local() and destination and destination.exists():
            if optimize and (self.media_type == mime_type.IMAGE_JPEG or
                             self.media_type == mime_type.IMAGE_PNG):
                img = Processor(self.read()).convert().get()
            else:
                img = self.read()

            if preserve_filename:
                target = destination / str(self.filename)
            else:
                target = destination / self.md5

            if target:
                target.write_bytes(img)

                return target
