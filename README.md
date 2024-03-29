# svgSCAD
Build colored SVGs with units using the OpenSCAD 2D subsystem.

# Motivation
OpenSCAD can export SVGs of a 2D creation.
However, the default output is lightgray with a black border.
Furthermore, there are no units associated with the output SVG.

For laser cutting purposes, units need to be specified.
Colors can also be used to indicate etching, cutting, etc.

For SVG images, colors are part of the aesthetic.

svgSCAD tries to address both of these issues.

# Example: Yin yang
Here is the source code to build a combination yin-yang image:

https://github.com/SmoothDragon/svgSCAD/blob/cc64f2af85b35822ec5a5426c10ca0aca9ecc75b/YinYang.svg.py#L1-L24

![Yin yang](./examples/YinYang.svg)

# Example: Nested Koch snowflakes
![Nested Koch snowflakes](./examples/NestedKoch.svg)
