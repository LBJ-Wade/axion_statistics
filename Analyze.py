import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import (inset_axes, InsetPosition, mark_inset)
import numpy as np
import sys

run=14
#instrument="XMM"
instrument="Athena"
dof = 1747

#plt.rc('text', usetex=True)
#plt.rc('font', family='serif')

############### zero method ################
file0 = "g_chisqred_0_"+str(instrument)+"_run"+str(run)+".txt"

print "############# "+file0+" #################"

g_chisq_0meth = np.loadtxt(file0)

# Find what values of g are being used
gvals = []
for i in range(len(g_chisq_0meth)):
    gval = g_chisq_0meth[i][0]
    if not gval in gvals:
        gvals.append(gval)

# Find 5% of chisq values for each g and make histograms
chisq05 = []

print "g, 5-percentile"


for i in range(len(gvals)):
    chisqs = []
    for j in range(len(g_chisq_0meth)):
        gval = g_chisq_0meth[j][0]
        chisqval = dof*g_chisq_0meth[j][1]
        if gval == gvals[i]:
            chisqs.append(chisqval)


    # make histograms
    plt.hist(chisqs, bins='auto')
    plt.title("g = "+str(gvals[i])+"e-13")
    plt.savefig("histo_"+str(gvals[i])+"_zeromethod.pdf", bbox_inches='tight')
    plt.clf()

    # 5 percentile of chisq distribution
    chisq05val = np.percentile(chisqs,5)
    chisq05.append(chisq05val)
    # 95 percentile if g=0
    if gvals[i]==0.:
        chisq95excl_g0 = np.percentile(chisqs,95)


    print [gvals[i], chisq05val]

print chisq95excl_g0

max05 = np.amax(chisq05)
min05 = np.amin(chisq05)


# Plot g vs 5% of Delta chi^2
fig, ax1 = plt.subplots()
#plt.rc('text', usetex=True)
ax1.loglog(gvals, chisq05, 'bo', [0.5,1500])
ax1.set_xlim(0.05,150.)
ax1.set_ylim(900,110000)
ax1.axhline(y=chisq95excl_g0, color='red', linestyle='--')
ax1.set_xlabel(r'$g\, [10^{-13}\, {\rm GeV}^{-1}]$', fontsize=16)
ax1.set_ylabel('$\chi^2_0$', fontsize=18)
ax1.annotate(r'$95\% \, {\rm of}\, [\chi^2_0(g=0)]$', xy=(0.1, 1.1*chisq95excl_g0), fontsize=12, color='red')
ax2 = plt.axes([0, 0, 1, 1])
ip = InsetPosition(ax1, [0.13,0.4,0.5,0.5])
ax2.set_axes_locator(ip)
mark_inset(ax1, ax2, loc1=2, loc2=1, fc="none", ec='0.5')
ax2.loglog(gvals, chisq05, 'bo', [0.5,1500])
ax2.axhline(y=chisq95excl_g0, color='red', linestyle='--')
ax2.set_xlim(3.5,11.)
ax2.set_ylim(1200,4000)
fig.savefig(file0[:-4]+"_05percentile.pdf", bbox_inches='tight')

############### new methods ################
files = ["g_chisq_Fourier_E2weighting_"+str(instrument)+"_run"+str(run)+".txt", "g_chisq_Fit_"+str(instrument)+"_run"+str(run)+".txt"]


for file in files:

    print "############ "+file+" #############"
    
    # Read in array: g, Delta chi^2
    g_chisq = np.loadtxt(file)

    # Find what values of g are being used
    gvals = []
    for i in range(len(g_chisq)):
        gval = g_chisq[i][0]
        if not gval in gvals:
            gvals.append(gval)

    #print gvals
    #print len(g_chisq)

    # Find 95% of chisq values for each g and make histograms
    chisq05 = []
    chisq95 = []
    chisq5 = []
    null_chisq95 = 0.

    print "g, 5-percentile, 95-percentile"


    for i in range(len(gvals)):
        chisqs = []
        for j in range(len(g_chisq)):
            gval = g_chisq[j][0]
            chisqval = g_chisq[j][1]
            if gval == gvals[i]:
                chisqs.append(chisqval)

        #print(len(chisqs))

        # make histograms
        plt.hist(chisqs, bins='auto')
        plt.title("g = "+str(gvals[i])+"e-13")
        plt.savefig("histo_"+file[8:-8]+str(gvals[i])+".pdf", bbox_inches='tight')
        plt.clf()

        # Various percentiles of chisq distribution
        chisqmean = np.mean(chisqs)
        #chisqmean = np.median(chisqs)
        chisq05val = np.percentile(chisqs,5)
        chisq95val = np.percentile(chisqs,95)


        # 95% percentile for g=0, 5% percentile for g>0
        if gvals[i]==0.:
            null_chisq95 = np.percentile(chisqs,95) 

        else:
            chisq05.append(chisq05val)
            chisq95.append(chisq95val)  
            chisq5.append(chisqmean)

        print [gvals[i], chisq05val, chisq95val]

    # Remove zero for plotting purposes
    if 0.0 in gvals:
        gvals.remove(0.0)



    max95 = np.amax(chisq95)
    min95 = np.amin(chisq95)
    max05 = np.amax(chisq05)
    min05 = np.amin(chisq05)

    # Plot g vs 5% of Delta chi^2
    if file=="g_chisq_Fit_"+str(instrument)+"_run"+str(run)+".txt":
        ylimit = [5,120000]
        yname = r'$\Delta \chi^2\,{\rm Fit}$'
        insetpos = [0.13,0.45,0.5,0.5]
        xlimitzoom = [2.5,5.5]
        ylimitzoom = [9,200] 
    else:
        ylimit = [5,120000]
        yname = r'$\Delta \chi^2\,{\rm Fourier}$'
        insetpos = [0.1,0.45,0.45,0.5]
        xlimitzoom = [2.5,5.5]
        ylimitzoom = [6,200]
    
    fig, ax1 = plt.subplots()
    #plt.rc('text', usetex=True)
    ax1.loglog(gvals, chisq05, 'bo', [0.5,1500])
    ax1.set_xlim(0.05,150.)
    ax1.set_ylim(ylimit[0],ylimit[1])
    ax1.axhline(y=null_chisq95, color='red', linestyle='--')
    ax1.set_xlabel(r'$g\, [10^{-13}\, {\rm GeV}^{-1}]$', fontsize=16)
    ax1.set_ylabel(yname, fontsize=18)
    ax1.annotate(r'$95\% \, {\rm of}\, [\Delta \chi^2(g=0)]$', xy=(0.1, 1.1*null_chisq95), fontsize=12, color='red')
    ax2 = plt.axes([0, 0, 1, 1])
    ip = InsetPosition(ax1, insetpos)
    ax2.set_axes_locator(ip)
    mark_inset(ax1, ax2, loc1=2, loc2=1, fc="none", ec='0.5')
    ax2.loglog(gvals, chisq05, 'bo', [0.5,1500])
    ax2.axhline(y=null_chisq95, color='red', linestyle='--')
    ax2.set_xlim(xlimitzoom[0],xlimitzoom[1])
    ax2.set_ylim(ylimitzoom[0],ylimitzoom[1])
    fig.savefig(file[:-4]+"_05percentile.pdf", bbox_inches='tight')

