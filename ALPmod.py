#!/usr/bin/python

from heasp import *
import csv
import os, glob, sys
#sys.exit()

os.chdir("/home/rummelm/Dropbox/Axion_Statistics/xspec_fakeit/2006")

# Usable files from ALP simulation are saved in "modfiles_usable.txt"
#with open('modfiles_usable.txt') as f:
#    content = f.readlines()
#modfiles = [x.strip() for x in content] 

#for filealp in modfiles:
for filealp in glob.glob("survivalProbs_*"):

    print(filealp)

    test = table()

    # set table descriptors and the energy array
    test.ModelName = filealp[:-4]
    test.ModelUnits = " "
    test.isRedshift = False
    test.isAdditive = False
    test.isError = False

    # Import energies and conversion factors from test.tsv written by matematica file that simulate ALP conversion probablility
    # Note that the size is one greater than that of the array of model fluxes
    convfacs = []
    with open(filealp) as tsv:
        for line in csv.reader(tsv, dialect="excel-tab"):
            test.Energies.append( float(line[0]) )
            convfacs.append( float(line[1]) )

    #print convfacs
    num_lines = len(convfacs)
    #print num_lines

    test.NumIntParams = 1
    test.NumAddParams = 0

    # define first parameter and give it 11 values ranging from
    # 0.0 to 2.0 in steps of 0.2.

    testpar = tableParameter()
    testpar.Name = "param1"
    testpar.InterpolationMethod = 0
    testpar.InitialValue = 1.0
    testpar.Delta = 0.1
    testpar.Minimum = 0.0
    testpar.Bottom = 0.0
    testpar.Top = 2.0
    testpar.Maximum = 2.0

    for i in xrange(11): testpar.TabulatedValues.append(0.2*i)

    # and push it onto the vector of parameters
    test.pushParameter(testpar)

    # now set up the spectra

    testspec = tableSpectrum()

    for i1 in xrange(11):
        testspec.clear()
        testspec.ParameterValues.append(0.2*i1)
        for j in xrange(num_lines-1):
            testspec.Flux.append(0.5*(convfacs[j+1]+convfacs[j]))
        test.pushSpectrum(testspec)

    # now write out the table.
    test.write(filealp[:-4]+".mod");
