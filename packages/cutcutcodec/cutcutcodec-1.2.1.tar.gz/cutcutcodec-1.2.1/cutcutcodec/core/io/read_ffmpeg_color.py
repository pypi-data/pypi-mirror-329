#!/usr/bin/env python3

"""Delegate the reading to the module read_ffmpeg, and add a filter to manage the colorspace."""

import logging

import av

from cutcutcodec.config.config import Config
from cutcutcodec.core.colorspace.cst import FFMPEG_PRIMARIES, FFMPEG_TRC
from cutcutcodec.core.colorspace.func import guess_space
from cutcutcodec.core.filter.identity import FilterIdentity
from cutcutcodec.core.filter.video.colorspace import FilterVideoColorspace
from .pix_map import PIX_MAP
from .read_ffmpeg import ContainerInputFFMPEG, _StreamFFMPEGBase


class ContainerInputFFMPEGColor:
    """Same as ContainerInputFFMPEG with colorspace convertion.

    Examples
    --------
    >>> import torch
    >>> from cutcutcodec.core.analysis.stream.shape import optimal_shape_video
    >>> from cutcutcodec.core.io.read_ffmpeg_color import ContainerInputFFMPEGColor
    >>> container = ContainerInputFFMPEGColor("cutcutcodec/examples/intro.webm")
    >>> for stream in container.out_streams:
    ...     if stream.type == "video":
    ...         stream.snapshot(0, optimal_shape_video(stream)).shape
    ...     elif stream.type == "audio":
    ...         torch.round(stream.snapshot(0, rate=2, samples=3), decimals=5)
    ...
    (720, 1280, 3)
    (360, 640, 3)
    FrameAudio(0, 2, 'stereo', [[     nan,  0.1804 , -0.34765],
                                [     nan, -0.07236,  0.07893]])
    FrameAudio(0, 2, 'mono', [[     nan,  0.06998, -0.24758]])
    """

    def __new__(cls, *args, **kwargs):
        """Create a basic ContainerInputFFMPEG then convert the colorspace."""
        container = ContainerInputFFMPEG(*args, **kwargs)
        return cls.conv_colors(container.out_streams)

    @staticmethod
    def conv_colors(in_streams: tuple[_StreamFFMPEGBase]) -> FilterIdentity:
        """Apply the color convertion on the video streams."""
        assert all(isinstance(s, _StreamFFMPEGBase) for s in in_streams)
        streams = []
        for stream in in_streams:
            if stream.type == "video":
                # read input information
                stream_av = stream.av_container.streams[stream.index]
                pix = PIX_MAP[stream_av.codec_context.format.name]
                if "gray" in pix:
                    streams.append(stream)
                    continue
                primaries, transfer = guess_space(stream.height, stream.width)
                transfer = FFMPEG_TRC[stream_av.codec_context.color_trc] or transfer
                primaries = FFMPEG_PRIMARIES[stream_av.codec_context.color_primaries] or primaries
                logging.info("from %s to %s", stream_av.codec_context.format.name, pix)
                logging.info("primaries = %s", primaries)
                logging.info("transfer = %s", transfer)
                if "yuv" in pix:  # input space is Y'CbCr
                    src = f"y'pbpr_{transfer}_{primaries}"
                else:  # input space is gray' or r'g'b'
                    src = f"r'g'b'_{transfer}_{primaries}"
                dst = f"rgb_{Config().working_prim}"
                alpha = len(av.video.format.VideoFormat(pix).components) == 4
                streams.append(FilterVideoColorspace([stream], src, dst, alpha).out_streams[0])
            else:
                streams.append(stream)
        return FilterIdentity(streams)
