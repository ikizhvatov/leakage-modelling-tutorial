'''
Playing around with linear regression - 1

A very simple example simulating the leakage of a single bit in the Gaussian
model, and then fitting the line onto it using (ordinary) least squares.

Started by Ilya on 2013-05-14
Part of the leakage modeling tutorial, license is GPLv3, see https://www.gnu.org/licenses/gpl-3.0.en.html
Requires traces and data from pysca toolbox
'''

import matplotlib.pyplot as plt
import numpy as np

# create simulated data (half for 0, half for 1)
numSamples = 100
mu0, sigma0 = 10, 2 # mean and standard deviation for 0
mu1, sigma1 = 20, 4 # mean and standard deviation for 1
samples0 = np.random.normal(mu0, sigma0, numSamples/2)
samples1 = np.random.normal(mu1, sigma1, numSamples/2)

x = np.concatenate((np.zeros(len(samples0)), np.ones(len(samples1)))) # intermediate variables
y = np.concatenate((samples0, samples1)) # simulated leakages

# create the matrix (left-hand side of the over-determined system) necessary
#  for the numpy least squares routine
columnOfOnes = np.concatenate((np.ones(len(samples0)), np.ones(len(samples1))))
A = np.vstack((x, columnOfOnes))

# perform regression, i.e. solve the system using OLS
beta = np.linalg.lstsq(A.T,y)[0] # obtaining the parameters

# visualize initial data (as dots) and the fitted line
xnew = np.arange(-1,3)
line = beta[0] * xnew + beta[1] # regression line
plt.plot(xnew, line, 'r-', x, y, '.')
plt.xlim((-1, 2))
plt.ylim((0, 30))
plt.show()
