#!/usr/bin/env python3

from __future__ import division

import solid2 as sd
import scipy.spatial

from math import atan, sqrt
import numpy as np
from typing import *


def edgesOfFace(face):
    '''Get the edges in order for a given face
    >>> edgesOfFace([1,4,2,5,3])
    [(1, 4), (4, 2), (2, 5), (5, 3), (3, 1)]
    '''
    return [(face[i], face[(i+1)%len(face)]) for i in range(len(face))]

def orientFaces(faces, start=None):
    '''When describing a polyhedron, it can be desirable to have all faces 
    oriented in a clockwise (or counterclockwise) direction.
    >>> orientFaces([[1,2,3],[1,2,4],[1,3,4],[2,3,4]])
    [(1, 2, 3), (4, 2, 1), (1, 3, 4), (4, 3, 2)]
    '''
    faces = [tuple(face) for face in faces]
    if start is None:
        start = faces[0]
    faces.remove(start)
    oriented = [start]
    edgeDirection = {}
    for v0, v1 in edgesOfFace(start):
        edgeDirection[v0,v1] = 1
        edgeDirection[v1,v0] = -1
    while faces:
        removeFace = []
        for face in faces:
            found = None
            faceEdges = edgesOfFace(face)
            for edge in faceEdges:
                if edge in edgeDirection:
                    found = edge
                    break
            if found:
                if edgeDirection[edge] == 1:
                    oriented.append(face[::-1])
                    for v0,v1 in faceEdges:
                        edgeDirection[v0,v1] = -1
                        edgeDirection[v1,v0] = 1
                else:
                    oriented.append(face)
                    for v0,v1 in faceEdges:
                        edgeDirection[v0,v1] = 1
                        edgeDirection[v1,v0] = -1
                removeFace.append(face)
        for face in removeFace:
            faces.remove(face)
    return oriented

def openscadHull(points):
    hull = scipy.spatial.ConvexHull(points)
    points = hull.points.tolist()
    faces = hull.simplices.tolist()
    faces = orientFaces(faces)
    return sd.polyhedron(points, faces)

def helicoid(
    size=100,       # Size of squares that are stacked up to make helicoid
    height=100,     # Height of helicoid
    twist=360,      # Total rotation from bottom to top
    gap=.5,         # Distance to move away from the center z-axis
    slices=1000,    # Number of level slices to make in curve
    center=False,   # If helicoid should be centered at origin
    ):
    '''
    gap: mm that cutting edge is moved perpendicularly away from the z-axis.
        Since the horizontal gap is larger than the actual gap, a larger size is needed.
        Potential work could be done to figure out what the correlation is.
    '''
    cutShape = sd.square(size, center=True)
    cutShape = sd.translate([0,size/2+gap,0])(cutShape)
    helicoid = sd.linear_extrude(
                height=height,
                twist=twist,
                slices=slices,
                convexity=10,
                )(cutShape)
    if center:
        helicoid = sd.translate([0,0,-height/2])(helicoid)
    return helicoid

def cuboctahedron(size=50):
    '''Creates a cuboctahedron
        1) Centered at the origin
        2) Oriented as cut from a centered cube
    '''
    vertices =  [
        [1,1,0], [-1,1,0],[-1,-1,0],[1,-1,0],  # point in xy-plane
        [1,0,1], [-1,0,1],[-1,0,-1],[1,0,-1],  # point in xz-plane
        [0,1,1], [0,-1,1],[0,-1,-1],[0,1,-1],  # point in yz-plane
        ]
    shape = openscadHull(vertices)
    shape = sd.scale([size/2]*3)(shape)
    return shape

def truncated_tetrahedron(radius, top_face='edge'):
    '''Creates a truncated tetrahedron
        1) Centered at the origin
        2) Oriented as cut from a centered cube
    '''
    # edge_length is √8 and radius is √11
    vertices =  [
        [ 3,  1,  1], [ 1,  3,  1], [ 1,  1,  3],
        [-3, -1,  1], [-1, -3,  1], [-1, -1,  3],
        [-3,  1, -1], [-1,  3, -1], [-1,  1, -3],
        [ 3, -1, -1], [ 1, -3, -1], [ 1, -1, -3],
        ]
    shape = openscadHull(vertices)
    if top_face == 'triangle':
        theta = np.arctan(np.sqrt(2)/3)
        shape = sd.rotate([0,0,45])(shape)
        shape = sd.rotate([30+theta*180/np.pi, 0, 30])(shape)

    if top_face == 'hexagon':
        theta = np.arctan(np.sqrt(2)/3)
        shape = sd.rotate([0,0,45])(shape)
        shape = sd.rotate([30+theta*180/np.pi, 0, 30])(shape)
        shape = sd.rotate([0,180,0])(shape)

    shape = sd.scale([radius/np.sqrt(11)]*3)(shape)
    return shape

