# tccpy - Target Confusability Competition (TCC) model 
This is a Python implementation of the Target Confusability Competition (TCC) visual memory model proposed by [Shurgin et al. (2020)](https://www.nature.com/articles/s41562-020-00938-0). The model builds on a combination of psychophysical scaling and signal detection theory and has been used to predict human memory performance on a wide range of visual (color selection) tasks. An interactive web-version of the model is available in the [Target confusability competition model (TCC) primer](https://bradylab.ucsd.edu/tcc/). 

## Setup

To install **tccpy**, simply do: 

    pip install tccpy

## Usage
TCC models the memory of each potential target using a memory match signal referred to as *familiarity*. A higher familiarity implies a stronger memory of that target, and as a result a higher likelihood for selection. The following code will run 100 iterations of TCC over four targets with familiarity 0, 0, 1, and 2:

    import tccpy

    dist = tccpy.tcc(familiarity=[0,0,1,2], count=100)
    print(dist) # should return something like array([ 6,  4, 20, 70])

## Acknowledgments

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



