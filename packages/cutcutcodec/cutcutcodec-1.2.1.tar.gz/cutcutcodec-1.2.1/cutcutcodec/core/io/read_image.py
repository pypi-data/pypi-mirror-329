#!/usr/bin/env python3

"""Read an image with opencv."""

from fractions import Fraction
import math
import pathlib
import typing

import cv2
import numpy as np
import torch

from cutcutcodec.core.classes.container import ContainerInput
from cutcutcodec.core.classes.frame_video import FrameVideo
from cutcutcodec.core.classes.stream import Stream
from cutcutcodec.core.classes.stream_video import StreamVideo
from cutcutcodec.core.exceptions import DecodeError, MissingStreamError, OutOfTimeRange
from cutcutcodec.core.filter.video.resize import resize_keep_ratio
from cutcutcodec.core.io.read_ffmpeg_color import ContainerInputFFMPEGColor


def _read_wand(filename: pathlib.Path) -> torch.Tensor:
    """Read the image with wand.

    Based on the system package ``libmagickwand-dev``.
    """
    from wand.image import Image  # pylint: disable=C0415
    from wand.exceptions import BaseError  # pylint: disable=C0415
    try:
        img_wand = Image(filename=filename)
    except BaseError as err:
        raise DecodeError("failed to decode with wand") from err
    img_wand.colorspace = "rgb"  # bgr not supported
    img_wand.alpha_channel = False
    img_rgb = np.asarray(img_wand)
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    return torch.from_numpy(img_bgr)


def _read_av(filename: pathlib.Path) -> torch.Tensor:
    """Read the image with the pyav module."""
    from cutcutcodec.core.analysis.stream.shape import optimal_shape_video  # pylint: disable=C0415
    streams = ContainerInputFFMPEGColor(filename).out_select("video")
    if not streams:
        raise DecodeError(f"no image stream found in {filename} with pyav")
    stream = streams[0]
    try:
        shape = optimal_shape_video(stream)
    except MissingStreamError as err:
        raise DecodeError(f"failed to decode video stream in {filename} with pyav") from err
    return stream.snapshot(0, shape)


def _read_cv2(filename: pathlib.Path) -> torch.Tensor:
    """Read the image with opencv."""
    try:
        if (img := cv2.imread(filename, cv2.IMREAD_UNCHANGED)) is None:
            raise DecodeError("failed to decode with cv2")
    except cv2.error as err:
        raise DecodeError("failed to decode with cv2") from err
    return torch.from_numpy(img)


def read_image(filename: typing.Union[str, bytes, pathlib.Path]) -> torch.Tensor:
    """Read the image and make it compatible with Video Frame.

    Parameters
    ----------
    filename : pathlike
        The pathlike of the image file.

    Returns
    -------
    image : torch.Tensor
        The image in float32 of shape (height, width, channels).

    Raises
    ------
    cutcutcodec.core.exceptions.DecodeError
        If it fails to read the image.

    Examples
    --------
    >>> from cutcutcodec.core.io.read_image import read_image
    >>> from cutcutcodec.utils import get_project_root
    >>> for file in sorted((get_project_root().parent / "media" / "image").glob("image.*")):
    ...     image = read_image(file)
    ...     print(f"{file.name}: {tuple(image.shape)}")
    ...
    image.avif: (64, 64, 3)
    image.bmp: (64, 64, 3)
    image.exr: (64, 64, 3)
    image.heic: (64, 64, 3)
    image.jp2: (64, 64, 3)
    image.jpg: (64, 64, 3)
    image.kra: (64, 64, 3)
    image.pbm: (64, 64, 1)
    image.pgm: (64, 64, 1)
    image.png: (64, 64, 3)
    image.pnm: (64, 64, 3)
    image.ppm: (64, 64, 3)
    image.psd: (64, 64, 3)
    image.ras: (64, 64, 3)
    image.sgi: (64, 64, 3)
    image.tiff: (64, 64, 3)
    image.webp: (64, 64, 3)
    image.xbm: (64, 64, 1)
    """
    filename = pathlib.Path(filename).expanduser().resolve()
    assert filename.is_file(), filename

    # try several decoders
    errs = []
    for decoder in (_read_av, _read_cv2, _read_wand):
        try:
            img = decoder(filename)
            break
        except DecodeError as err:
            errs.append(err)
    else:
        raise DecodeError(f"failed to decode the image {filename}", errs) from errs[0]

    # convert in float32
    if img.ndim == 2:
        img = img[:, :, None]
    if not torch.is_floating_point(img):
        iinfo = torch.iinfo(img.dtype)
        img = img.to(torch.float32)
        img -= float(iinfo.min)
        img *= 1.0 / float(iinfo.max - iinfo.min)
    elif img.dtype != torch.float32:
        img = img.to(torch.float32)

    return torch.asarray(img)


