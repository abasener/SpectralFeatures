import spectral
import spectral.io.envi as envi
from matplotlib import pyplot as plt
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.text as mtext
import matplotlib.transforms as mtransforms

class aplot:
    def __init__ (self, wl,spec, name, type = "veg", h= 8, w = 20, LineColor=[],LineName=[],LineNM=[],LineAll=[],LineFound=[],ShadeName=[],ShadeColor=[],ShadeStart=[],ShadeStop=[]):
    # Parameters:
    # - wl: Array of wavelengths corresponding to the spectral data.
    # - spec: Array of reflectance values corresponding to the spectral data.
    # - name: Name or label associated with the spectral data.
    # - type: Type of data (default is "veg" for vegetation).
    # - h: Height of the plot figure in inches (default is 8).
    # - w: Width of the plot figure in inches (default is 20).
    # - LineColor: List of colors for vertical lines to be added to the plot.
    # - LineName: List indicating whether to include chemical names in annotations for each line (1 for include, 0 for exclude).
    # - LineNM: List indicating whether to include wavelength (WL) in annotations for each line (1 for include, 0 for exclude).
    # - LineAll: List indicating whether to use all possible features or only those flagged as important in the file (1 for all, 0 for flagged).
    # - LineFound: List indicating whether to plot only lines that match the feature find criteria (1 for plot, 0 for all).
    # - ShadeName: List of names or labels for shaded regions to be added to the plot.
    # - ShadeColor: List of colors for shaded regions.
    # - ShadeStart: List of starting wavelengths for each shaded region.
    # - ShadeStop: List of stopping wavelengths for each shaded region.
        self.spec = spec
        self.wl = wl
        self.type = type
        self.h = h
        self.w = w
        self.name = name
        # Read data lines
        self.read_lines()
        # Make plot
        self.make_plot()

        # Add shade
        # Determine the minimum length of ShadeStart and ShadeStop lists
        min_length = min(len(ShadeStart), len(ShadeStop))
        for n in range(min_length):
            args = {}
            if n < len(ShadeName) and ShadeName:  # Check if ShadeName has an element at index n and is not empty
                args['name'] = ShadeName[n]
            if n < len(ShadeColor) and ShadeColor:  # Check if ShadeColor has an element at index n and is not empty
                args['color'] = ShadeColor[n]
            if n < len(ShadeStart) and ShadeStart:  # Check if ShadeStart has an element at index n and is not empty
                args['start'] = ShadeStart[n]
            if n < len(ShadeStop) and ShadeStop:  # Check if ShadeStop has an element at index n and is not empty
                args['stop'] = ShadeStop[n]
            # Call self.add_shade with the arguments that are not empty
            if args:
                self.add_shade(**args)
            #Example call: ShadeName=["Red Edge"],ShadeColor=["red"],ShadeStart=[650,1375,1880],ShadeStop=[750,1500]

        # Add lines
        # Determine the maximum length of LineName, LineNM, LineAll, LineFound, and LineColor lists
        max_length = max(len(LineName), len(LineNM), len(LineAll), len(LineFound),len(LineColor))
        for n in range(max_length):
            args = {}
            #    n = n-2
            if n < len(LineName) and LineName:  # Check if LineName has an element at index n and is not empty
                args['nameBool'] = LineName[n]
            if n < len(LineNM) and LineNM:  # Check if LineNM has an element at index n and is not empty
                args['nmBool'] = LineNM[n]
            if n < len(LineAll) and LineAll:  # Check if LineAll has an element at index n and is not empty
                args['allBool'] = LineAll[n]
            if n < len(LineFound) and LineFound:  # Check if LineFound has an element at index n and is not empty
                args['foundBool'] = LineFound[n]
            if n < len(LineColor) and LineColor:  # Check if LineColor has an element at index n and is not empty
                args['color'] = LineColor[n]
            # Call self.add_lines with the arguments that are not empty
            if args:
                self.add_lines(**args)
            #Example call: LineColor=["green","red"],LineFound=[1,0],LineAll=[1,1],LineNM=[1,0],LineName=[1,1]
        # Plot 
        plt.show()
        
    def read_lines(self):
        if self.type == "veg":
            file_path = 'Veg1.xlsx'
        self.dfL = pd.read_excel(file_path)

    def make_plot(self):
        plt.figure(figsize=(self.w, self.h))
        plt.plot(self.wl, self.spec, label=self.name, linewidth=0.75)
        plt.xlabel('Wavelength (nm)', fontsize=12)
        plt.ylabel('Reflectance', fontsize=12)

        # Calculate the range of wavelengths
        min_wavelength = np.min(self.wl)
        max_wavelength = np.max(self.wl)

        # Set major and minor ticks for the x-axis
        major_ticks = np.arange(np.ceil(min_wavelength / 500) * 500, max_wavelength + 500, 500)
        minor_ticks = np.arange(np.ceil(min_wavelength / 100) * 100, max_wavelength + 100, 100)

        plt.xticks(major_ticks)
        plt.gca().set_xticks(minor_ticks, minor=True)

        # Set grid lines
        plt.grid(True, which='major', axis='both', linestyle='-', linewidth=0.5, color='gray')  # Darker grid every 500 nm
        plt.grid(True, which='minor', axis='x', linestyle='--', linewidth=0.25, color='grey')  # Lighter grid every 100 nm

        plt.title('Reflectance Spectra for Vegetation', fontsize=20)
        plt.legend(bbox_to_anchor=(0, -0.1), loc='upper left', ncol=4)
        plt.xlim(min_wavelength, max_wavelength)

    def add_lines(self,color="green",nameBool=1,nmBool=0,allBool=1,foundBool=1,LineSize=0.05,fontSize=10):
    # Parameters for add_lines function:
    # - color: Color of the vertical lines to be added to the plot (default is "green").
    # - nameBool: Flag indicating whether to include chemical names in annotations above the lines (1 for include, 0 for exclude).
    # - nmBool: Flag indicating whether to include wavelength (WL) in annotations (1 for include, 0 for exclude).
    # - allBool: Flag indicating whether to use all possible features or only those flagged as important in the data file (1 for all, 0 for flagged).
    # - foundBool: Flag indicating whether to plot only lines that match the feature find criteria (1 for plot, 0 for all).
    # - LineSize: Size of the vertical lines relative to the plot dimensions (default is 0.05).
    # - fontSize: Font size of annotations (default is 10).
        ymin, ymax = plt.ylim()
        dif = ymax - ymin  # Calculate the difference between maximum and minimum y-axis values
        adjP = (0.8 / dif)  # Adjust parameter relative to y-axis range
        adjF = 0.01 * dif  # Adjust factor relative to y-axis range
        LineSize = LineSize * dif  # Scale line size relative to y-axis range
        for index, row in self.dfL.iterrows():
            if row['Bool'] == 1 or allBool == 1:
                # Find the index of closest wavelength in centers_np to row['WL']
                idx = np.abs(np.array(self.wl) - row['WL']).argmin()
                y_value = self.spec[idx]  # Access the spectrum directly

                # Calculate the average reflectance value within the range
                average_reflectanceR = np.mean(self.spec[idx:idx + 35])
                average_reflectanceL = np.mean(self.spec[idx - 35:idx])

                # Compare y_value with the average_reflectance1
                if y_value < average_reflectanceR and y_value < average_reflectanceL and foundBool == 1 or foundBool == 0:
                    # Plot vertical line centered at row['WL'], with y_value - 0.05 and y_value + 0.05
                    plt.plot([row['WL'], row['WL']], [y_value - LineSize, y_value + LineSize], color=color, linestyle='-', linewidth=1)
                    
                    # Add annotation with chemical name above the vertical line
                    if nameBool == 1:
                        if nmBool == 1:
                            output = f"{row['Chem']}, {row['WL']}nm"
                        else:
                            output = f"{row['Chem']}"
                        wordSize = (fontSize*dif*len(output))*0.0012
                        if y_value+LineSize+adjF+wordSize <= 0.9*ymax:
                            bar = LineSize+adjF
                        else:
                            bar = -(LineSize+adjF+wordSize)
                        plt.text(row['WL'], y_value + bar, output, ha='center', va='bottom', rotation=90, fontsize=fontSize)

    def add_shade(self, start, stop, color="blue", name="Water Bands"): 
    # Parameters for add_shade function:
    # - start: Starting wavelength of the shaded region.
    # - stop: Stopping wavelength of the shaded region.
    # - color: Color of the shaded region (default is "blue").
    # - name: Name or label for the shaded region (default is "Water Bands").

        # Save current y-axis limits
        ymin, ymax = plt.ylim()
        # Assuming lib contains the necessary x-axis values (e.g., wavelengths)
        x_values = np.array(self.wl)

        # Find corresponding positions in the plot based on x-axis values in lib
        start_pos = np.abs(x_values - start).argmin()
        stop_pos = np.abs(x_values - stop).argmin()

        # Create a shaded region between start_pos and stop_pos
        plt.axvspan(x_values[start_pos], x_values[stop_pos], color=color, alpha=0.1)
        
        # Add vertical lines on each side of the shaded region
        #plt.plot([x_values[start_pos], x_values[start_pos]], [ymin, ymax], color=color, linestyle='--', linewidth=1, alpha=0.2)
        #plt.plot([x_values[stop_pos], x_values[stop_pos]], [ymin, ymax], color=color, linestyle='--', linewidth=1, alpha=0.2)

        # Add text annotation to the shaded region
        midpoint = (x_values[start_pos] + x_values[stop_pos]) / 2
        plt.text(midpoint, ymax - 0.2 * (ymax - ymin), name, ha='center', va='center', rotation=90, fontsize=12)
        # Restore original y-axis limits
        plt.ylim(ymin, ymax)