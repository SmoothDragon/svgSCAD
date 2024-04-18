#!/usr/bin/env python

'''Prime radiant model
'''

import solid2 as sd
import numpy as np
import svgSCAD as svg
import tgd_shapes as tgd


if __name__ == '__main__':
    fn = 64
    R = 50

    unit = 20
    v = tgd.truncated_cuboctahedron(unit)
    v = tgd.cuboctahedron(unit)
    pieces = []
    pieces.append( [[0,0,0], [-unit,0,0], [unit,0,0], [0,unit,0], [0,unit,unit]])
    pieces.append( [[0,0,0], [-unit,0,0], [unit,0,0], [0,unit,0], ])
    pieces.append( [[0,0,0], [-unit,0,0], [unit,0,0], [-unit,unit,0], ])
    pieces.append( [[0,0,0], [-unit,unit,0], [unit,0,0], [0,unit,0], [0,unit,unit]])
    pieces.append( [[0,0,0], [-unit,unit,0], [unit,unit,0], [0,unit,0], [-unit,unit,unit]])
    pieces.append( [[0,0,0], [unit,0,0], [0,unit,0], [0,unit,unit]])
    
    pieces = [sd.union()(*[sd.translate(p)(v) for p in piece]) for piece in pieces]
    # final = sd.union()(*[sd.translate(p)(v) for p in pieces[5]])
    final = pieces[0]
    final += sd.translate([3*unit,unit,0])(sd.rotate([0,0,180])(pieces[1]))
    final += sd.translate([-3*unit,unit,0])(sd.rotate([180,0,0])(pieces[2]))
    final += sd.translate([-3*unit,3*unit,0])(sd.rotate([0,0,0])(pieces[3]))
    final += sd.translate([0,3*unit,0])(sd.rotate([0,0,0])(pieces[4]))
    final += sd.translate([3*unit,3*unit,0])(sd.rotate([0,0,0])(pieces[5]))
    # final += sd.translate([3*unit,unit,0])(pieces[1])
    print(sd.scad_render(final, file_header=f'$fn={fn};'))

    # print(svg.scadSVG(final, fn=fn, fill='blue')) #+svg.scadSVG(image2, fn=fn, fill='lightgreen'))




