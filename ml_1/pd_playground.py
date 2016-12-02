#!/usr/bin/env python

import numpy as np
import pandas as pd

r = np.arange(1, 7).reshape((3, 2))
df = pd.DataFrame(r, columns=list('AB'))

print(df)
print(df.pct_change())
