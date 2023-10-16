#!/usr/bin/env python3

from __future__ import division

import solid
import scipy.spatial

from solid.utils import degrees
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
    return solid.polyhedron(points, faces)

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
    cutShape = solid.square(size, center=True)
    cutShape = solid.translate([0,size/2+gap,0])(cutShape)
    helicoid = solid.linear_extrude(
                height=height,
                twist=twist,
                slices=slices,
                convexity=10,
                )(cutShape)
    if center:
        helicoid = solid.translate([0,0,-height/2])(helicoid)
    return helicoid


def inverseSierpinskiGasket(size=50, iterations=3):
    figure = solid.square(1, center=True)
    shifts = [(i-1, j-1) for i in range(3) for j in range(3)]
    shifts.remove( (0,0) )
    for _ in range(iterations):
        scaledFigure = solid.scale([1/3, 1/3, 1])(figure)
        squares = [solid.translate(shift)(scaledFigure) for shift in shifts]
        figure = solid.union()(figure, *squares)
    figure = solid.scale([size/2, size/2, 1])(figure)
    return figure

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
    shape = solid.scale([size/2]*3)(shape)
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
        shape = solid.rotate([0,0,45])(shape)
        shape = solid.rotate([30+theta*180/np.pi, 0, 30])(shape)

    if top_face == 'hexagon':
        theta = np.arctan(np.sqrt(2)/3)
        shape = solid.rotate([0,0,45])(shape)
        shape = solid.rotate([30+theta*180/np.pi, 0, 30])(shape)
        shape = solid.rotate([0,180,0])(shape)

    shape = solid.scale([radius/np.sqrt(11)]*3)(shape)
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
    shape = solid.scale([size/2]*3)(shape)
    return shape

def torus(hole_diameter=20, arm_diameter=20):
    shape = solid.circle(d=arm_diameter)
    shape = solid.translate([(hole_diameter+arm_diameter)/2, 0, 0])(shape)
    carving = solid.rotate_extrude()(shape)
    return carving

def thickPath(r:float, xy:List[complex]):
    dot = solid.circle(r)
    dots = [solid.translate([v.real,v.imag])(dot) for v in xy]
    edges = [solid.hull()(v,w) for v,w in zip(dots[:-1],dots[1:])]
    path = solid.union()(*edges)
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

if __name__ == '__main__':
    arm_diameter=20
    hole_diameter=20
    cross_twist = 0
    cut_extend = 1
    shape = inverseSierpinskiGasket()
    shape = cuboctahedron()
    shape = torus()
    shape = helicoid()
    cutter = helicoid(height=arm_diameter+2*cut_extend, twist=cross_twist, gap=-.5)
    cutter = solid.intersection()(
                cutter,
                solid.rotate([0,0,90])(cutter),
                )
    cutter = solid.union()(
                cutter,
                solid.rotate([0,0,180])(cutter),
                )
    cutter = solid.rotate([0,0,45+cross_twist/2])(cutter)
    cutter = solid.translate([0,0,hole_diameter/2-cut_extend])(cutter)
    carving = solid.rotate([0,90,0])(torus())
    shape = solid.union()(cutter(), carving())
    shape = solid.difference()(carving(), cutter())

    print(solid.scad_render(shape))
