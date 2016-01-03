#!/usr/bin/python2.7.6 -tt

import pandas as pd
from ros import ros

x = pd.Series([0.5,0.5,1,1.5,5,10,100])
y = pd.Series([1,0,0,1,0,0,0], dtype='bool8')

z = ros(x,y)
print(z)
