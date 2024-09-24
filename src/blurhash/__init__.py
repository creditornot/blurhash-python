from enum import Enum

from PIL import Image

from ._functions import ffi as _ffi, lib as _lib
from ._version import version as __version__


__all__ = ('encode', 'decode', 'is_valid_blurhash', 'PixelMode',
           'BlurhashDecodeError', '__version__')


class PixelMode(Enum):
    RGB = 3
    RGBA = 4


class BlurhashDecodeError(Exception):

    def __init__(self, blurhash):
        self.blurhash = blurhash

    def __str__(self):
        return "Failed to decode blurhash {}".format(self.blurhash)


def encode(image, x_components, y_components):
    if not isinstance(image, Image.Image):
        image = Image.open(image)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    rgb_data = image.tobytes()
    width, height = image.size
    image.close()

    rgb = _ffi.new('uint8_t[]', rgb_data)
    bytes_per_row = _ffi.cast('size_t', width * 3)
    width = _ffi.cast('int', width)
    height = _ffi.cast('int', height)
    x_components = _ffi.cast('int', x_components)
    y_components = _ffi.cast('int', y_components)
    destination = _ffi.new("char[]", 2 + 4 + (9 * 9 - 1) * 2 + 1)

    result = _lib.create_hash_from_pixels(
        x_components,
        y_components,
        width,
        height,
        rgb,
        bytes_per_row,
        destination,
    )

    if result == _ffi.NULL:
        raise ValueError('Invalid x_components or y_components')

    return _ffi.string(result).decode()


def decode(blurhash, width, height, punch=1, mode=PixelMode.RGB):

    if width <= 0 or type(width) != int:
        raise ValueError(
          "Argument width={} is not a valid positive integer"
          " (must be > 0).".format(width)
        )

    if height <= 0 or type(height) != int:
        raise ValueError(
          "Argument height={} is not a valid positive integer"
          " (must be > 0).".format(height)
        )

    if punch < 1 or type(punch) != int:
        raise ValueError(
          "Argument punch={} is not a valid positive integer"
          " (must be >= 1).".format(punch)
        )

    if not isinstance(mode, PixelMode):
        raise ValueError(
          "Argument 'mode' must be of type {}"
          " but got {}".format(PixelMode, type(mode))
        )

    channels = mode.value
    blurhash_str = _ffi.new('char[]', bytes(blurhash, "utf-8"))

    if not _lib.is_valid_blurhash(blurhash_str):
        raise ValueError("{} is not a valid blurhash".format(blurhash))

    width_int = _ffi.cast('int', width)
    height_int = _ffi.cast('int', height)
    punch_int = _ffi.cast('int', punch)
    channels_int = _ffi.cast('int', channels)

    pixel_array = _ffi.new('uint8_t[]', width * height * channels)

    result = _lib.create_pixels_from_blurhash(blurhash_str,
                                              width_int, height_int,
                                              punch_int, channels_int,
                                              pixel_array)

    if result == -1:
        raise BlurhashDecodeError(blurhash)

    pixels_buffer = _ffi.buffer(pixel_array, width * height * channels)
    image = Image.frombuffer(mode.name, (width, height), pixels_buffer)

    return image


def is_valid_blurhash(blurhash):

    blurhash_str = _ffi.new('char[]', bytes(blurhash, 'utf-8'))
    return bool(_lib.is_valid_blurhash(blurhash_str))
