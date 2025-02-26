#!/usr/bin/env python3

"""Manage the input/output layer."""

import logging
import pathlib
import typing

from cutcutcodec.core.exceptions import DecodeError
from cutcutcodec.core.classes.node import Node
from .read_ffmpeg_color import ContainerInputFFMPEGColor
from .read_image import ContainerInputImage
from .read_svg import ContainerInputSVG
from .write_ffmpeg import ContainerOutputFFMPEG


IMAGE_SUFFIXES = {
    ".avif",
    ".bmp", ".dib",
    ".exr",
    ".hdr", ".pic",
    ".heic",
    ".jp2", ".jpg2", ".jpeg2000", ".jpg2000",
    ".jpeg", ".jpg", ".jpe",
    ".kra",
    ".pbm", ".pgm", ".ppm", ".pxm", ".pnm",
    ".pfm",
    ".png",
    ".psd",
    ".sgi",
    ".sr",  ".ras",
    ".tif", ".tiff",
    ".webp",
    ".xbm",
}
VIDEO_SUFFIXES = {
    ".avi", ".gif", ".m2ts", ".mkv", ".mp4", ".ogv", ".vob", ".webm"
}


__all__ = ["read", "IMAGE_SUFFIXES", "VIDEO_SUFFIXES"]


def read(filename: typing.Union[str, bytes, pathlib.Path], **kwargs) -> Node:
    """Open the media file with the appropriate reader.

    Parameters
    ----------
    filename : pathlike
        The path to the file to be decoded.
    **kwargs : dict
        Transmitted to ``cutcutcodec.core.io.read_ffmpeg.ContainerInputFFMPEGColor``
        or ``cutcutcodec.core.io.read_image.ContainerInputImage``
        or ``cutcutcodec.core.io.read_svg.ContainerInputSVG``.

    Returns
    -------
    container : cutcutcodec.core.classes.container.ContainerInput
        The appropriated instanciated container, according to the nature of the file.

    Raises
    ------
    cutcutcodec.core.exceptions.DecodeError
        If the file can not be decoded by any reader.
    """
    extension = pathlib.Path(filename).suffix.lower()

    # simple case where extension is knowned
    if extension in VIDEO_SUFFIXES:
        return ContainerInputFFMPEGColor(filename, **kwargs)
    if extension in IMAGE_SUFFIXES:
        return ContainerInputImage(filename, **kwargs)
    if extension in {".svg"}:
        return ContainerInputSVG(filename, **kwargs)

    # case we have to try
    logging.warning("unknowned extension %s, try several readers", extension)
    try:
        return ContainerInputSVG(filename, **kwargs)
    except DecodeError:
        try:
            return ContainerInputImage(filename, **kwargs)
        except DecodeError:
            return ContainerInputFFMPEGColor(filename, **kwargs)


def write(*args, **kwargs):
    """Alias to ``cutcutcodec.core.io.write_ffmpeg.ContainerOutputFFMPEG``."""
    # conv = (
    #     convert(
    #         f"r'g'b'_{Config().working_prim}"
    #         f"r'g'b'_{Config().target_trc}_{Config().target_prim}",
    #     )
    #     [::-1]  # rgb to bgr
    #     .subs(zip(SYMBS["r'g'b'"], ("b0", "g0", "r0")), simultaneous=True)
    # )
    ContainerOutputFFMPEG(*args, **kwargs).write()
