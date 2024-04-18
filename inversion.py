from numpy import exp, pi, linspace
import matplotlib.pyplot as plt

θ = linspace(0, 2*pi, 200)

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
    return mobius(curve, 1, 2, 3, 4)

circles = [circle(1, 0), circle(2, 0), circle(2, 2)]
plot_curves(circles)
plot_curves([m(c) for c in circles])
