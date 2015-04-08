__author__ = 'benjaminjohnson'

import numpy as np
#import os

class Spectrum:
    def __init__(self, data_location):
        inputfile = open(data_location, "r") #open the file in read
        input = inputfile.readlines()
        self._my_array_length = len(input)

        #will contain lists of all x and y values in a spectra respectively
        self._my_x_values = np.empty([self._my_array_length])  #@UndefinedVariable - Pydev gave error, but syntax works in terminal; automatically set to float type
        self._my_y_values = np.empty([self._my_array_length]) #@UndefinedVariable - Pydev gave error, but syntax works in terminal
        index = 0
        for line in input:
            line = line.strip() #stripping off the \r\n
            sep = line.split(" ") #separating on the space to make them two elements
            intens = float(sep[1]) #indexing into each data line and taking only the intensity value (changed to a float from int)
            mass_to_charge = float(sep[0]) #grabbing the m/z value
            #when we build sample class, take into account flat-line samples and how to skip them?
            if intens == 0: #checking for an automated run flat-line (ie all y-values will be zeros)
                print "Skipping " + str(file) + " because it is a flat-line spectrum."
                break
            else:
                self._my_y_values[index] = intens #appending all the ndarray intensity values into an empty list so each file is a list of lists
                self._my_x_values[index] = mass_to_charge
                index += 1
        inputfile.close()

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

    def getRangeX(self, start, end):
        """returns array containing values indicated by index range, including last index
        """
        if end == -1:
            return self._my_x_values[start:]
        return self._my_x_values[start:end+1]

    def getRangeY(self, start, end):
        """returns array containing values indicated by index range, including last index
        """
        if end == -1:
            return self._my_y_values[start:]
        return self._my_y_values[start:end+1]