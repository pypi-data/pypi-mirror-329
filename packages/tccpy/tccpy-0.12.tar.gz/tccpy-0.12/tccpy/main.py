"""Target Confusability Competition (TCC) model 
This is a Python implementation of the Target Confusability Competition (TCC) model proposed by 
Shurgin et al. (2020), (https://www.nature.com/articles/s41562-020-00938-0. An interactive web-version of the model 
is available in the Target confusability competition model (TCC) primer, https://bradylab.ucsd.edu/tcc/.

Usage: 

The following code will run 100 iterations of TCC over four targets with familiarity 0, 0, 1, and 2:

    import tccpy

    dist = tccpy.tcc([0,0,1,2], 1, 1000)
    print(dist)

Copyright [2025] [Erik Billing, https://his.se/erikb]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import numpy as np

def tccUCN(dPrime, similarity):
    """
    Target Confusability Competition (TCC):
        * dPrime: scalar, list or numpy array specifying the familiarity (memory matching signal) of each cued target
        * similarity: list or numpy array specifying similarity for each potential target
        returns a vector specifying the index of the selected target, for each cued target.

        This is a Python interpretation of the original matlab reference implementation with uncorrelated noise provided by Shurgin et al. (2020).
    """
    if not isinstance(dPrime, np.ndarray): dPrime = np.array(dPrime)
    if not isinstance(similarity, np.ndarray): similarity = np.array(similarity)
    sig = np.random.normal(loc=0,scale=1,size=(dPrime.size,similarity.size)) + np.tile(similarity.ravel(), (dPrime.size, 1)) * dPrime
    return np.argmax(sig, axis=1)

def tcc(familiarity, count = 1, returnDetectionSignal = False):
    """
    Target Confusability Competition (TCC):
        * familiarity: list or 1d numpy array specifying the familiarity (memory matching signal) of each potential target
        * count: the number of iterations to execute
        tcc returns a target confusability distribution over each potential target specified by the familiarity parameter. If returnDetectionSignal is true, a (dist,sig,sigMax) tuple is returned, where sig and sigMax represents the detection signal and winning target of each executed iteration.
    """
    if not isinstance(familiarity, np.ndarray): familiarity = np.array(familiarity)
    sig = np.random.normal(loc=0,scale=1,size=(count,familiarity.shape[0])) + np.tile(familiarity, (count, 1))
    sigMax = np.argmax(sig, axis=1)
    unique_values, dist = np.unique(sigMax, return_counts=True)
    if returnDetectionSignal:
        return dist, sig, sigMax
    else:
        return dist