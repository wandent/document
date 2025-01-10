

# Convert the pdf files found on the current folder into images on the folder ./images
# The images are named as the pdf file with the page number appended to it.
# The images are in the format png.
# each page in the pdf document should be converted to a separate image.
# The images are in the resolution 300 dpi.
# The images are in the color space RGB.



# create a function to convert the pdf files into images
import os
from pdf2image import convert_from_path
from PIL import ImageFilter
import pandas as pd
from fpdf import FPDF

def pdf_to_png(pdf_file):
    # Create the output directory if it doesn't exist
    output_dir = "./images"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Convert PDF to a list of images
    images = convert_from_path(pdf_file)
    
    # Save each image as a PNG file
    for i, image in enumerate(images):
        output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(pdf_file))[0] + f"page_{i + 1}.jpg")
        # i'd like to invert the colors of the image
        #image = image.convert("RGB")
        #image = image.point(lambda p: 255 - p)    
        #image = image.filter(ImageFilter.SHARPEN)
        # enhance the image constrast
        #image = image.point(lambda p: p * 1.5)    
        image.save(output_file, 'JPEG')       
    

# create a function xls_to_pdf to convert the xls files into pdf
def xls_to_pdf(xls_file):
    # Create the output directory if it doesn't exist
    output_dir = "./document"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    

    # read each tab of the excel file
    xls_file = pd.ExcelFile(xls_file)
    # convert each tab of the excel file into a pdf file
    for sheet_name in xls_file.sheet_names:
        df = pd.read_excel(xls_file, sheet_name)
        
        # Create a PDF object
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Add the data to the PDF
        for i in range(len(df)):
            row = df.ser.iloc[i]
            for j in range(len(row)):
                pdf.cell(200, 10, str(row[j]), 1, 0, 'C')
            pdf.ln()
        
        # Save the PDF to a file
        output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(xls_file))[0] + f"_{sheet_name}.pdf")
        pdf.output(output_file)
        
    # Save the PDF to a file
    output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(xls_file))[0] + ".pdf")
    pdf.output(output_file)


# create the main function
def main():
    
    # convert xls files to pdf

    # convert the xls files to pdf
    # run the xls_to_pdf function on all the xls files located on ./documents folder
    for xls_file in [f for f in os.listdir("./document") if f.endswith(".xlsx")]:
        # ignore if the file exists
        if not os.path.exists(os.path.join("./document", os.path.splitext(xls_file)[0] + ".pdf")):
            xls_to_pdf(os.path.join("./document", xls_file))

    # run the pdf_to_png function on all the pdf files located on ./documents folder
    for pdf_file in [f for f in os.listdir("./document") if f.endswith(".pdf")]:
        pdf_to_png(os.path.join("./document", pdf_file))
        
# call the main function
if __name__ == "__main__":
    main()
