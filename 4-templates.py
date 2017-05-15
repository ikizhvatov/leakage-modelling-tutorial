'''
Playing around with linear regression - 4

Build reduced templates (only the mean, no covariance matrix)

Started by Ilya on 2013-05-17
Part of the leakage modeling tutorial, license is GPLv3, see https://www.gnu.org/licenses/gpl-3.0.en.html
Requires traces and data from pysca toolbox
'''

import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

# load AES S-Box
sbox = np.load('../data/aessbox.npy')
byteHammingWeight = np.load('../data/bytehammingweight.npy')

# load samples and data
inputRange = range(0, 2000)  # range for traces (not samples!)
SboxNum = 0
SampleNum = 1025

npzfile = np.load('../traces/swaes_atmega_power.npz')
data = npzfile['data'][inputRange, SboxNum]
traces = npzfile['traces'][inputRange, SampleNum]

# now, knowing the key byte, we compute the intermediate variable valuse - S-box outputs
keyByte = np.uint8(0x2B)
sBoxOut = sbox[data ^ keyByte]

# organize the samples according to the data
binnedSamples = []
for i in range(256):
    binnedSamples.append([])

for i in range(len(data)):
    binnedSamples[sBoxOut[i]].append(traces[i])

# save binned samples, needed with 2000 traces for incomplete template correction below
#np.save('results/binnedSamples', binnedSamples)

###########
# some correcting tricks

# truncate to 2 samples per value (I do not remember why I needed it)
#for i in range(256):
#    binnedSamples[i] = binnedSamples[i][0:2]

# Compensating for incomplete template
# for small amount of traces, we will not get traces for every out of 256 input values
# so some bins will be empty
# here we replenish the missing means from a file with all bins populated by at least one traces
# such a file can be obtained by this script by running it on 2000 traces
# (see the commented line saving the binned samples above)
# this is just for simplicity, to avoid dealing with an incomplete template lateer
# of course it somewhat improves the model, but for our comaprison later it does not matter much
binnedSamples2000 = np.load('results/binnedSamples2000.npy')
for i in range(256):
    if not binnedSamples[i]:
        binnedSamples[i] = binnedSamples2000[i]

#
###########

means = map(np.mean, binnedSamples)

# save the results (do not forget to rename the file later!)
np.save('results/means', means)
