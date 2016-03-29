import skrf as rf
import numpy as np
import math
from matplotlib import pyplot
from matplotlib import animation
from numpy.core.function_base import linspace
import time

# Input: Write Z as a complex impedance
Z = 25 + 100 * 1j
Z0 = 50  #Characteristic Impedance

def getElectricalDelay(z,z0):
    #Gets the shortest electrical delay to get a purely resistive impedance
    
    #First convert impedance to S Parameter (or reflection coefficient)
    s1 = ((z/z0) - 1) / ((z/z0) + 1)
    s1Angle = np.angle(s1, deg=True)
    a = 180 - s1Angle
    b = 0 - s1Angle
    if a < b :
        ang = a
    else:
        ang = b
    print("Angle is:")
    print(s1Angle)
    print("Shortest Delay in Degrees: ")
    print(ang)
    
    return ang
    
def plotComplexImpedanceOnSmith(z,z0):
    # Simple function to plot single impedances on the smith chart
    
    s1 = ((z/z0) - 1) / ((z/z0) + 1)
    s = np.ones(3) * s1
    freq = rf.Frequency(1,2,3) # Arbitrary Frequency
    obj = rf.Network(frequency = freq, s = s, z0 = 50)
    obj.plot_s_smith(draw_labels=True, marker = 'o',show_legend=False,
                     color = "r")
    #pyplot.show()
       
def plotImpedanceAfterDelay(z,z0):
    # Simple function to plot single impedances on the smith chart
    
    # Convert to s parameters
    s1 = ((z/z0) - 1) / ((z/z0) + 1)
    ang = getElectricalDelay(z, z0)
    s1 = s1 * np.exp((math.pi /180) * ang * 1j )
    s = np.ones(3) * s1
    freq = rf.Frequency(1,2,3) # Arbitrary Frequency
    obj = rf.Network(frequency = freq, s = s, z0 = 50)
    
    obj.plot_s_smith(draw_labels=True, marker = 'o',show_legend=False, 
                     color = "r")
    #pyplot.show()
    
plotComplexImpedanceOnSmith(Z,Z0) 
plotImpedanceAfterDelay(Z, Z0)
totalIter = 200
# Create object so we don't have to keep recreating it
s1 = ((Z/Z0) - 1) / ((Z/Z0) + 1)
freq = rf.Frequency(1,2,3) # Arbitrary Frequency
obj = rf.Network(frequency = freq, s = s1, z0 = 50)

def plotDelayAnimation(i):
    
    #print(i)
    i = i + 1
    freq = obj.frequency
    freq._f = np.linspace(1, i, i)
    obj.frequency = freq
    ang = getElectricalDelay(Z, Z0)
    s = np.ones(i,dtype=np.complex)
    for n in range(1, i+1):
        angMul = (ang / totalIter) * n 
        s[n-1] =  s1 * np.exp((np.pi /180) * angMul * 1j ) + 0j
        
    obj.s = s
    
    obj.plot_s_smith(draw_labels=True,show_legend=False,
                     color = "r")
     
current_figure = pyplot.gcf()
anim = animation.FuncAnimation(current_figure, plotDelayAnimation, 
                               frames = totalIter,interval = 10)
#pyplot.show()
Writer = animation.writers['ffmpeg']
writer = Writer(fps=30, metadata=dict(artist='Eric Perez'), bitrate=1800)

anim.save('im.mp4', writer=writer)

