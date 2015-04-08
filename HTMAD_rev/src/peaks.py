__author__ = 'benjaminjohnson'

import numpy as np
import spectrum
#from optparse import OptionParser
#import os
#import matplotlib.pyplot as plt
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
#import subprocess
#import itertools
#import csv
#import sys

class Peaks():
    def __init__(self, *args):
        if len(args) == 1:
            found_arg = 1; arg_one = args[0]
        elif len(args) == 2:
            found_arg = 2; arg_one = args[0]

        if found_arg == 1 and isinstance(arg_one, str):
            self.initializeFromFile(arg_one)

        elif found_arg == 1 and isinstance(arg_one, spectrum.Spectrum):
            self.initializeFromSpectrumBasic(arg_one)

        elif found_arg == 2 and isinstance(arg_one, spectrum.Spectrum):
            self.initializeFromSpectrumOptimal(arg_one)
            #add error or catch here if the arguments passed in are not valid

    def initializeFromFile(self, data_location):
        print "Reading in files from the user specified location."

        inputfile = open(data_location, "r") #open the file in read
        input = inputfile.readlines()
        self._my_array_length = len(input)

        #will contain lists of all x and y values in a spectra respectively
        self._my_x_values = np.empty([self._my_array_length])  #@UndefinedVariable - Pydev gave error, but syntax works in terminal; automatically set to float type
        self._my_y_values = np.empty([self._my_array_length]) #@UndefinedVariable - Pydev gave error, but syntax works in terminal

        #              print "Read file into the program and split the file into usable lines of data (x,y)."
        index = 0
        for line in input:
            line = line.strip() #stripping off the \r\n
            sep = line.split(" ") #separating on the space to make them two elements
            intens = float(sep[1]) #indexing into each data line and taking only the intensity value (changed to a float from int)
            mass_to_charge = float(sep[0]) #grabbing the m/z value
            self._my_y_values[index] = intens #adding all the ndarray intensity values into an empty array
            self._my_x_values[index] = mass_to_charge
            index += 1
        inputfile.close()

    def initializeFromSpectrumBasic(self, spec):
        R = robjects.r

        #import rpy2.robjects.lib.MassSpecWavelet as MSW
        importr('MassSpecWavelet')    # load the package

        r_vec = robjects.FloatVector(spec.getAllY())

        peak_detection = R['peakDetectionCWT']
        myC = R['c']
        myseq = R['seq']
        scales = myC(1,myseq(2,30,2),myseq(32,64,4))
        #picking peaks on the first half of the split spectra (from 3000th to 30999th index)
        peak_info = peak_detection(r_vec, scales, 32)#the second argument is a python rewrite of the R default arguments
        major_peak_info = peak_info.rx2('majorPeakInfo')
        peak_indices = major_peak_info.rx2('peakIndex')
        for index in peak_indices:
            int(index)
        self._my_array_length = len(peak_indices)
        self._my_x_values = np.empty([self._my_array_length])  #@UndefinedVariable - Pydev gave error, but syntax works in terminal; automatically set to float type
        self._my_y_values = np.empty([self._my_array_length]) #@UndefinedVariable - Pydev gave error, but syntax works in terminal
        for i in range(self._my_array_length):
            self._my_x_values[i] = spec.getX(peak_indices[i])
            self._my_y_values[i] = spec.getY(peak_indices[i])

    def initializeFromSpectrumOptimal(self, spec):
        R = robjects.r
        #these variables are used to split the spectrum and analyze each half with different stringencies
        place_of_start = 3000
        place_of_divide = 10000
        first_stringency = 35
        second_stringency = 8
        #finds the index of the first value in the spectrum that is >= the specified start point
        index_of_start = 0
        for i in range(spec.getSize()):
            if spec.getX(i) >= place_of_start:
                index_of_start = i
                break
            #finds the index of the first value in the spectrum that is >= the specified stringency divide
        index_of_divide = 0
        for i in range(spec.getSize()):
            if spec.getX(i) >= place_of_divide:
                index_of_divide = i
                break
            #import rpy2.robjects.lib.MassSpecWavelet as MSW
        importr('MassSpecWavelet')    # load the package

        #these r vectors comprise the two halves of the spectrum, and will be passed into r separately to analyze at different stringencies
        r_vec1 = robjects.FloatVector(spec.getRangeY(index_of_start, index_of_divide-1))
        r_vec2 = robjects.FloatVector(spec.getRangeY(index_of_divide,-1))

        peak_detection = R['peakDetectionCWT']
        myC = R['c']
        myseq = R['seq']
        scales = myC(1,myseq(2,30,2),myseq(32,64,4))#this is a python rewrite of the R default arguments
        #peak picking in the first half of the spectrum
        peak_info1 = peak_detection(r_vec1, scales, first_stringency)
        major_peak_info1 = peak_info1.rx2('majorPeakInfo')
        peak_indices1 = major_peak_info1.rx2('peakIndex')
        for index in peak_indices1:
            int(index)
            #peak picking in the second half of the spectrum
        peak_info2 = peak_detection(r_vec2, scales, second_stringency)
        major_peak_info2 = peak_info2.rx2('majorPeakInfo')
        peak_indices2 = major_peak_info2.rx2('peakIndex')
        for index in peak_indices2:
            int(index)
            #initializes arrays to length needed to hold peak values
        self._my_array_length = len(peak_indices1)+len(peak_indices2)
        self._my_x_values = np.empty([self._my_array_length])
        self._my_y_values = np.empty([self._my_array_length])

        for i in range(self._my_array_length):
            if i < len(peak_indices1):
                self._my_x_values[i] = spec.getX(peak_indices1[i]+index_of_start)
                self._my_y_values[i] = spec.getY(peak_indices1[i]+index_of_start)
            else:
                self._my_x_values[i] = spec.getX(peak_indices2[i-len(peak_indices1)]+index_of_divide)
                self._my_y_values[i] = spec.getY(peak_indices2[i-len(peak_indices1)]+index_of_divide)

    def getX(self, index):
        """returns the float at index in the array of x values
        """
        return self._my_x_values[index]

    def getY(self, index):
        """returns the float at index in the array of y values
        """
        return self._my_y_values[index]

    def getAllX(self):
        """returns the entire array of x values
        """
        return self._my_x_values

    def getAllY(self):
        """returns the entire array of y values
        """
        return self._my_y_values

    def getSize(self):
        """returns size of both the x and y spectra arrays
        """
        return self._my_array_length