def rhombicosidodecahedron(size=50):
    '''Cartesian coordinates for the vertices of a rhombicosidodecahedron. 
    Edge length of 2 centered at the origin are all even permutations of:

        (±1, ±1, ±φ3),
        (±φ2, ±φ, ±2φ),
        (±(2+φ), 0, ±φ2),

        where φ = (1 + √5)/2 is the golden ratio. 

    Therefore, the circumradius of this rhombicosidodecahedron is the common distance of these points from the origin, namely √φ6+2 = √8φ+7 for edge length 2. For unit edge length, R must be halved, giving

        R = √(8φ+7)/2 = √(11+4√5)/2 ≈ 2.233.
    '''
    phi = (1+np.sqrt(5))/2
    basis = [
             [1, 1, phi**3],
             [phi**2, phi, 2*phi],
             [2+phi, 0, phi**2],
            ]
    vertices =  [
        [ 3,  1,  1], [ 1,  3,  1], [ 1,  1,  3],
        [-3, -1,  1], [-1, -3,  1], [-1, -1,  3],
        [-3,  1, -1], [-1,  3, -1], [-1,  1, -3],
        [ 3, -1, -1], [ 1, -3, -1], [ 1, -1, -3],
        ]
    shape = openscadHull(vertices)
    shape = sd.scale([size/2]*3)(shape)
    return shape

def torus(hole_diameter=20, arm_diameter=20):
    shape = sd.circle(d=arm_diameter)
    shape = sd.translate([(hole_diameter+arm_diameter)/2, 0, 0])(shape)
    carving = sd.rotate_extrude()(shape)
    return carving

def thickPath(r:float, xy:List[complex]):
    dot = sd.circle(r)
    dots = [sd.translate([v.real,v.imag])(dot) for v in xy]
    edges = [sd.hull()(v,w) for v,w in zip(dots[:-1],dots[1:])]
    path = sd.union()(*edges)
    return path

def beveled_square(diameter, base, center=True):
    '''Each corner of the square is beveled at a 45 degree angle
    diameter: side to side distance of octagon
    base: length of bottom rectilinear flat side 0 < base < diameter
    base == 0 => square diamond
    base == diameter => square
    '''
    # TODO: make points from parameters
    x = diameter/2
    y = base/2
    points = [ (x,y), (y,x), (-y,x), (-x,y), (-x,-y), (-y,-x), (y,-x), (x,-y) ]
    shape = polygon(points=points)
    return shape

def beveled_box(length, diameter, base, beveled_end=True, center=False):
    '''Octogon shaped segment
    Ends are cut so that two rods can be joined at 90 degrees
    length: X-direction
    diameter: Y-direction
    diameter: Z-direction
    Will be placed in the same location as cube([X,Y,Z])
    center: Positions beveled_box with respect to origin identically to cube()
    '''
    shape = beveled_square(diameter=diameter, base=base)
    rod = linear_extrude(height=length, center=True, convexity=10, twist=0)(shape)
    if beveled_end:
        cut_length = (length + base)/sqrt(2)
        cut_block = rotate([45,0,0])(cube(cut_length, center=True))
        rod = intersection()(rod, cut_block, rotate([0,0,90])(cut_block))
    final = rotate([0,90,0])(rod)  # lay in XY plane
    if not center:
        final = translate([length/2, diameter/2, diameter/2])(final)
    return final

# Useful 2D functions

def inverseSierpinskiGasket(size=50, iterations=3):
    figure = sd.square(1, center=True)
    shifts = [(i-1, j-1) for i in range(3) for j in range(3)]
    shifts.remove( (0,0) )
    for _ in range(iterations):
        scaledFigure = sd.scale([1/3, 1/3, 1])(figure)
        squares = [sd.translate(shift)(scaledFigure) for shift in shifts]
        figure = sd.union()(figure, *squares)
    figure = sd.scale([size/2, size/2, 1])(figure)
    return figure

