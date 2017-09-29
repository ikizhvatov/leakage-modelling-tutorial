# Side channel leakage modelling tutorial

This is a collection of scripts that I developed back in 2013 to understand apllication of linear regression techniques in side channel analysis.

## Background

The tutorial is mainly inspired by the following paper:
* [Carolyn Whitnall and Elisabeth Oswald. Profiling DPA: Efficacy and efficiency trade-offs](https://eprint.iacr.org/2013/353)

Another paper would also help the understanding of linear regression techniques (in the non-profiled setting, which is not covered by this tutorial):
* [Victor Lomné, Emmanuel Prouff, and Thomas Roche. Behind the Scene of Side Channel Attacks](https://eprint.iacr.org/2013/794)

If you are completely new to side channel analysis, you would need [this book](http://dpabook.org).

The tutorial uses the same example traces and data as the [Pysca toobox](https://github.com/ikizhvatov/pysca). It is intended to be a subfolder of Pysca but maintained as a separate repository. It is tested with Python 3.

## Contents

1. [Simulation of single bit leakage](1-Simulation.ipynb). Fitting a line using Ordinary Least Squares (OLS).

2. [Real leakge of a single bit](2-Singlebit.ipynb). Measurements here and below come from an AES-128 implementation on an 8-bit AVR microcontroller. In addition to linear regression with OLS, we use another technique for leakage modelling: building templates.

3. [Multi-bit leakge modelling](3-Multibit.ipynb). Performing linear regression with different sets of basis functions of all the 8 bits of the target variable.

4. [Templates](4-Templates.ipynb). Building reduced templates, now for the full 8-bit values.

5. [Comparing leakage models](5-CompareLeakageModels.ipynb). First layer of comparison between Hamming weight and models built using linear regression and templates. Plotting the values side-by-side and computing correlation between them.

6. [Running a correlation attack](6-COmpareSingleAttack.ipynb). Second layer of comparison: looking at the effect of the correlation-based distinguisher with different models plugged in.

7. TODO. Computing the success rate. Running many attacks to get the ratio the of successful ones. Illustrates the point that linear regression needs less traces than template building to obtain a model that is precise enough in this case.

Author: Ilya Kizhvatov<br>
License: GPLv3