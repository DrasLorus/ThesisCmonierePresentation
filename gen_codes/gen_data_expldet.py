#! /usr/bin/env python3
"""_summary_ Yolo
"""

import multiprocessing as mpc
import numpy as np
from numpy.fft import fft
from numpy.fft import ifft
from matplotlib import pyplot as plt
from itertools import repeat

pn = np.array([1, -1, -1, -1])
cfpn = np.conj(fft(pn))
best = np.array([-1, 1, 1, -1, 1, -1])


def ccsk_modulate(word):
    """_summary_

    Args:
        word (_type_): _description_

    Returns:
        _type_: _description_
    """
    return np.array(np.concatenate([np.roll(pn, symbol) for symbol in word]))


def over_modulate(ccsk_word):
    """_summary_

    Args:
        word (_type_): _description_

    Returns:
        _type_: _description_
    """
    return np.array(np.concatenate(
        [symbol * ovmod for symbol,
            ovmod in zip(np.reshape(ccsk_word, (N, Q)), best[:N])]
    ))


Q = 4
N = 6
rng = np.random.default_rng(12345)


def corrfft(sequence, endseq=Q):
    """_summary_ do CCSK correlation

    Args:
        sequence (_type_): _description_
        endseq   (_type_): _description_

    Returns:
        _type_: _description_
    """
    return ifft(fft(sequence[endseq - Q:endseq]) * cfpn)


def sum_N(seq, endseq=N*Q):
    """_summary_

    Args:
        seq (_type_): _description_
        endseq (_type_, optional): _description_. Defaults to N.

    Returns:
        _type_: _description_
    """
    return np.sum(seq[endseq - N*Q:endseq:Q])


def calc_score(sequence):
    """_summary_

    Args:
        sequence (_type_): _description_
    """
    with mpc.Pool() as pool_obj:
        corrs = np.array(pool_obj.starmap(
            corrfft, zip(repeat(sequence), range(Q, sequence.size))
        ), np.complex64)
        all_maxs = np.array([np.max(np.abs(corr)) for corr in corrs])
        res = pool_obj.starmap(
            sum_N, zip(repeat(all_maxs), range(N*Q, all_maxs.size))
        )
    return np.array(res), all_maxs


codeword = np.array([1, 2, 1, 3, 2, 3])
qcsp_frame = over_modulate(ccsk_modulate(codeword))
full_seq = np.concatenate((
    np.zeros(int(Q*N*3/2)),
    qcsp_frame,
    np.zeros(int(Q*N*3/2))
))

mpc.freeze_support()

result, maxs = calc_score(full_seq)

plt.plot(result)
plt.show()

plt.plot(maxs)
plt.show()

np.savetxt(
    'result.dat',
    np.transpose(np.array([np.arange(result.size), result]))
)

np.savetxt(
    'maxs.dat',
    np.transpose(np.array([np.arange(maxs.size), maxs]))
)
