#!/usr/bin/env python3

"""Resize an image."""

from fractions import Fraction
import numbers
import typing

import cv2
import numpy as np
import torch

from cutcutcodec.core.classes.filter import Filter
from cutcutcodec.core.classes.frame_video import FrameVideo
from cutcutcodec.core.classes.stream import Stream
from cutcutcodec.core.classes.stream_video import StreamVideoWrapper
from .pad import pad_keep_ratio


def _resize(image: np.ndarray, shape: tuple[int, int], copy: bool) -> np.ndarray:
    """Help ``resize``.

    Notes
    -----
    * No verifications are performed for performance reason.
    * The output tensor can be a reference to the provided tensor if copy is False.
    """
    if image.shape[:2] == shape:  # optional optimization
        return image.copy() if copy else image
    height, width = shape
    enlarge = height >= image.shape[0] or width >= image.shape[1]
    image = np.ascontiguousarray(image)  # cv2 needs it
    image = cv2.resize(  # 10 times faster than torchvision.transforms.v2.functional.resize
        image,
        dsize=(width, height),
        interpolation=(cv2.INTER_CUBIC if enlarge else cv2.INTER_AREA),  # for antialiasing
    )
    if enlarge and np.issubdtype(image.dtype, np.floating):
        image = np.clip(image, 0.0, 1.0, out=image)
    return image


def resize(
    image: typing.Union[FrameVideo, torch.Tensor, np.ndarray],
    shape: typing.Union[tuple[numbers.Integral, numbers.Integral], list[numbers.Integral]],
    copy: bool = True,
) -> typing.Union[FrameVideo, torch.Tensor, np.ndarray]:
    """Reshape the image, can introduce a deformation.

    Parameters
    ----------
    image : cutcutcodec.core.classes.image_video.FrameVideo or torch.Tensor or numpy.ndarray
        The image to be resized, of shape (height, width, channels).
        It has to match with the video image specifications.
    shape : int and int
        The pixel dimensions of the returned image.
        The convention adopted is the numpy convention (height, width).
    copy : boolean, default=True
        If True, ensure that the returned tensor doesn't share the data of the input tensor.

    Returns
    -------
    resized_image
        The resized image homogeneous with the input.
        The underground data are not shared with the input. A safe copy is done.

    Examples
    --------
    >>> import torch
    >>> from cutcutcodec.core.classes.frame_video import FrameVideo
    >>> from cutcutcodec.core.filter.video.resize import resize
    >>> ref = FrameVideo(0, torch.empty(480, 720, 3))
    >>> resize(ref, (720, 1080)).shape  # upscaling
    (720, 1080, 3)
    >>> resize(ref, (480, 360)).shape  # downscaling
    (480, 360, 3)
    >>>
    """
    # case cast homogeneous
    if isinstance(image, FrameVideo):
        return FrameVideo(image.time, resize(torch.Tensor(image), shape, copy=copy))
    if isinstance(image, torch.Tensor):
        return torch.as_tensor(
            resize(image.numpy(force=True), shape, copy=copy), device=image.device
        )

    # verif case np.ndarray
    assert isinstance(image, np.ndarray), image.__class__.__name__
    assert image.ndim == 3, image.shape
    assert image.shape[0] >= 1, image.shape
    assert image.shape[1] >= 1, image.shape
    assert image.shape[2] in {1, 2, 3, 4}, image.shape
    assert image.dtype.type in {np.uint8, np.float32}
    assert isinstance(shape, (tuple, list)), shape.__class__.__name__
    assert len(shape) == 2, len(shape)
    assert all(isinstance(s, numbers.Integral) and s >= 1 for s in shape), shape
    shape = (int(shape[0]), int(shape[1]))
    assert isinstance(copy, bool), copy.__class__.__name__

    # resize
    return _resize(image, shape, copy=copy)


