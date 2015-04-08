__author__ = 'benjaminjohnson'

import spectrum
import peaks
import matplotlib.pyplot as plt

class Sample:
    def __init__(self, filename, run_type = "F", peak_picking_type = "B"):

        self._my_name = filename.split("/")[-1].split(".")[0]
        self._my_sequence = []

        if run_type.upper() == "F":
            self._my_spectrum = spectrum.Spectrum(filename)
            if peak_picking_type.upper() == "O":
                self._my_peaks = peaks.Peaks(self._my_spectrum, 23)#placeholder for tuple with optimal data
            elif peak_picking_type.upper() == "B":
                self._my_peaks = peaks.Peaks(self._my_spectrum)
                #add else statement with error catches later

        elif run_type.upper() == "A":
            self._my_spectrum = None
            self._my_peaks = peaks.Peaks(filename)
            #add else statement with error catches later

    def loadSequence(self, seq):
        """takes a list of the binary pseudonucleotide sequence and
        saves it into self._my_sequence
        """
        self._my_sequence = seq

    def getSpectrum(self):
        """returns the sample spectrum of type Spectrum
        """
        return self._my_spectrum

    def getPeaks(self):
        """returns the sample peaks of type Peaks
        """
        return self._my_peaks

    def getName(self):
        """returns the sample Name of type string
        """
        return self._my_name

    def getSequence(self):
        """returns the sample binary pseudonucleotide sequence
        of type list
        """
        return self._my_sequence

    def graphSpectrum(self, directory_path, line_color = "b", peak_color = "r", resolution = 300):
        """
        The method graphs the spectrum and the picked peaks
        ------------
        optional arguments to pass are the colors for the lines and peaks
        plotted. Color codes are red = 'r', yellow = 'y', green = 'g',
        blue = 'b', cyan = 'c', magenta = 'm', black = 'k', white = 'w'
        resolution of the graph can also be specified by a number from 1 to 1000

        """
        #plotting only the picked peaks as dots, peak+shape = color and shape, ms is the size and alpha is the transparency
        peak_shape = peak_color.lower() + 'o'
        plot_picked_peaks = plt.plot(self._my_peaks.getAllX(), self._my_peaks.getAllY(), peak_shape, ms = 5.0, alpha = 0.5)
        plot_spectra = plt.plot(self._my_sequence.getAllX(), self._my_sequence.getAllX())  #ploting the spectra on which the peaks will appear
        plt.setp(plot_spectra, linewidth=0.2, color = line_color)
        plt.xlim(self._my_spectrum.getX(0), self._my_spectrum.getX(-1))   #setting the x-axis to span from the x min to x max

        plt.xlabel("m/z")
        plt.ylabel("Intensity [arbitrary units]")
        plt.legend((plot_spectra, plot_picked_peaks), ("Processed spectrum", "Picked peaks"), loc = 1)
        spotname = "picked peaks of " + self._my_name
        plt.title(spotname)
        filename = spotname + ".png"
        outfile = open(directory_path + "/" + filename, "w")
        plt.savefig(directory_path + "/" + filename, dpi=resolution)
        outfile.close()
        plt.clf()   #clears the graph. without the first plot will stay on the graph and be plotted with the next spectra and so fourth
