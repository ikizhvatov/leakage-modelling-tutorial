'''
Playing around with linear regression - 5

Comparing different leakage models for illustration:

- 9-component fitted model
- Hamming Weight (with fitted coefficients and pure)
- reduced template (means only)

These models are obtaiend with scripts 3 and 4 (and some manual file renaming)

The predicted leakge for each of the values of the intermediate variable are
plotted, and Pearson corelation coefficient between the prediction vectors
is computed.

Note that both fitted HW and pure HW yield the same correlation coefficient
of 0.857798 from comparison to the to 9-component LR-fitted model. This
ilustrates the property of the Pearson correlation coefficient to be invariant
under an affine linear transformation.

Started by Ilya on 2013-05-21
Part of the leakage modeling tutorial, license is GPLv3, see https://www.gnu.org/licenses/gpl-3.0.en.html
Requires traces and data from pysca toolbox
'''

import numpy as np
import matplotlib.pyplot as plt

# functions for computing leakage mode
# 8-component leakage function; beta is a 9-element array
def leakage9(x, beta):
    result = beta[8]
    for i in range(0, 8):
        bit = (x >> i) & 1  # this is the definition: gi = [bit i of x]
        result += beta[i] * bit
    return result

# hamming weight leakage model (with coefficient and intercept from LR though)
# beta is a 2-element array
def leakageHWfitted(x, beta):
    return beta[0] * byteHammingWeight[x] + beta[1]

# hamming weight leakage model (pure)
def leakageHWpure(x, beta):
    return byteHammingWeight[x]

##############################################################################

# load the required data
byteHammingWeight = np.load('../data/bytehammingweight.npy') # HW table
beta9 = np.load('results/lrmodel9_1000traces.npy') # 9 coefs, the last one being the intercept
betaHW = np.load('results/lrmodelhw.npy') # 2 coefs, the last one being the intercept
#predictionsT = np.load('results/means2000.npy') # reduced templates, i.e. just means

predictions9 = np.zeros(256)
predictionsHW = np.zeros(256)

# for all inputs predict the leakage
for x in range(256):
    predictions9[x] = leakage9(x, beta9)
    predictionsHW[x] = leakageHWfitted(x, betaHW) # replace by leakageHWpure
                                                  # to see no difference :)

# correlate the models
c = np.corrcoef(predictions9, predictionsHW)
print "Correlation: %f" % c[0,1]

# plot the two leakage vectors, vizualizing the difference
for x in range(256):
    line = np.array([predictions9[x], predictionsHW[x]])
    plt.plot(np.array([x, x]), line, '-', color='silver')
p1, = plt.plot(predictions9, 'r.')  # left-hand size is for later use in the legend
p2, = plt.plot(predictionsHW, 'g.')
#p3, = plt.plot(predictionsT, 'b.')

plt.xlim(-1, 256)
plt.xlabel('Value of the intermediate variable')
plt.ylabel('Leakage predicted by a model')
plt.title('Correlation: %f' % c[0,1])
plt.legend([p1, p2], ['9-component LR fitted', 'Hamming weight'], loc='best', numpoints=1)
plt.show()
