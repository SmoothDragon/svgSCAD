#!/usr/bin/env python

import solid as sd
import numpy as np
import sys

phi = (np.sqrt(5)+1)/2

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

def snowfish(R, pieces=5, iterations=3):
    scale = (3-np.sqrt(5))/2
    shift = (np.sqrt(5)-1)/2
    base = sd.circle(R, segments=pieces)
    for _ in range(iterations):
        base2 = sd.scale(scale)(base)
        base3 = sd.translate([R*shift,0])(base2)
        base = sd.union()(*[sd.rotate([0,0,i*360/pieces])(base3) for i in range(pieces)])
        base += sd.rotate([0,0,180])(base2)
    base = sd.rotate([0,0,90])(base)
    return base

def startree(R, base, pieces=5, iterations=3):
    scale = (3-np.sqrt(5))/2
    shift = (np.sqrt(5)-1)/2
    for _ in range(iterations):
        base2 = sd.scale(scale)(base)
        base3 = sd.translate([R*shift,0])(base2)
        base += sd.union()(*[sd.rotate([0,0,i*360/pieces])(base3) for i in range(pieces)])
        # base += sd.rotate([0,0,180])(base2)
    base = sd.rotate([0,0,90])(base)
    return base

def rotate_spread(R, base, include_center=False, pieces=5, iterations=3):
    scale = (3-np.sqrt(5))/2
    shift = (np.sqrt(5)-1)/2
    for _ in range(iterations):
        base2 = sd.scale(scale)(base)
        base3 = sd.translate([R*shift, 0])(base2)
        base4 = sd.union()(*[sd.rotate([0, 0, i*360/pieces])(base3) for i in range(pieces)])
        if include_center:
            base += base4
        else:
            base = base4
    base = sd.rotate([0,0,90])(base)
    return base

def logo1(R):
    base = pentagram(R)


def square20copies(final, R):
    # Make 20 copies in square
    sy = 1.75
    sx = 1.55
    final += sd.translate([0,sy*R])(final)
    final += sd.translate([0,2*sy*R])(final)
    last = final
    final += sd.translate([sx*R,4.51*R])(sd.rotate([0,0,180])(final))
    final += sd.translate([2*sx*R,0])(final)
    final += sd.translate([4*sx*R,0])(last)
    final = sd.translate([1*R,1.8*R])(final)
    return final

def square12copies(final, R):
    # Make 20 copies in square
    sy = 1.8
    sx = 1.5
    sY = 4.6
    final += sd.translate([0,sy*R])(final) + sd.translate([0,2*sy*R])(final)
    final += sd.translate([sx*R,sY*R])(sd.rotate([0,0,180])(final))
    final += sd.translate([2*sx*R,0])(final)
    final = sd.translate([1*R,1.8*R])(final)
    return final

def stack3(final, R):
    # Make 20 copies in square
    sy = 1.8
    sx = 1.5
    sY = 4.6
    final += sd.translate([0,sy*R])(final) + sd.translate([0,2*sy*R])(final)
    return final

if __name__ == '__main__':
    fn = 512
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
    outline = sd.circle(r=R)
    pattern = sd.circle(r=phi*scale*R, segments=5)
    pattern = sd.rotate([0,0,90])(pattern)
    outline = sd.minkowski()(star, pattern)
    final = outline
    final -= star
    final = tree
    final += year

    # Uncomment for cutting
    final = star

    # print(sd.scad_render(final, file_header=f'$fn={fn};'))
    # exit(0)
    final = stack3(final, R)
    print(sd.scad_render(final, file_header=f'$fn={fn};'))
