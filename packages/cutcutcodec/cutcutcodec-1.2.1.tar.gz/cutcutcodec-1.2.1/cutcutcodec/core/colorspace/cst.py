#!/usr/bin/env python3

"""Regroup all standard color space constants.

The ffmpeg constants are defined on the
`ffmpeg colorspace website <https://trac.ffmpeg.org/wiki/colorspace>`_,
or are described somewhere in ``ffmpeg -h full``.

The tristimulus and transfer functions are taken from the
`International Telecomunication Union Recomandation ITU-T H.273 (V4)`.
"""

import sympy

SYMBS = {
    "y'pbpr": sympy.symbols("y' p_b p_r", real=True),
    "r'g'b'": sympy.symbols("r' g' b'", real=True),
    "rgb": sympy.symbols("r g b", real=True),
    "xyz": sympy.symbols("x y z", real=True),
}

FFMPEG_COLORSPACE = {
    0: "rgb",
    1: "bt709",
    2: None,  # unknown
    4: "fcc",
    5: "bt470bg",
    6: "smpte170m",
    7: "smpte240m",
    8: "ycgco, ycocg",
    9: "bt2020nc, bt2020_ncl",
    10: "bt2020c, bt2020_cl",
    11: "smpte2085",
    12: "chroma-derived-nc",
    13: "chroma-derived-c",
    14: "ictcp",
    15: "ipt-c2",
    16: "ycgco-re",
    17: "ycgco-ro",
}

FFMPEG_PRIMARIES = {
    1: "bt709",
    2: None,  # unknown, unspecified
    4: "bt470m",
    5: "bt470bg",
    6: "smpte170m",
    7: "smpte240m",
    8: "film",
    9: "bt2020",
    10: "smpte428, smpte428_1",
    11: "smpte431",
    12: "smpte432",
    22: "jedec-p22, ebu3213",
}

FFMPEG_RANGE = {
    0: None,  # unknown, unspecified
    1: "tv",  # tv = mpeg = limited
    2: "pc",  # pc = jpeg = full
}

FFMPEG_TRC = {
    1: "bt709",
    2: None,  # unknown, unspecified
    4: "gamma22",
    5: "gamma28",
    6: "smpte170m",
    7: "smpte240m",
    8: "linear",
    9: "log100, log",
    10: "log316, log_sqrt",
    11: "iec61966-2-4, iec61966_2_4",
    12: "bt1361e, bt1361",
    13: "iec61966-2-1, iec61966_2_1",
    14: "bt2020-10, bt2020_10bit",
    15: "bt2020-12, bt2020_12bit",
    16: "smpte2084",
    17: "smpte428, smpte428_1",
    18: "arib-std-b67",
}

PRIMARIES = {  # red, green, blue, white primaries in CIE XY 1936
    "bt2020": ((0.708, 0.292), (0.170, 0.797), (0.131, 0.046), (0.3127, 0.3290)),
    "bt470bg": ((0.64, 0.33), (0.29, 0.60), (0.15, 0.06), (0.3127, 0.329)),  # bt601-625
    "bt470m": ((0.67, 0.33), (0.21, 0.71), (0.14, 0.08), (0.310, 0.316)),
    "bt709": ((0.64, 0.33), (0.3, 0.6), (0.15, 0.06), (0.3127, 0.329)),  # ITU-R BT.709-6
    "film": ((0.681, 0.319), (0.243, 0.692), (0.145, 0.049), (0.310, 0.316)),
    "jedec-p22, ebu3213": ((0.630, 0.340), (0.295, 0.605), (0.155, 0.077), (0.3127, 0.3290)),
    "smpte170m": ((0.630, 0.340), (0.310, 0.595), (0.155, 0.070), (0.3127, 0.329)),  # bt601-525
    "smpte428, smpte428_1": ((1.0, 0.0), (0.0, 1.0), (0.0, 0.0), (1.0/3.0, 1.0/3.0)),
    "smpte431": ((0.680, 0.320), (0.265, 0.690), (0.150, 0.060), (0.314, 0.351)),
    "smpte432": ((0.680, 0.320), (0.265, 0.690), (0.150, 0.060), (0.3127, 0.3290)),
}
PRIMARIES |= {
    "ntsc": PRIMARIES["smpte170m"],
    "pal": PRIMARIES["bt470bg"],
    "smpte240m": PRIMARIES["smpte170m"],
    "srgb": PRIMARIES["bt709"],  # alias given by ITU
}

