#!/usr/bin/env python

'''Nested fidget star with a twist
Uses svgSCAD package.
'''

import solid2 as sd
import numpy as np
import svgSCAD as svg
import itertools



def perimeter(shape, r, segments=64):
    border = sd.circle(r=r, _fn=segments)
    final = sd.minkowski()(shape, border)
    final -= shape
    return final

def cross(R):
    center = sd.square([R, R/4], center=True)
    center += sd.rotate([0,0,90])(center)
    return center

def ring(R, r, height, twist, slices, scale):
    koch = cross(R)
    koch = perimeter(koch, r)
    graphic = sd.linear_extrude(height=10, twist=twist, slices=slices, scale=scale)(koch)
    graphic += sd.rotate([180,0,180])(graphic)
    return graphic

def cross_perimeter(R, r, pushout, wall=.8):
    cross = sd.square([R, r], center=True)
    cross += sd.rotate([0,0,90])(cross)
    if pushout > 0:
        cross = sd.minkowski()(cross, sd.square(pushout, center=True))
    outer = sd.minkowski()(cross, sd.square(2*wall, center=True))
    outer -= cross
    return outer
    # Minkowski sum of square with cross
    # Make square bigger with each iteration
    # Stack layers formed by Minkowski
    # Walls are .8mm, gap between each layer 2mm?


def cross_extrude(R, r, h, pushout, wall=.8):
    total = []
    step = .5
    for z in range(5*h):
        total.append(sd.rotate([0,0,-step*z])(sd.translate([0,0,z*.2])(sd.linear_extrude(height=.2)(cross_perimeter(R, r, pushout+2*z*.2)))))
    shape = sd.union()(*total)
    shape = sd.translate([0,0,-h])(shape)
    shape = sd.rotate([0,0,step*5*h])(shape)
    shape += sd.rotate([0,180,0])(shape)
    return shape

if __name__ == '__main__':
    fn = 64
    R = 50
    r = 10
    h = 10
    wall = .8
    gap = 2
    shift = 2*(wall+gap)
    shape = sd.union()(*[cross_extrude(R, r, h, i*shift, wall) for i in range(8)])
    # shape = sd.translate([0,0,-h])(shape)
    # shape += sd.mirror([0,0,1])(shape)
    # shape = sd.union()(*[cross_perimeter(R, r, i*shift, wall) for i in range(8)])
    # shape = cross_perimeter(R, r, 0)
    # shape += cross_perimeter(R, r, 2*wall+2*gap)
    # final = sd.union()(*[ring(R-i*gap, 1.2, height=10, twist=twist, slices=slices, scale=scale) for i in range(8)])
    final = sd.scad_render(shape, file_header=f'$fn={fn};')
    print(final)




