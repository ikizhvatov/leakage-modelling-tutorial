'''
Playing around with linear regression - 3

Fitting multi-bit models for the leakage of the AES S-box output. 

The first model is of the form

    bb + b0 x x0 + b1 x x1 + ... + b7 x x7,

where xi is bit i of byte x, and 9 coefficients bb and bi are to be estimated
with linear regression using ordinary least squares. (bb is the intercept)

Other models are:
* 2-component model (a reduced 8-component model with only 2 LSB's considered)
* Hamming weight model, i.e. with only one basis function g_0 = HW(x)
* 256-component model with all possible products of the 8 bits

Observe how the resulting coefficients match the single-bit model in the sense
of the contribution of each bit to the model.

Results in terms of the adjusted coefficient of determination:
* HW model: 0.328
* 9-component model: 0.435
* 2-component model: 0.324
* 256-component model: 0.437

Started by Ilya on 2013-05-17
Part of the leakage modeling tutorial, license is GPLv3, see https://www.gnu.org/licenses/gpl-3.0.en.html
Requires traces and data from pysca toolbox
'''

import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

##############################################################################
# These functions do 2 things in the same place:
# 1. define basis functions gi(x) of a leakage model for a byte x:
#    b0 x g0(x) + b1 x g1(x) + ... + bn x gn(x)
# 2. compute and return the values of gi(x), such that they can be used
#    later to obtain rows of the matrix for linear regression

# A simple 9-component linear model (sum of bits with different
#  coefficients): gi = xi, 0 <= i < 8.
def leakageModel9(x):
    g = []
    for i in range(0, 8):
        bit = (x >> i) & 1  # this is the definition: gi = [bit i of x]
        g.append(bit)
    return g
# same but only two LSB's included (because teh above shows that they are the
#  most contributing ones)
def leakageModel2(x):
    g = []
    for i in range(0, 2):
        bit = (x >> i) & 1
        g.append(bit)
    return g

# A Hamming weight model: g0 = HW(x)
def leakageModelHW(x):
    g = []
    hw = byteHammingWeight[x]  # this is the definition: gi = HW(x)
    g.append(hw)
    return g

# An 'all 256 bit combinations' model:
# a) helper from http://wiki.python.org/moin/BitManipulation
def parityOf(int_type):
    parity = 0
    while (int_type):
        parity = ~parity
        int_type = int_type & (int_type - 1)
    if (parity != 0): # to convert -1 to 1
        parity = 1
    return(parity)
# b) the model itself
def leakageModel256(x):
    g = []
    # note that we start from 1 to exclude case 0 which means the function
    # does not depend on any bit of x, i.e. a constant - we will add the
    # constant explicitly later as the last column.
    for i in np.arange(1, 256, dtype='uint8'):
        xmasked = x & i
        gi = parityOf(xmasked)
        g.append(gi)
    return g

 
##############################################################################


# load AES S-Box
sbox = np.load('../data/aessbox.npy')
byteHammingWeight = np.load('../data/bytehammingweight.npy')

# load samples and data
inputRange = range(0, 1000) # range for traces (not samples!)
SboxNum = 0
SampleNum = 1025

npzfile = np.load('../traces/swaes_atmega_power.npz')
data = npzfile['data'][inputRange,SboxNum]
traces = npzfile['traces'][inputRange,SampleNum]

# now, knowing the key byte, we compute the intermediate variable valuse - S-box outputs
keyByte = np.uint8(0x2B)
sBoxOut = sbox[data ^ keyByte]

# create the matrix with computed leakage model components)
X = map(leakageModel9, sBoxOut)

# perform regression, i.e. solve the system using OLS
A = sm.add_constant(X, prepend=False) # add constant coefficient (trailing column of ones)
results = sm.OLS(traces, A).fit() # the OLS itself
print results.summary()

# save the mpdel (do not forget to rename the file later!)
np.save('results/lrmodel', results.params)

# plot the coefficients except for the intercept
for i in range(len(results.params) - 1):
    line = np.array([0, results.params[i]])
    plt.plot(np.array([i, i]), line, '-', color='black')
plt.plot(results.params[0:-1], 'o')
plt.xlabel(r'$i$', fontsize=20)
plt.ylabel(r'$\beta_i$', fontsize=20)
plt.xlim(-1, A.shape[1]-1)
plt.xticks(np.arange(0, len(results.params) - 1, 32))
plt.show()
