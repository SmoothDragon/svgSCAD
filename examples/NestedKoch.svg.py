#!/usr/bin/env python

'''Nested tiling of Koch snowflakes.
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

if __name__ == '__main__':
    R = 50
    scale = 1/np.sqrt(3)

    koch = koch_snowflake(R, iterations=3)
    ring = sd.scale(scale)(koch)
    ring = sd.rotate([0,0,30])(ring)
    ring = sd.translate([2/np.sqrt(3)*R,0,0])(ring)
    ring = sd.union()(*[sd.rotate([0,0,i*60])(ring) for i in range(6)])
    ring2 = sd.scale(scale)(ring)
    ring2 = sd.rotate([0,0,30])(ring2)
    ring3 = sd.scale(scale)(ring2)
    ring3 = sd.rotate([0,0,30])(ring3)
    graphic = svg.scadSVG(koch, fill='blue',strokewidth=.01)
    graphic += svg.scadSVG(ring, fill='blue',strokewidth=.01)
    graphic += svg.scadSVG(ring2, fill='red',strokewidth=.01)
    graphic += svg.scadSVG(ring3, fill='yellow',strokewidth=.01)
    print(graphic)




