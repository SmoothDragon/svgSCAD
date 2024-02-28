#!/usr/bin/env python

'''Nested fidget star with a twist
Uses svgSCAD package.
'''

import solid2 as sd
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
    base = sd.rotate(30)(base)
    return base

def perimeter(shape, r, segments=64):
    border = sd.circle(r=r, _fn=segments)
    final = sd.minkowski()(shape, border)
    final -= shape
    return final

def heart(R):
    center = sd.square(R, center=True)
    curve = sd.circle(d=R)
    center += sd.translate([R/2,0])(curve)
    center += sd.translate([0,R/2])(curve)
    center = sd.rotate(45)(center)
    center = sd.translate([0,-R/8])(center)
    return center

def ring(R, r, height, twist, slices, scale):
    koch = heart(R)
    koch = perimeter(koch, r)
    graphic = sd.linear_extrude(height=10, twist=twist, slices=slices, scale=scale)(koch)
    graphic += sd.rotate([180,0,180])(graphic)
    return graphic

if __name__ == '__main__':
    R = 62
    fn = 45
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