V = sympy.Symbol("V", real=True, positive=True)  # we truth V to be in [0, 1]
L = sympy.Symbol("L", real=True)

# Values comes from International Telecomunication Union Recomandation ITU-T H.273 (V4).
# When it is noc clear in the report, values comes from:
# https://github.com/sekrit-twc/zimg/blob/master/src/zimg/colorspace/gamma.cpp
# The alpha and beta constants of the power loop are determined so as to have a c1 class function:
# V1 = alpha * L ** p - (alpha - 1) if L >= beta, V2 = q * L overwise
# V1(beta) = V2(beta) and V1'(beta) = V2(beta)
# <=> alpha = beta * (q/p - q) + 1 and (beta * q * (1-p) + p) * beta**(p-1) - q = 0
# Resolusion:
# beta, p, q = sympy.Symbol("beta"), 0.45, 4.5
# f = (beta * q * (1-p) + p) * beta**(p-1) - q
# beta = sympy.nsolve(f, (1e-6, 0.5), solver='bisect', prec=20)
# alpha = beta * (q/p - q) + 1
ALPHA_REC709 = 1.0992968268094429844
BETA_REC709 = 0.018053968510807815347
ALPHA_SMPTE240M = 1.1115721959217312779
BETA_SMPTE240M = 0.022821585529445032264
ALPHA_IEC61966 = 1.0550107189475865597
BETA_IEC61966 = 0.0030412825601275186163


