#!/usr/bin/env python

'''Prime radiant model
'''

import solid as sd
import numpy as np
import svgSCAD as svg
import tgd_shapes as tgd


if __name__ == '__main__':
    fn = 64
    R = 50

    unit = 20
    v = tgd.truncated_cuboctahedron(unit)
    pieces = []
    pieces.append( [[0,0,0], [-unit,0,0], [unit,0,0], [0,unit,0], [0,unit,unit]])
    pieces.append( [[0,0,0], [-unit,0,0], [unit,0,0], [0,unit,0], ])
    pieces.append( [[0,0,0], [-unit,0,0], [unit,0,0], [-unit,unit,0], ])
    pieces.append( [[0,0,0], [-unit,unit,0], [unit,0,0], [0,unit,0], [0,unit,unit]])
    pieces.append( [[0,0,0], [-unit,unit,0], [unit,0,0], [0,unit,0], [-unit,unit,unit]])
    pieces.append( [[0,0,0], [unit,0,0], [0,unit,0], [0,unit,unit]])
    
    final = sd.union()(*[sd.translate(p)(v) for p in pieces[5]])
    print(sd.scad_render(final, file_header=f'$fn={fn};'))

    # print(svg.scadSVG(final, fn=fn, fill='blue')) #+svg.scadSVG(image2, fn=fn, fill='lightgreen'))




