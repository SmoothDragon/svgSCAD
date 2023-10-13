#!/usr/bin/env python

'''Challenge coin for cutting and etching on a laser cutter.
Uses svgSCAD package.
'''

import solid as sd
import numpy as np
import svgSCAD as svg

def pentagram(R):
    wedge = sd.square(R)
    wedge = sd.intersection()(
                sd.rotate([0,0,18])(wedge),
                sd.rotate([0,0,72])(wedge),
                sd.translate([-R/2,0])(wedge),
                )
    wedge = sd.translate([0,-R])(wedge)
    wedge = sd.rotate([0,0,180])(wedge)
    base = sd.union()(*[sd.rotate([0,0,i*360/pieces])(wedge) for i in range(pieces)])

def starfish(R, pieces=5, iterations=3):
    scale = 1-1/phi
    wedge = sd.square(R)
    wedge = sd.intersection()(
                sd.rotate([0,0,18])(wedge),
                sd.rotate([0,0,72])(wedge),
                sd.translate([-R/2,0])(wedge),
                )
    wedge = sd.translate([0,-R])(wedge)
    wedge = sd.rotate([0,0,180])(wedge)
    base = sd.union()(*[sd.rotate([0,0,i*360/pieces])(wedge) for i in range(pieces)])
    for _ in range(iterations):
        base2 = sd.scale(scale)(base)
        base3 = sd.translate([0,(1-scale)*R])(base2)
        base += sd.union()(*[sd.rotate([0,0,i*360/pieces])(base3) for i in range(pieces)])
    return base

def stack3(final, R):
    # Make 20 copies in square
    sy = 1.8
    sx = 1.5
    sY = 4.6
    final += sd.translate([0,sy*R])(final) + sd.translate([0,2*sy*R])(final)
    return final

if __name__ == '__main__':
    fn = 512
    phi = (np.sqrt(5)+1)/2
    R = 50
    iterations = 3 #4
    t_iter = 2 # 2
    font_size = 9
    scale = (1-1/phi)**4

    star = starfish(R,iterations=iterations)
    year = sd.text('20  23', size=font_size, halign='center', valign='center')
    year = sd.translate([0,-.7*font_size])(year)
    tree = sd.import_('ljtree_lowres.svg')
    tree = sd.translate([-65,-213])(tree)
    tree = sd.scale(.3)(tree)
    pattern = sd.circle(r=phi*scale*R, segments=5)
    pattern = sd.rotate([0,0,90])(pattern)
    outline = sd.minkowski()(star, pattern)
    final = outline
    final -= star
    final += tree
    final += year
    final = tree

    # Uncomment for cutting
    # final = star

    # print(sd.scad_render(final, file_header=f'$fn={fn};'))
    # exit(0)
    # final = stack3(final, R)
    print(svg.scadSVG(final, fn=fn, fill='blue')) #+svg.scadSVG(image2, fn=fn, fill='lightgreen'))




