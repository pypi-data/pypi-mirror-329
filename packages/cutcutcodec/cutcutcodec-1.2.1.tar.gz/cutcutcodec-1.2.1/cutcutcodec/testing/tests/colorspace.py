#!/usr/bin/env python3

"""Some test on colorspace function."""

import torch

from cutcutcodec.core.compilation.sympy_to_torch.lambdify import Lambdify
from cutcutcodec.core.colorspace.cst import TRC


def _test_trc_bij(code: str):
    """Test if the transfer function is bijective."""
    func_symb, inv_symb = TRC[code]
    func = Lambdify(func_symb)
    inv = Lambdify(inv_symb)
    l_num = torch.linspace(0.0, 1.0, 1_000_000, dtype=torch.float64)
    v_num = func(l_num)

    # import matplotlib.pyplot as plt
    # plt.xlabel("linear rgb")
    # plt.ylabel("gamma corrected r'g'b'")
    # plt.title(code)
    # plt.plot(l_num, v_num)
    # plt.plot(l_num, inv_num(l_num))
    # plt.show()

    assert v_num.min() >= -1e-8
    assert v_num.max() <= 1.0 + 1e-8
    l_num_bis = inv(v_num)
    assert torch.allclose(l_num, l_num_bis)


def test_trc_bt709():
    """Ensure the transfer function."""
    _test_trc_bij("bt709")


def test_trc_gamma22():
    """Ensure the transfer function."""
    _test_trc_bij("gamma22")


def test_trc_gamma28():
    """Ensure the transfer function."""
    _test_trc_bij("gamma28")


def test_trc_smpte240m():
    """Ensure the transfer function."""
    _test_trc_bij("smpte240m")


def test_trc_linear():
    """Ensure the transfer function."""
    _test_trc_bij("linear")


def test_trc_log100():
    """Ensure the transfer function."""
    _test_trc_bij("log100, log")


def test_trc_log316():
    """Ensure the transfer function."""
    _test_trc_bij("log316, log_sqrt")


def test_trc_iec_61966_2_4():
    """Ensure the transfer function."""
    _test_trc_bij("iec61966-2-4, iec61966_2_4")


def test_trc_bt1361():
    """Ensure the transfer function."""
    _test_trc_bij("bt1361e, bt1361")


def test_trc_iec61966():
    """Ensure the transfer function."""
    _test_trc_bij("iec61966-2-1, iec61966_2_1")


def test_trc_smpte2084():
    """Ensure the transfer function."""
    _test_trc_bij("smpte2084")


def test_trc_smpte428():
    """Ensure the transfer function."""
    _test_trc_bij("smpte428, smpte428_1")


def test_trc_arib():
    """Ensure the transfer function."""
    _test_trc_bij("arib-std-b67")
