from deepface import DeepFace
import os
import pandas as pd
import cv2
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")  


def visualize_attribute(img_path, result, attribute="age"):
    # Read and convert the image
    image = cv2.imread(img_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Generate the display text
    text = f"{attribute}: {result[0].get(attribute, 'not found')}"

    # Display the image with the attribute text
    plt.imshow(image_rgb)
    plt.axis('off')
    plt.title(text)
    plt.show()

# Example usage
visualize_attribute(img_path, result, "age")
