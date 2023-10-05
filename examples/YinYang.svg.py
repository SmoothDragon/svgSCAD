#!/usr/bin/env python

'''Yin-yang symbol created with OpenSCAD and imported to SVG with color.
Uses svgSCAD package.
'''

import solid as sd
import svgSCAD as svg

if __name__ == '__main__':
    fn = 1024
    R = 50
    r = R/6

    image = sd.circle(r=R)
    image -= svg.halfPlane('L')
    image += sd.translate([0,R/2])(sd.circle(R/2))
    image -= sd.translate([0,-R/2])(sd.circle(R/2))
    image -= sd.translate([0,R/2])(sd.circle(R/6))
    image += sd.translate([0,-R/2])(sd.circle(R/6))
    image += svg.annulus(R, R/20, 'outer')
    image2 = sd.translate([50,-50])(image)

    print(svg.scadSVG(image, fn=fn, fill='blue')+svg.scadSVG(image2, fn=fn, fill='lightgreen'))