class ContainerInputImage(ContainerInput):
    """Decode an image.

    Attributes
    ----------
    filename : pathlib.Path
        The path to the physical file that contains the extracted image stream (readonly).

    Examples
    --------
    >>> from cutcutcodec.core.io.read_image import ContainerInputImage
    >>> from cutcutcodec.utils import get_project_root
    >>> (stream,) = ContainerInputImage(get_project_root() / "examples" / "logo.png").out_streams
    >>> stream.snapshot(0, (9, 9))[..., 3]
    tensor([[0.0000, 0.0415, 0.5152, 0.8748, 0.9872, 0.8744, 0.5164, 0.0422, 0.0000],
            [0.0418, 0.7853, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 0.7851, 0.0420],
            [0.5156, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 0.5141],
            [0.8749, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 0.8732],
            [0.9871, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 0.9861],
            [0.8745, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 0.8727],
            [0.5150, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 0.5137],
            [0.0417, 0.7838, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 0.7842, 0.0413],
            [0.0000, 0.0411, 0.5139, 0.8732, 0.9865, 0.8729, 0.5144, 0.0417, 0.0000]])
    >>>
    """

    def __init__(self, filename: typing.Union[str, bytes, pathlib.Path]):
        """Initialise and create the class.

        Parameters
        ----------
        filename : pathlike
            Path to the file to be decoded.

        Raises
        ------
        cutcutcodec.core.exceptions.DecodeError
            If it fail to extract any multimedia stream from the provided file.
        """
        filename = pathlib.Path(filename).expanduser().resolve()
        assert filename.is_file(), filename
        self._filename = filename
        super().__init__([_StreamVideoImage(self)])

    def __enter__(self):
        """Make the object compatible with a context manager."""
        return self

    def __exit__(self, *_):
        """Exit the context manager."""

    def _getstate(self) -> dict:
        return {"filename": str(self.filename)}

    def _setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        keys = {"filename"}
        assert state.keys() == keys, set(state)-keys
        ContainerInputImage.__init__(self, state["filename"])

    @property
    def filename(self) -> pathlib.Path:
        """Return the path to the physical file that contains the extracted image stream."""
        return self._filename


class _StreamVideoImage(StreamVideo):
    """Read an image as a video stream.

    Parameters
    ----------
    height : int
        The dimension i (vertical) of the encoded frames in pxl (readonly).
    width : int
        The dimension j (horizontal) of the encoded frames in pxl (readonly).
    """

    is_space_continuous = False
    is_time_continuous = False

    def __init__(self, node: ContainerInputImage):
        assert isinstance(node, ContainerInputImage), node.__class__.__name__
        super().__init__(node)
        self._img = read_image(node.filename)
        self._height, self._width, *_ = self._img.shape
        self._resized_img = FrameVideo(0, self._img)  # not from_numpy for casting shape and type

    def _snapshot(self, timestamp: Fraction, mask: torch.Tensor) -> torch.Tensor:
        if timestamp < 0:
            raise OutOfTimeRange(f"there is no image frame at timestamp {timestamp} (need >= 0)")

        # reshape if needed
        if self._resized_img.shape[:2] != mask.shape:
            self._resized_img = resize_keep_ratio(FrameVideo(0, self._img), mask.shape)

        return FrameVideo(timestamp, self._resized_img.clone())

    @property
    def beginning(self) -> Fraction:
        return Fraction(0)

    @property
    def duration(self) -> typing.Union[Fraction, float]:
        return math.inf

    @property
    def height(self) -> int:
        """Return the preconised dimension i (vertical) of the picture in pxl."""
        return self._height

    @property
    def width(self) -> int:
        """Return the preconised dimension j (horizontal) of the picture in pxl."""
        return self._width
