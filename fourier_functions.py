import numpy as np

def chisq(m,y,yerr):
    return sum( (y[i]-m[i])*(y[i]-m[i])/yerr[i]/yerr[i] for i in range(len(m)) )
