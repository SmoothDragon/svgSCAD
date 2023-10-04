#!/usr/bin/env python3

import solid as sd

def halfPlane(direction, D=1000):
    r'''Create a 2D half plane. Choose D large enough to be "infinity".
    >>> sd.scad_render(halfPlane('N'))
    '\n\ntranslate(v = [0, 1000]) {\n\tsquare(center = true, size = 2000);\n}'
    '''
    planetype = {
        'N':( 0,  D),
        'S':( 0, -D),
        'E':( D,  0),
        'W':(-D,  0),
        'U':( 0,  D),
        'D':( 0, -D),
        'R':( D,  0),
        'L':(-D,  0),
        }
    plane = sd.square(2*D, center=True)
    plane = sd.translate(planetype[direction])(plane)
    return plane

def annulus(R, w, position='center'):
    '''Annulus or radius R with line of width w centered on perimeter
    '''
    linetype = {
        'center': (R+w/2, R-w/2),
        'inner': (R, R-w),
        'outer': (R+w, R),
        }
    R_outer, R_inner = linetype[position]
    figure = sd.circle(R_outer)
    figure -= sd.circle(R_inner)
    return figure

if __name__ == '__main__':
    import doctest
    doctest.testmod()
