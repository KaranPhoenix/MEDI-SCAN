import streamlit as st
import cv2
import pytesseract
import os
from openpyxl import Workbook
import base64
import numpy as np
import matplotlib.pyplot as plt

# Function to process images and extract information
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

    # Additional text extraction from OCR results
    data = data.split("\n")
    print("Extracted OCR Text:", data)  # Debug print to see extracted text
    for item in data:
        if 'Patient Name:' in item:
            patient_name = item.split(':')[-1].strip()
        elif 'Contact:' in item:
            contact = item.split(':')[-1].strip()
        elif 'Address:' in item:
            address = item.split(':')[-1].strip()
        elif 'Date:' in item:
            date = item.split(':')[1].strip()

    # Find contours
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw contours on the original image
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x+w, y+h), (36, 255, 12), 2)

    return patient_name, contact, address, date, image



    # Find contours
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Draw contours on the original image
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(image, (x, y), (x+w, y+h), (36, 255, 12), 2)

    return patient_name, contact, address, date, image

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
        patient_name, contact, address, date, processed_image = process_image(image)

        # Display the extracted information
        st.write("Extracted Information:")
        st.write("Patient Name:", patient_name)
        st.write("Contact:", contact)
        st.write("Address:", address)
        st.write("Date:", date)

        # Display the image with contours
        st.image(processed_image, caption='Image with Contours', use_column_width=True)

        # Save the extracted information to an Excel file
        excel_folder = "output"
        os.makedirs(excel_folder, exist_ok=True)
        excel_path = os.path.join(excel_folder, "extracted_data.xlsx")

        wb = Workbook()
        ws = wb.active
        ws.append(["Patient Name", "Contact", "Address", "Date"])
        ws.append([patient_name, contact, address, date])
        wb.save(excel_path)

        # Provide a download link for the Excel file
        st.write('Download the extracted data [here](data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{})'.format(
            base64.b64encode(open(excel_path, "rb").read()).decode()
        ), unsafe_allow_html=True)

if __name__ == '__main__':
    main()
