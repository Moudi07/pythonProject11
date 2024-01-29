import os
import pandas as pd
from skimage.io import imread
from skimage import color
from skimage.transform import resize
from skimage.filters import threshold_otsu, gaussian
from skimage import measure
from sklearn.preprocessing import MinMaxScaler
from natsort import natsorted
import joblib
import matplotlib.pyplot as plt

class ECG:
    def get_image(self, image_path):
        """
        Loads an image from the given path.
        
        :param image_path: Path to the image file
        :return: Loaded image
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        return imread(image_path)

    def convert_to_gray(self, image):
        """
        Converts the input image to grayscale and resizes it.
        
        :param image: Input image
        :return: Grayscale image
        """
        if len(image.shape) == 3 and image.shape[2] == 3:  # Check if the image is in RGB
            image_gray = color.rgb2gray(image)
        else:
            image_gray = image
        return resize(image_gray, (1572, 2213))

    def divide_leads(self, image):
        """
        Divides the ECG image into 13 Leads.
        
        :param image: Grayscale ECG image
        :return: List of divided leads
        """
        leads = [image[300:600, 150:643], image[300:600, 646:1135],  # Leads 1, aVR
                 # ... other leads ...
                 image[1250:1480, 150:2125]]  # Long Lead
        
        # Plotting leads 1-12
        fig, ax = plt.subplots(4, 3)
        fig.set_size_inches(10, 10)
        for i, lead in enumerate(leads[:-1]):
            ax[i // 3, i % 3].imshow(lead)
            ax[i // 3, i % 3].axis('off')
            ax[i // 3, i % 3].set_title(f"Lead {i + 1}")
        fig.savefig('Leads_1-12_figure.png')

        # Plotting lead 13
        fig1, ax1 = plt.subplots()
        fig1.set_size_inches(10, 10)
        ax1.imshow(leads[-1])
        ax1.set_title("Lead 13")
        ax1.axis('off')
        fig1.savefig('Long_Lead_13_figure.png')

        return leads

    def preprocess_leads(self, leads):
        """
        Preprocesses each ECG lead by converting to binary and resizing.
        
        :param leads: List of ECG leads
        :return: List of preprocessed leads
        """
        preprocessed_leads = []
        fig2, ax2 = plt.subplots(4, 3)
        fig2.set_size_inches(10, 10)
        x_counter, y_counter = 0, 0

        for x, lead in enumerate(leads[:-1]):
            grayscale = color.rgb2gray(lead)
            blurred_image = gaussian(grayscale, sigma=1)
            global_thresh = threshold_otsu(blurred_image)
            binary_global = blurred_image < global_thresh
            binary_global = resize(binary_global, (300, 450))
            preprocessed_leads.append(binary_global)
            ax2[x_counter, y_counter].imshow(binary_global, cmap="gray")
            ax2[x_counter, y_counter].axis('off')
            ax2[x_counter, y_counter].set_title(f"Pre-processed Lead {x + 1}")
            
            if (x + 1) % 3 == 0:
                x_counter += 1
                y_counter = 0
            else:
                y_counter += 1

        fig2.savefig('Preprocessed_Leads_1-12_figure.png')

        # Process and plot Lead 13
        fig3, ax3 = plt.subplots()
        fig3.set_size_inches(10, 10)
        grayscale = color.rgb2gray(leads[-1])
        blurred_image = gaussian(grayscale, sigma=1)
        global_thresh = threshold_otsu(blurred_image)
        binary_global = blurred_image < global_thresh
        ax3.imshow(binary_global, cmap='gray')
        ax3.set_title("Lead 13")
        ax3.axis('off')
        fig3.savefig('Preprocessed_Lead_13_figure.png')

        return preprocessed_leads

    # Additional methods for SignalExtraction_Scaling, CombineConvert1Dsignal, etc.
    # ...

# Example usage
ecg_processor = ECG()
image = ecg_processor.get_image("path_to_image.jpg")
gray_image = ecg_processor.convert_to_gray(image)
leads = ecg_processor.divide_leads(gray_image)
preprocessed_leads = ecg_processor.preprocess_leads(leads)
