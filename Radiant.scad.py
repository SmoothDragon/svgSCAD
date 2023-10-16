#!/usr/bin/env python

'''Prime radiant model
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

def path(v, L):
    edges = [sd.hull()(sd.translate(list(v0))(v), sd.translate(list(v1))(v)) for v0,v1 in zip(L, list(np.roll(L,-1,axis=0)))]
    return edges

def edge(v, v0, v1):
    return sd.hull()(sd.translate(list(v0))(v), sd.translate(list(v1))(v))

if __name__ == '__main__':
    fn = 64
    R = 50

    unit = 3
    v = sd.cube(unit, center=True)
    vz = [list(np.array(x)*R) for x in [[1,1,0],[1,-1,0],[-1,-1,0],[-1,1,0]]]
    vy = [list(np.array(y)*R) for y in [[1,0,1],[1,0,-1],[-1,0,-1],[-1,0,1]]]
    vx = [list(np.array(y)*R) for y in [[0,1,1],[0,1,-1],[0,-1,-1],[0,-1,1]]]

    edges = [sd.hull()(sd.translate(v0)(v), sd.translate(v1)(v)) for v0,v1 in 
             [(vx[2], vy[1]), (vy[1], vx[1]), (vx[1], vy[2]), (vy[2],vx[2])]]

    L = [vx[2],vy[1],vx[1],vy[2]]
    final = sd.union()(*path(v, L))
    L = [vx[2],vz[1],vx[3],vz[2]]
    outer = sd.union()(*[sd.rotate([i*90,0,0])(final) for i in range(4)]) \
          + sd.union()(*[sd.rotate([0, i*90,0])(final) for i in range(4)])
    R/=3
    vz = [list(np.array(x)*R) for x in [[1,1,0],[1,-1,0],[-1,-1,0],[-1,1,0]]]
    vy = [list(np.array(y)*R) for y in [[1,0,1],[1,0,-1],[-1,0,-1],[-1,0,1]]]
    vx = [list(np.array(y)*R) for y in [[0,1,1],[0,1,-1],[0,-1,-1],[0,-1,1]]]
    L = [vx[2],vy[1],vx[1],vy[2]]
    final = sd.union()(*path(v, L))
    inner = sd.union()(*[sd.rotate([i*90,0,0])(final) for i in range(4)]) \
          + sd.union()(*[sd.rotate([0, i*90,0])(final) for i in range(4)])

    final = outer + inner


    # pyramid
    R = 50
    outerp = R*np.array([[1,0,-1],[0,1,-1],[-1,0,-1],[0,-1,-1]])
    outinp = R*np.array([[1/3,0,-1],[0,1/3,-1],[-1/3,0,-1],[0,-1/3,-1]])
    outint = R*np.array([[5/6,5/6,-1/3],[5/6,1/3,-5/6],[1/3,5/6,-5/6]])
    outint = R*np.array([[3/4,3/4,-1/2],[3/4,1/2,-3/4],[1/2,3/4,-3/4]])
    outsq = R*np.array([[1,1,0],[1,0,-1],[0,1,-1]])
    innerp = outerp/3
    outer = path(v, outerp)
    inner = path(v, innerp)
    outin = path(v, outinp)
    outt = path(v, outint)
    face = outer + inner + outin + outt
    face += sd.union()(*[edge(v, v0, v1) for v0, v1 in zip(outerp, outinp)])
    face += sd.union()(*[edge(v, v0, v1) for v0, v1 in zip(outerp, innerp)])
    face += sd.union()(*[edge(v, v0, v1) for v0, v1 in zip(outint, outsq)])
    pyramid = sd.union()(*[sd.rotate([i*90,0,0])(face) for i in range(4)]) \
            + sd.union()(*[sd.rotate([0, i*90,0])(face) for i in range(4)])
    pyramid += sd.rotate([0,0,90])(pyramid)
    final = pyramid
    # final = face
    # print(L)
    # print(list(zip(L, list(np.roll(L,1)))))
    print(sd.scad_render(final, file_header=f'$fn={fn};'))

    # print(svg.scadSVG(final, fn=fn, fill='blue')) #+svg.scadSVG(image2, fn=fn, fill='lightgreen'))




