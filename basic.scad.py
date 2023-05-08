#!/usr/bin/env python

import solid as sd
import numpy as np

n = 5
points = np.exp(2j*np.pi/n*np.arange(n))
result = sd.polygon(np.column_stack([points.real,points.imag]))
print(sd.scad_render(result))