def resize_keep_ratio(
    image: typing.Union[FrameVideo, torch.Tensor, np.ndarray],
    shape: typing.Union[tuple[numbers.Integral, numbers.Integral], list[numbers.Integral]],
    copy: bool = True,
) -> typing.Union[FrameVideo, torch.Tensor, np.ndarray]:
    """Reshape the image, keep the spact ratio and pad with transparent pixels.

    Parameters
    ----------
    image : cutcutcodec.core.classes.image_video.FrameVideo or torch.Tensor or numpy.ndarray
        Transmitted to ``cutcutcodec.core.filter.video.resize.resize``.
    shape : int and int
        Transmitted to ``cutcutcodec.core.filter.video.resize.resize``.
    copy : boolean, default=True
        Transmitted to ``cutcutcodec.core.filter.video.resize.resize``.

    Returns
    -------
    resized_image
        The resized (and padded) image homogeneous with the input.
        The underground data are not shared with the input. A safe copy is done.

    Examples
    --------
    >>> import torch
    >>> from cutcutcodec.core.classes.frame_video import FrameVideo
    >>> from cutcutcodec.core.filter.video.resize import resize_keep_ratio
    >>> ref = FrameVideo(0, torch.full((4, 8, 1), 0.5))
    >>>
    >>> # upscale
    >>> resize_keep_ratio(ref, (8, 9))[..., 1]  # alpha layer
    tensor([[0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [1., 1., 1., 1., 1., 1., 1., 1., 1.],
            [1., 1., 1., 1., 1., 1., 1., 1., 1.],
            [1., 1., 1., 1., 1., 1., 1., 1., 1.],
            [1., 1., 1., 1., 1., 1., 1., 1., 1.],
            [0., 0., 0., 0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0., 0., 0., 0.]])
    >>> resize_keep_ratio(ref, (8, 9)).convert(1)[..., 0]  # as gray
    tensor([[0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
            [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
            [0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000],
            [0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000],
            [0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000],
            [0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000],
            [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
            [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000]])
    >>>
    >>> # downscale
    >>> resize_keep_ratio(ref, (4, 4))[..., 1]  # alpha layer
    tensor([[0., 0., 0., 0.],
            [1., 1., 1., 1.],
            [1., 1., 1., 1.],
            [0., 0., 0., 0.]])
    >>> resize_keep_ratio(ref, (4, 4)).convert(1)[..., 0]  # as gray
    tensor([[0.0000, 0.0000, 0.0000, 0.0000],
            [0.5000, 0.5000, 0.5000, 0.5000],
            [0.5000, 0.5000, 0.5000, 0.5000],
            [0.0000, 0.0000, 0.0000, 0.0000]])
    >>>
    >>> # mix
    >>> resize_keep_ratio(ref, (6, 6))[..., 1]  # alpha layer
    tensor([[0., 0., 0., 0., 0., 0.],
            [1., 1., 1., 1., 1., 1.],
            [1., 1., 1., 1., 1., 1.],
            [1., 1., 1., 1., 1., 1.],
            [0., 0., 0., 0., 0., 0.],
            [0., 0., 0., 0., 0., 0.]])
    >>> resize_keep_ratio(ref, (6, 6)).convert(1)[..., 0]  # as gray
    tensor([[0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
            [0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000],
            [0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000],
            [0.5000, 0.5000, 0.5000, 0.5000, 0.5000, 0.5000],
            [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
            [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000]])
    >>>
    """
    # minimalist verifications
    assert isinstance(image, (FrameVideo, torch.Tensor, np.ndarray)), image.__class__.__name__
    assert image.ndim >= 2, image.shape
    assert image.shape[0] >= 1, image.shape
    assert image.shape[1] >= 1, image.shape
    assert isinstance(shape, (tuple, list)), shape.__class__.__name__
    assert len(shape) == 2, len(shape)
    assert all(isinstance(s, numbers.Integral) and s >= 1 for s in shape), shape

    # find the shape for keeping proportion
    dw_sh, dh_sw = shape[1]*image.shape[0], shape[0]*image.shape[1]
    if dw_sh < dh_sw:  # need vertical padding
        height, width = (round(dw_sh/image.shape[1]), shape[1])  # keep width unchanged
    elif dw_sh > dh_sw:  # need horizontal padding
        height, width = (shape[0], round(dh_sw/image.shape[0]))  # keep height unchanged
    else:  # if the proportion is the same
        return resize(image, shape, copy=copy)

    # resize and pad
    image = resize(image, (height, width), copy=copy)
    image = pad_keep_ratio(image, shape, copy=False)
    return image


