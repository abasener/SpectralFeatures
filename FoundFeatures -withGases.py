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
from datetime import datetime
import re

class fFeat:
    def __init__ (self, wl, spec, name, type = "veg", folder_name=None, FetSave=1):
    # Parameters:
    # - wl: Array of wavelengths corresponding to the spectral data.
    # - spec: Array of reflectance values corresponding to the spectral data.
    # - name: Name or label associated with the spectral data.
    # - type: Type of data (default is "veg" for vegetation).
    # - folder_name: Name of the folder where the plot will be saved (default is current date: YYYY-MM-DD).
    # - FetSave: Control how the plots are saved: 0 for none, 1 for printed on screen, 2 for saved as a png, 3 for saved and printed.
        self.spec = spec
        self.wl = wl
        self.type = type
        self.name = name
        output_list = [self.name]
        output_list.append(f"Found Features: ")
        # Read data lines
        self.read_lines()
        # Determine folder name
        if folder_name is None:
            folder_name = datetime.now().strftime("%Y-%m-%d")
        # Create folder if it does not exist
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        self.folder_name = folder_name
       
        for index, row in self.dfL.iterrows():
            # Find the index of closest wavelength in centers_np to row['WL']
            idx = np.abs(np.array(self.wl) - row['WL']).argmin()
            y_value = self.spec[idx]  # Access the spectrum directly
            # Calculate the average reflectance value within the range
            average_reflectanceR = np.mean(self.spec[idx:idx + 35])
            average_reflectanceL = np.mean(self.spec[idx - 35:idx])

            # Compare y_value with the average_reflectance1
            if y_value < average_reflectanceR and y_value < average_reflectanceL:
                # Plot vertical line centered at row['WL'], with y_value - 0.05 and y_value + 0.05
                output = f"{row['Chem(Form)']}: {row['Chem']}, {row['WL']}nm"
                # Save the feachure name and wave legth
                output_list.append(f"{row['WL']}, {output}")

        if FetSave == 1 or FetSave == 3:
            for item in output_list:
                print(item)
        
        if FetSave == 2 or FetSave == 3:
            self.write_output_list_to_file(output_list)
        
    def read_lines(self):
        if self.type == "veg":
            file_path = 'Veg1.xlsx'
        if self.type == "mineral":
            file_path = 'Mineral1.xlsx'
        self.dfL = pd.read_excel(file_path)
    def write_output_list_to_file(self, output_list):
        # Create filename based on type and current time with milliseconds
        current_time = datetime.now().strftime("%H-%M-%S")
        # Sanitize the name by replacing invalid characters
        sanitized_name = re.sub(r'[<>:"/\\|?*]', '_', self.name)
        filename = f"{sanitized_name}_{current_time}.txt"
        filepath = os.path.join(self.folder_name, filename)
        
        # Write output_list to text file
        with open(filepath, 'w') as file:
            for item in output_list:
                file.write(f"{item}\n")
        
        print(f"Output list saved as {filename} in folder {self.folder_name}")