# curves here: https://github.com/awxkee/colorutils-rs/blob/master/src/gamma_curves.rs
# truncate L in [0, 1] (commes from rgb), but no V truncation because we truth yuv values.
TRC = {  # l to l' and l' to l
    "bt709": (
        sympy.Min(1, sympy.Max(0, sympy.Piecewise(
            (ALPHA_REC709*L**0.45-(ALPHA_REC709-1.0), L >= BETA_REC709),
            (4.5*L, True)
        ))),
        sympy.Piecewise(
            (V/4.5, V <= BETA_REC709*4.5),
            (((V+(ALPHA_REC709-1.0))/ALPHA_REC709)**(1/0.45), True)
        ),
    ),
    "gamma22": (  # bt470m
        sympy.Min(1, sympy.Max(0, L**(1.0/2.2))), V**2.2,
    ),
    "gamma28": (  # bt470bg
        sympy.Min(1, sympy.Max(0, L**(1.0/2.8))), V**2.8,
    ),
    "smpte240m": (
        sympy.Min(1, sympy.Max(0, sympy.Piecewise(
            (ALPHA_SMPTE240M*L**0.45-(ALPHA_SMPTE240M-1.0), L >= BETA_SMPTE240M),
            (4.0*L, True)
        ))),
        sympy.Piecewise(
            (V/4.0, V <= BETA_SMPTE240M*4.0),
            (((V+(ALPHA_SMPTE240M-1.0))/ALPHA_SMPTE240M)**(1/0.45), True)
        ),
    ),
    "linear": (sympy.Min(1, sympy.Max(0, L)), V),
    "log100, log": (
        sympy.Min(1, sympy.Max(0, sympy.Max(1+(sympy.log(L)/sympy.log(10))/2, L/65536))),
        sympy.Min(10**(2*V-2), 65536*V),  # not 0 to be bijective
    ),
    "log316, log_sqrt": (
        sympy.Min(1, sympy.Max(0, sympy.Max(1+(sympy.log(L)/sympy.log(10))/2.5, L/65536))),
        sympy.Min(10**(2.5*V-2.5), 65536*V),
    ),
    "iec61966-2-1, iec61966_2_1": (  # sRGB
        sympy.Min(1, sympy.Max(0, sympy.Piecewise(
            (ALPHA_IEC61966*L**(1/2.4)-(ALPHA_IEC61966-1.0), L >= BETA_IEC61966),
            (12.92*L, True)
        ))),
        sympy.Piecewise(
            (V/12.92, V <= BETA_IEC61966*12.92),
            (((V+(ALPHA_IEC61966-1.0))/ALPHA_IEC61966)**2.4, True)
        ),
    ),
    "smpte2084": (
        # ((c1 + c2 * L**n) / (1 + c3 * L**n))**m,
        sympy.Min(1, sympy.Max(0, (
            ((107/128 + 2413/128 * L**(1305/8192)) / (1 + 2392/128 * L**(1305/8192)))**(2523/32)
        ))),
        # ((-V**(1/m) + c1)/(V**(1/m)*c3 - c2))**(1/n),
        ((-V**(32/2523) + 107/128)/(V**(32/2523)*2392/128 - 2413/128))**(8192/1305),
    ),
    "smpte428, smpte428_1": (  # in range [0, 1-eps]
        sympy.Min(1, sympy.Max(0, (48.0/52.37 * L)**(1/2.6))), 52.37/48.0 * V**2.6
    ),
    "arib-std-b67": (
        sympy.Min(1, sympy.Max(0, sympy.Piecewise(
            (0.17883277 * sympy.log(12.0*L - 0.28466892) + 0.55991073, L > 1.0/12.0),
            (sympy.sqrt(3.0*L), True)
        ))),
        sympy.Piecewise(
            ((sympy.exp((V-0.55991073)/0.17883277) + 0.28466892) / 12.0, V > 0.5),
            (V**2 / 3.0, True),
        ),
    ),
}

TRC |= {
    "bt470m": TRC["gamma22"],
    "bt470bg": TRC["gamma28"],
    "smpte170m": TRC["bt709"],
    "bt2020": TRC["bt709"],
    "bt2020-10, bt2020_10bit": TRC["bt709"],
    "bt2020-12, bt2020_12bit": TRC["bt709"],
    "iec61966-2-4, iec61966_2_4": (
        sympy.sign(L) * TRC["bt709"][0].subs(L, sympy.Abs(L)),
        sympy.sign(V) * TRC["bt709"][1].subs(V, sympy.Abs(V)),
    ),
    "bt1361e, bt1361": TRC["bt709"],  # wrong for negative L values
    "srgb": TRC["iec61966-2-1, iec61966_2_1"]  # alias given by ITU
}


__doc__ += f"""
PRIMARIES
---------
.. csv-table:: The tristimulus primaries colors (gamut), defined in the CIE XY space.
    :header: name, red, green, blue, white
    :widths: auto

    {"\n    ".join(
    f'"{n}", "x={rx}, y={ry}", "x={gx}, y={gy}", "x={bx}, y={by}", "x={wx}, y={wy}"'
    for n, ((rx, ry), (gx, gy), (bx, by), (wx, wy))
    in ((n, PRIMARIES[n]) for n in sorted(PRIMARIES)))}

TRC
---
.. csv-table:: The transfer functions (gamma), Let the luminance be Y or L, the luma Y' or V.
    :header: name, ":math:`V = f(L)`", ":math:`L = f^{{-1}}(V)`"
    :widths: auto

    {"\n    ".join(
        f'"{n}", ":math:`{sympy.latex(l2v)}`", ":math:`{sympy.latex(v2l)}`"'
        for n, (l2v, v2l) in ((n, TRC[n]) for n in sorted(TRC)))}
"""
