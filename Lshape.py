from numpy import exp, pi, linspace
import matplotlib.pyplot as plt
import numpy as np

θ = linspace(0, pi, 200)

# array of points
# Calculate the weighted mean by 
#   weight = half of the distance from each point to its predecessor and successor.
#   position = point

def w_avg(arr):
    w = arr * (np.abs(arr-np.roll(arr,1)) + np.abs(arr-np.roll(arr, -1))) /2
    return w.mean()

def Lshape(cutoff, limit):
    aline = list(np.arange(0, limit))
    aline += list(limit+1j*np.arange(0, cutoff))
    aline += list(cutoff*1j+np.arange(limit, cutoff, -1))
    aline += list(cutoff +1j*np.arange(cutoff, limit))
    aline += list(limit*1j+np.arange(cutoff, 0, -1))
    aline += list(1j*np.arange(limit, 0, -1))
    aline = np.array(aline)
    mean = aline.mean()
    aline -= mean
    radius = np.sum(np.abs(aline))/len(aline)
    aline/= radius
    return aline

def square(limit):
    aline = list(np.arange(0, limit))
    aline += list(limit+1j*np.arange(0, limit))
    aline += list(limit*1j+np.arange(limit, 0, -1))
    aline += list(1j*np.arange(limit, 0, -1))
    aline = np.array(aline)
    # mean = aline.mean()
    # aline -= mean
    # radius = np.sum(np.abs(aline))/len(aline)
    # aline/= radius
    return aline


def circle(radius, center):
    return center + radius*exp(1j*θ)



def plot_curves(curves):
    plt.axes().set_aspect(1)
    for c in curves:
        plt.plot(c.real, c.imag)
        # plt.scatter([mean.real], [mean.imag])
    plt.show()
    plt.close()

def mobius(z, a, b, c, d):
    return (a*z + b)/(c*z + d)

def m(curve):
    return mobius(curve, 0, 1, 1, 0)

circles = [circle(1, 0), circle(2, 0), circle(2, 2)]

limit = 10
cutoff = limit/2
aline = Lshape(cutoff, limit)
aline = square(limit)
plot_curves([aline])
plot_curves([m(aline)])
# print(linspace(0,10,11))
# print(np.arange(10,0,-1))
# print(dir(plt))
print(m(aline))
radius = np.sum(np.abs(aline))/len(aline)
print(radius)
aline = m(aline)
radius = np.sum(np.abs(aline))/len(aline)
print(radius)
sq = square(10)
print(w_avg(sq))
print(sq.mean())
