# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 13:12:19 2018

@author: vince
"""

import numpy as np

hoi = float(200/(128 - 0.99999999))
hoi2 = float(0.9999999*200/128)
hoi3 = float(200/(128 - 1))

print(hoi3 == hoi)