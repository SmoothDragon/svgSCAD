from numpy import exp, pi, linspace
import matplotlib.pyplot as plt

θ = linspace(0, pi, 200)

line = linspace(-1,1,200)
line1 = 1 + 1j*line
line2 = line + 1j 
line3 = -1 + 1j*line
line4 = line - 1j 

def circle(radius, center):
    return center + radius*exp(1j*θ)



def plot_curves(curves):
    plt.axes().set_aspect(1)
    for c in curves:
        plt.plot(c.real, c.imag)
    plt.show()
    plt.close()

def mobius(z, a, b, c, d):
    return (a*z + b)/(c*z + d)

def m(curve):
    return mobius(curve, 0, 1, 1, 0)

circles = [circle(1, 0), circle(2, 0), circle(2, 2)]
lines = [line1, line2, line3, line4]
half1 = circle(1,0) + 1j
half2 = 1j * half1
half3 = 1j * half2
half4 = 1j * half3
half = [half1, half2, half3, half4]

# plot_curves(circles)
plot_curves(lines)
# plot_curves([m(c) for c in circles])
plot_curves([m(c) for c in lines]+half)
plot_curves([m(m(c)) for c in lines])
print(sum(sum(l for l in half)))
