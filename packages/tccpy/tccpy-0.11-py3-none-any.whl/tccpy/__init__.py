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

from .main import tcc