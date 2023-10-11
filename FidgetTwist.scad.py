#!/usr/bin/env python

'''Nested fidget star with a twist
Uses svgSCAD package.
'''

import solid as sd
import numpy as np
import svgSCAD as svg
import itertools


def koch_snowflake(R, pieces=6, iterations=3):
    scale = 1/3
    base = svg.hexagram(R)
    for _ in range(iterations):
        base2 = sd.scale(scale)(base)
        base3 = sd.translate([(1-scale)*R,0])(base2)
        base += sd.union()(*[sd.rotate([0,0,i*360/pieces])(base3) for i in range(pieces)])
    base = sd.rotate([0,0,30])(base)
    return base

def perimeter(shape, r, segments=6):
    border = sd.circle(r=r, segments=segments)
    final = sd.minkowski()(shape, border)
    final -= shape
    return final

def ring(R, r, height, twist, slices, scale):
    koch = koch_snowflake(R, iterations=0)
    koch = perimeter(koch, r)
    graphic = sd.linear_extrude(height=10, twist=twist, slices=slices, scale=scale)(koch)
    graphic += sd.rotate([180,0,0])(graphic)
    return graphic

if __name__ == '__main__':
    R = 62
    fn = 6
    twist = 15
    slices=50
    scale=.8
    gap = 6
    gaps = [8,7.5,7,6.5,6,5.5,5,4.5,4]
    drops = itertools.accumulate(gaps, initial=0)
    # drops = itertools.accumulate(gaps)

    # final = sd.union()(*[ring(R-i*gap, 1.2, height=10, twist=twist, slices=slices, scale=scale) for i in range(8)])
    final = sd.union()(*[ring(R-drop, 1.2, height=10, twist=twist, slices=slices, scale=scale) for drop in drops])
    final = sd.scad_render(final, file_header=f'$fn={fn};')
    print(final)




