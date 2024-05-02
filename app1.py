import streamlit as st
import cv2
import pytesseract
import os
from openpyxl import Workbook, load_workbook
import base64
import numpy as np

# Define the path for the Excel file
excel_file = "/Users/karan/Downloads/output.xlsx"

# Function to process images and extract information
def process_image(image):
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform OCR on the grayscale image
    data = pytesseract.image_to_string(gray)

    # Extract relevant information from OCR results
    patient_name = None
    contact = None
    address = None
    date = None

    data = data.split("\n")
    for item in data:
        if 'Patient Name:' in item:
            patient_name = item.split(':')[-1].strip()
        elif 'Contact:' in item:
            contact = item.split(':')[-1].strip()
        elif 'Address:' in item:
            address = item.split(':')[-1].strip()
        elif 'Date:' in item:
            date = item.split(':')[1].strip()

    return patient_name, contact, address, date

# Streamlit app
def main():
    st.title('Image Processing and Data Extraction')

    # File upload widget
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Read the uploaded image
        file_bytes = uploaded_file.read()
        nparr = np.frombuffer(file_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Display the uploaded image
        st.image(image, caption='Uploaded Image', use_column_width=True)

        # Process the uploaded image
        patient_name, contact, address, date = process_image(image)

        # Display the extracted information
        st.write("Extracted Information:")
        st.write("Patient Name:", patient_name)
        st.write("Contact:", contact)
        st.write("Address:", address)
        st.write("Date:", date)

        # Save the extracted information to the Excel file
        try:
            wb = load_workbook(excel_file)
            ws = wb.active
            ws.append([patient_name, contact, address, date])
            wb.save(excel_file)
        except Exception as e:
            st.error(f"Error saving Excel file: {e}")

if __name__ == '__main__':
    main()