class FilterVideoResize(Filter):
    """Frozen the shape of the input stream.

    Attributes
    ----------
    keep_ratio : boolean
        True if the aspect ratio is keep, False otherwise (readonly).
    shape : tuple[int, int]
        The pixel dimensions of the incoming frames (readonly).
        The convention adopted is the numpy convention (height, width).

    Examples
    --------
    >>> from cutcutcodec.core.generation.video.noise import GeneratorVideoNoise
    >>> from cutcutcodec.core.filter.video.resize import FilterVideoResize
    >>> (stream_in,) = GeneratorVideoNoise(0).out_streams
    >>>
    >>> # keep ratio
    >>> (stream_out,) = FilterVideoResize([stream_in], (4, 6), keep_ratio=True).out_streams
    >>> stream_out.snapshot(0, (8, 9)).convert(1)[..., 0]
    tensor([[0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
            [0.5824, 0.4850, 0.4080, 0.4435, 0.4082, 0.3316, 0.1949, 0.1162, 0.1010],
            [0.5159, 0.6177, 0.6451, 0.4976, 0.4357, 0.4693, 0.5354, 0.4819, 0.4018],
            [0.5097, 0.6685, 0.7636, 0.6089, 0.5496, 0.6249, 0.7717, 0.7542, 0.6719],
            [0.5771, 0.4820, 0.4956, 0.7424, 0.7381, 0.5821, 0.4989, 0.4615, 0.4656],
            [0.6798, 0.3974, 0.1954, 0.4461, 0.6377, 0.5819, 0.2722, 0.4009, 0.6595],
            [0.7855, 0.3979, 0.0538, 0.1131, 0.4572, 0.5968, 0.1714, 0.4655, 0.9226],
            [0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000]])
    >>> stream_out.snapshot(0, (4, 3)).convert(1)[..., 0]
    tensor([[0.0000, 0.0000, 0.0000],
            [0.5843, 0.4749, 0.4459],
            [0.4446, 0.5585, 0.4656],
            [0.0000, 0.0000, 0.0000]])
    >>> stream_out.snapshot(0, (6, 5)).convert(1)[..., 0]
    tensor([[0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
            [0.5525, 0.5121, 0.4382, 0.3709, 0.2706],
            [0.5619, 0.6026, 0.6194, 0.5938, 0.5695],
            [0.6026, 0.2289, 0.4924, 0.3640, 0.6547],
            [0.0000, 0.0000, 0.0000, 0.0000, 0.0000],
            [0.0000, 0.0000, 0.0000, 0.0000, 0.0000]])
    >>>
    >>> # deformation
    >>> (stream_out,) = FilterVideoResize([stream_in], (4, 6), keep_ratio=False).out_streams
    >>> stream_out.snapshot(0, (8, 9))[..., 0]
    tensor([[0.5249, 0.2219, 0.1432, 0.6494, 0.9650, 0.8563, 0.4235, 0.5095, 0.7819],
            [0.5466, 0.3829, 0.3196, 0.5422, 0.8268, 0.8783, 0.5912, 0.5052, 0.5478],
            [0.5869, 0.6509, 0.6105, 0.3653, 0.5991, 0.9156, 0.8694, 0.4953, 0.1543],
            [0.4496, 0.7269, 0.7851, 0.2679, 0.4595, 0.9105, 0.9867, 0.5825, 0.1567],
            [0.1976, 0.5635, 0.7489, 0.3050, 0.4868, 0.8683, 0.8806, 0.7199, 0.5543],
            [0.3183, 0.5522, 0.6515, 0.3231, 0.4995, 0.8010, 0.7522, 0.7571, 0.7768],
            [0.7429, 0.6901, 0.5374, 0.3183, 0.4986, 0.7456, 0.6644, 0.6728, 0.7112],
            [0.9979, 0.7723, 0.4679, 0.3156, 0.4980, 0.7114, 0.6099, 0.6234, 0.6762]])
    >>> stream_out.snapshot(0, (4, 3))[..., 0]
    tensor([[0.2707, 0.9211, 0.5108],
            [0.7336, 0.5043, 0.5231],
            [0.5234, 0.5003, 0.7601],
            [0.7485, 0.4983, 0.6364]])
    >>> stream_out.snapshot(0, (6, 5))[..., 0]
    tensor([[0.4540, 0.2289, 0.9573, 0.5031, 0.7061],
            [0.5602, 0.4533, 0.7130, 0.7831, 0.3862],
            [0.5510, 0.6799, 0.4676, 1.0000, 0.2411],
            [0.2747, 0.6644, 0.4939, 0.8722, 0.6517],
            [0.5425, 0.5388, 0.4989, 0.7224, 0.7488],
            [0.9176, 0.4212, 0.4981, 0.6359, 0.6641]])
    >>>
    """

    def __init__(
        self,
        in_streams: typing.Iterable[Stream],
        shape: typing.Union[tuple[numbers.Integral, numbers.Integral], list[numbers.Integral]],
        keep_ratio: bool = False,
    ):
        """Initialise and create the class.

        Parameters
        ----------
        in_streams : typing.Iterable[Stream]
            Transmitted to ``cutcutcodec.core.classes.filter.Filter``.
        shape : tuple[int, int]
            The pixel dimensions of the incoming frames.
            The convention adopted is the numpy convention (height, width).
        keep_ratio : boolean, default=False
            If True, the returned frame is padded to keep the proportion of the incoming frame.
        """
        assert isinstance(shape, (tuple, list)), shape.__class__.__name__
        assert len(shape) == 2, len(shape)
        assert all(isinstance(s, numbers.Integral) and s >= 1 for s in shape), shape
        assert isinstance(keep_ratio, bool), keep_ratio.__class__.__name__
        self._shape = (int(shape[0]), int(shape[1]))
        self._keep_ratio = keep_ratio

        super().__init__(in_streams, in_streams)
        super().__init__(
            in_streams, [_StreamVideoResize(self, index) for index in range(len(in_streams))]
        )

    def _getstate(self) -> dict:
        return {
            "keep_ratio": self.keep_ratio,
            "shape": list(self.shape),
        }

    def _setstate(self, in_streams: typing.Iterable[Stream], state: dict) -> None:
        assert state.keys() == {"keep_ratio", "shape"}, set(state)
        FilterVideoResize.__init__(self, in_streams, state["shape"], keep_ratio=state["keep_ratio"])

    @property
    def keep_ratio(self) -> bool:
        """Return True if the aspect ratio is keep, False otherwise."""
        return self._keep_ratio

    @property
    def shape(self) -> tuple[int, int]:
        """Return The pixel dimensions of the incoming frames."""
        return self._shape


class _StreamVideoResize(StreamVideoWrapper):
    """Translate a video stream from a certain delay."""

    def _snapshot(self, timestamp: Fraction, mask: torch.Tensor) -> torch.Tensor:
        in_mask = torch.full(self.node.shape, True, dtype=bool)
        src = self.stream._snapshot(timestamp, in_mask)  # pylint: disable=W0212
        dst = (
            resize_keep_ratio(src, mask.shape)
            if self.node.keep_ratio else
            resize(src, mask.shape)
        )
        return dst
