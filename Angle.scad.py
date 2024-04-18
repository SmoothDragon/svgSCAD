#!/usr/bin/env python3

from __future__ import division

import solid2 as sd
import scipy.spatial

from math import atan, sqrt
import numpy as np
from typing import *


if __name__ == '__main__':
    fn = 256
    piece = sd.cube([20,60,10]) + sd.cube([60,20,10])
    final = sd.scad_render(piece, file_header=f'$fn={fn};')
    print(final)
