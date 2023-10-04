#!/usr/bin/env python

import solid as sd
import numpy as np
import XYtools as xy
import tempfile
import subprocess
import shlex


class scadSVG:
    def __init__(self, scad_obj, stroke=None, fill=None, strokewidth=None):
        temp_scad = tempfile.NamedTemporaryFile(delete=True)
        temp_svg = tempfile.NamedTemporaryFile(delete=True)

        sd.scad_render_to_file(obj, filepath=temp_scad.name, file_header=f'$fn={fn};')
        temp_scad.flush()
        command = f'openscad --export-format=svg {temp_scad.name} -o {temp_svg.name}'
        subprocess.run(shlex.split(command))
        with open(temp_svg.name) as infile:
            svglist = [line for line in infile]
        svg = scadsvginfo(svglist, stroke, fill, strokewidth)
        svg['path'] = svglist[4:-2]

    def __add__(self, other):
        pass

    def __str__(self):
        pass

def scadsvginfo(svg, stroke=None, fill=None, strokewidth=None):
    line = svg[2].split()
    xmin = float(line[3][9:])
    ymin = float(line[4])
    width = float(line[5])
    height = float(line[6][:-1])
    line = svg[-2].split()
    stroke = line[1][8:-1] if stroke is None else stroke
    fill = line[2][6:-1] if fill is None else fill
    strokewidth = float(line[3][14:-3]) if strokewidth is None else strokewidth
    return {
        'xmin':xmin,
        'ymin':ymin,
        'xmax':xmin+width,
        'ymax':ymin+height,
        'width':width,
        'height':height,
        'stroke':stroke,
        'fill':fill,
        'stroke-width':strokewidth,
        }

def scad2svg(obj, stroke=None, fill=None, strokewidth=None):
    temp_scad = tempfile.NamedTemporaryFile(delete=True)
    temp_svg = tempfile.NamedTemporaryFile(delete=True)

    sd.scad_render_to_file(obj, filepath=temp_scad.name, file_header=f'$fn={fn};')
    temp_scad.flush()
    command = f'openscad --export-format=svg {temp_scad.name} -o {temp_svg.name}'
    subprocess.run(shlex.split(command))
    with open(temp_svg.name) as infile:
        svglist = [line for line in infile]
    svg = scadsvginfo(svglist, stroke, fill, strokewidth)
    svg['path'] = svglist[4:-2]
    return svg

def scadsvg2string(svg):
    width = svg['width']
    height = svg['height']
    xmin = svg['xmin']
    ymin = svg['ymin']
    intro = [
        '<?xml version="1.0" standalone="no"?>',
        '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">',
        f'<svg width="{width}mm" height="{height}mm" viewBox="{xmin} {ymin} {width} {height}" xmlns="http://www.w3.org/2000/svg" version="1.1">',
        ]
    intro += svg['path']
    stroke = svg['stroke']
    fill = svg['fill']
    strokewidth = svg['stroke-width']
    intro.append(f'" stroke="{stroke}" fill="{fill}" stroke-width="{strokewidth}"/>')
    intro.append('</svg>')
    return '\n'.join(intro)

fn = 1024
R = 50
r = R/6

image = sd.circle(r=R)
image -= xy.halfPlane('L')
image += sd.translate([0,R/2])(sd.circle(R/2))
image -= sd.translate([0,-R/2])(sd.circle(R/2))
image -= sd.translate([0,R/2])(sd.circle(R/6))
image += sd.translate([0,-R/2])(sd.circle(R/6))
image += xy.annulus(R, R/20, 'outer')

svg = scad2svg(image, fill='green')
print(scadsvg2string(svg))

'''
<?xml version="1.0" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="106mm" height="106mm" viewBox="-53 -53 106 106" xmlns="http://www.w3.org/2000/svg" version="1.1">
<title>OpenSCAD Model</title>
['"', 'stroke="black"', 'fill="lightgray"', 'stroke-width="0.5"/>']

'''
