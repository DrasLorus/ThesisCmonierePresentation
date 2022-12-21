#! /usr/bin/env python3

import numpy as np
from numpy import fft
from matplotlib import pyplot as plt
#import os

#with open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/test_pn.txt')), 'r') as f:
#     content = f.read().strip().split();

#pn = np.array(list(map(int, content)))

#del content

#cft = np.conj(fft.fft(pn))

#results = [fft.ifft(fft.fft(np.roll(pn, v)) * cft) for v in np.arange(pn.size)]

#plt.plot(np.abs(results[0] ))
#plt.plot(np.abs(results[16]))
#plt.plot(np.abs(results[39]))
#plt.plot(np.abs(results[56]))
#plt.show()

pn = np.array([1, -1, -1, -1])
cft = np.conj(fft.fft(pn))
results = [fft.ifft(fft.fft(np.roll(pn, v)) * cft) for v in np.arange(pn.size)]
plt.subplot(1, 4, 1)
plt.stem(results[0], '-*')
plt.subplot(1, 4, 2)
plt.stem(results[1], '-d')
plt.subplot(1, 4, 3)
plt.stem(results[2], '-s')
plt.subplot(1, 4, 4)
plt.stem(results[3], '-x')
plt.show()



