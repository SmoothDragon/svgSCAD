#!/usr/bin/env python

'''Nested fidget star with a twist
Uses svgSCAD package.
'''

import solid as sd
import numpy as np
import svgSCAD as svg


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


if __name__ == '__main__':
    R = 50
    scale = 1/np.sqrt(3)
    fn = 6
    twist = 15
    slices=10
    scale=.8

    koch = koch_snowflake(R, iterations=0)
    koch = perimeter(koch, 1)
    graphic = sd.linear_extrude(height=10, twist=twist, slices=slices, scale=scale)(koch)
    graphic += sd.mirror([0,0,1])(graphic)
    koch = koch_snowflake(R-3, iterations=0)
    koch = perimeter(koch, 1)
    graphic2 = sd.linear_extrude(height=10, twist=twist, slices=slices, scale=scale)(koch)
    graphic2 += sd.mirror([0,0,1])(graphic2)
    koch = koch_snowflake(R-6, iterations=0)
    koch = perimeter(koch, 1)
    graphic3 = sd.linear_extrude(height=10, twist=twist, slices=slices, scale=scale)(koch)
    graphic3 += sd.mirror([0,0,1])(graphic3)
    final = graphic + graphic2 + graphic3
    final = sd.scad_render(final, file_header=f'$fn={fn};')
    print(final)