def halfPlane(direction, D=1000):
    r'''Create a 2D half plane. Choose D large enough to be "infinity".
    Quadrants like 'NE' are allowed.
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
    # plane = sd.translate(planetype[direction])(plane)
    plane = sd.intersection()(*[sd.translate(planetype[d])(plane) for d in direction])
    return plane

def sector(angle, r=0, D=1000):
    R = r/np.tan(angle/2/360*np.pi)/2
    piece = halfPlane('U', D=D)
    if r>0:
        piece -= sd.circle(R)
    piece = sd.intersection()(piece, sd.rotate([0,0,angle-180])(piece))
    if r>0:
        piece += sd.translate([R,r])(sd.circle(r))
    return piece

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

def hexagram(R):
    wedge = sd.circle(R, segments=3)
    wedge += sd.rotate([0,0,180])(wedge),
    return wedge

def dcos(angle):
    '''Cosine function based on degrees.
    '''
    return np.cos(angle/180*np.pi)

def dsin(angle):
    '''Sine function based on degrees.
    '''
    return np.sin(angle/180*np.pi)

def tiara_loop(r=5, w=3):
    fn = 64
    deg_switch = 5  # Degrees beyond half plane to change arc
    mul_r = 8  # relative ratio difference between two arcs
    top = annulus(r, w, position='outer')
    top &= halfPlane('N')
    top += sd.rotate(deg_switch)(top) & halfPlane('S')
    top += sd.rotate(-deg_switch)(top) & halfPlane('S')
    bottom = annulus(mul_r*r, w, position='outer')
    bottom &= (halfPlane('SE'))
    bottom &= sd.rotate(-deg_switch)(halfPlane('SE'))
    bottom &= sd.rotate(45)(halfPlane('SE'))
    bottom = sd.translate([-dcos(deg_switch)*(mul_r-1)*r, dsin(deg_switch)*(mul_r-1)*r])(bottom)
    bottom += sd.mirror([1,0])(bottom)
    final = top + bottom
    final = sd.translate([0,dcos(45)*mul_r*r])(final)
    # final += sd.translate([0,37])(sd.square(3,center=True))
    final -= sd.translate([3,36])(sd.square([.35,3],center=True))
    final -= sd.translate([-3,36])(sd.square([.35,3],center=True))
    diag = sd.rotate(45)(sd.square([.35,2.2],center=True))
    diag += sd.rotate(135)(sd.square([.7,1],center=False))
    diag = sd.translate([-5.6,18])(diag)
    final -= diag
    final -= sd.mirror([1,0])(diag)
    return final

def tiara_band():
    shift = 13
    loop = tiara_loop()
    final = sd.union()(*[sd.translate([i*shift,0])(loop) for i in range(-4,5)])
    final += sd.square([9*shift+5, shift/2], center=True)
    return final

def flat2cylinder(obj2d, w_obj, h_obj=1000, r=100, thickness=3, segments=64):
    '''Take a 2D object of width w and project it onto half a cylinder.
    '''
    theta=90/segments
    section = annulus(r, thickness, position='outer')
    section &= sector(angle=2*theta)
    section = sd.rotate(-theta)(section)
    section = sd.linear_extrude(1000, center=True)(section)
    w_section = 2*r*dsin(theta)
    # return section

    obj_scale = w_section*segments/w_obj
    obj2d = sd.scale(obj_scale)(obj2d)
    extrude = sd.linear_extrude(r+thickness)(obj2d)
    extrude = sd.rotate([90,0,90])(extrude)
    extrude = sd.translate([0,-w_section/2,0])(extrude)
    # return extrude
    final = sd.union()(*[sd.rotate([0,0,(2*i+1)*theta])(section & sd.translate([0,-i*w_section,0])(extrude)) for i in range(segments)])
    return final

def wire_guide():
    guide = sd.cube([3.9,3,2],center=True)
    guide += sd.cube([2,3,4],center=True)
    guide = sd.hull()(guide)
    guide -= sd.cube([5,.35,5], center=True)
    guide -= sd.cube([3,1.5,5], center=True)
    return guide

def back_fins():
    h=17
    fins = sd.cylinder(r=103, h=h, center=True)
    fins -= sd.cylinder(r=100, h=h+1, center=True)
    fins -= sd.rotate([0,0,-45])(sd.translate([500,-500,0])(sd.cube(1000,center=True)))
    end = sd.cylinder(d=17, h=3)
    end &= (sd.translate([500,0,0])(sd.cube(1000,center=True)))
    end = sd.rotate([90,0,0])(end)
    end = sd.translate([0,-100,0])(end)
    end = sd.rotate([0,0,-45])(end)
    fins += end
    fins += sd.mirror([1,0,0])(end)
    return fins

if __name__ == '__main__':
    fn = 256
    band = tiara_band()
    band = sd.translate([(9*13+5)/2,0])(band)
    final = flat2cylinder(band, 9*13+5, segments = 100)
    guide = wire_guide()
    # guide = sd.translate([101,0,85])(guide)
    guide = sd.translate([101,0,75])(guide)
    # guide = sd.rotate([0,0,22.85])(guide)
    guide = sd.union()(*[sd.rotate([0,0,22.85+i*19.18])(guide) for i in range(-1,9)])
    final += guide
    final += back_fins()
    final = sd.scale(.7)(final)
    final = sd.scad_render(final, file_header=f'$fn={fn};')
    print(final)
