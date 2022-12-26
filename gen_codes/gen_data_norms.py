#! /usr/bin/env python3
"""_summary_ Yolo
"""

import multiprocessing as mpc
import numpy as np
from numpy.fft import fft
from numpy.fft import ifft
from matplotlib import pyplot as plt
from itertools import repeat

pn = np.array(
    [1, 1, 1, -1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, 1,
     -1, 1, 1, -1, -1, -1, -1, 1, -1, 1, -1, 1, 1, -1, -1, 1, -1,
     1, 1, -1, -1, -1, -1, -1, 1, 1, -1, -1, -1, 1, 1, -1, -1, 1,
     -1, 1, -1, -1, -1, 1, 1, 1, 1, 1, 1, -1]
)
cfpn = np.conj(fft(pn))
best = np.array(
    [1, 1, 1, -1, 1, -1, 1, -1, -1, 1, -1, -1, 1, -1, -1, -1,
     1, -1, 1, -1, -1, 1, -1, -1, -1, 1, 1, 1, -1, 1, 1, -1,
     -1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, -1, 1, 1, -1, -1,
     1, -1, -1, -1, -1, 1, 1, 1, 1, -1, 1, -1]
)


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


SNR = -7.0
SIGMA = np.sqrt((10.0**(-SNR / 10)) / 2)
Q = 64
N = 7
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


def get_noise():
    """_summary_

    Returns:
        _type_: _description_
    """
    return SIGMA * (rng.standard_normal(Q * N) +
                    1j * rng.standard_normal(Q * N))


def rotate_seq(sequence, rotation=0):
    """_summary_

    Args:
        sequence (_type_): _description_
        rotation (int, optional): _description_. Defaults to 0.
    """
    return sequence * np.exp(1j * rotation * np.arange(sequence.size) / Q)


def sum_N(seq, endseq=N*Q):
    """_summary_

    Args:
        seq (_type_): _description_
        endseq (_type_, optional): _description_. Defaults to N.

    Returns:
        _type_: _description_
    """
    return np.sum(seq[endseq - N*Q:endseq:Q])


def norm2(sequence, endseq=Q):
    """_summary_

    Args:
        sequence (_type_): _description_
        endseq (_type_): _description_
    """
    local_seq = sequence[endseq - Q: endseq]
    return np.sqrt(np.sum(local_seq.real**2 + local_seq.imag**2))


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
    return np.array(res)


def calc_score_normed(sequence):
    """_summary_

    Args:
        sequence (_type_): _description_
    """
    with mpc.Pool() as pool_obj:
        seqrep = zip(repeat(sequence), range(Q, sequence.size))
        corrs = np.array(pool_obj.starmap(corrfft, seqrep), np.complex64)
        norms = np.array([norm2(sequence, k) for k in range(Q, sequence.size)], np.float32)
        all_maxs = np.array([np.max(np.abs(corr)) for corr in corrs]) / norms
        res2 = np.array(pool_obj.starmap(
            sum_N, zip(repeat(all_maxs), range(N*Q, all_maxs.size))
        ))
    return res2, norms


codeword = rng.integers(0, 63, N)
qcsp_frame = over_modulate(ccsk_modulate(codeword))
full_seq = np.concatenate((
    np.zeros(int(Q*N*3/2)),
    qcsp_frame,
    np.zeros(int(Q*N*3/2))
))
noise = np.concatenate((
    get_noise()[:int(Q*N/2)],
    get_noise(),
    get_noise(),
    get_noise(),
    get_noise()[:int(Q*N/2)]
))

mpc.freeze_support()

gainvar = np.ones(full_seq.shape)

varsize = int(Q*N)

for i in range(1,  128):
    rng.standard_normal()
for i in range(1,  int(gainvar.size / varsize)):
    val = 10**(rng.standard_normal() * -1 / 10)
    gainvar[i * varsize: (i+1) * varsize] = val

gainvar = np.roll(gainvar, rng.integers(0, N * Q / 2))

noisy_seq = noise + full_seq
noisy_seq_gain = noisy_seq * gainvar

result_0 = calc_score(noisy_seq)
result_gained = calc_score(noisy_seq_gain)
result_normed, normres = calc_score_normed(noisy_seq_gain)

plt.plot(result_0)
plt.plot(result_gained)
plt.show()

plt.plot(result_normed)
plt.show()

tuple_to_w = (
    np.arange(gainvar.size),
    gainvar,
    np.concatenate((result_0, np.zeros(gainvar.size - result_0.size))),
    np.concatenate((result_gained, np.zeros(gainvar.size - result_0.size))),
    np.concatenate((result_normed, np.zeros(gainvar.size - result_0.size)))
)

np.savetxt(
    'result.dat',
    np.transpose(tuple_to_w)
)
