import skrf as rf
import numpy as np
from matplotlib import pyplot

# Input: Write Z as a complex impedance
Z = 25 + 100 * 1j
Z0 = 50  #Characteristic Impedance



def plotComplexImpedanceOnSmith(z,z0):
    # Simple function to plot single impedances on the smith chart
    
    s1 = ((z/z0) - 1) / ((z/z0) + 1)
    s = np.ones(3) * s1
    freq = rf.Frequency(1,2,3) # Arbitrary Frequency
    obj = rf.Network(frequency = freq, s = s, z0 = 50)
    obj.plot_s_smith(draw_labels=True, marker = 'o',show_legend=False)

    pyplot.show()

plotComplexImpedanceOnSmith(Z, Z0)