import json
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject
from flask import send_file
import tempfile
import os

class PDFHandler:
    def __init__(self, template_pdf_path="resources/permit_application.pdf"):
        self.template_pdf_path = template_pdf_path

    def fill_pdf(self, json_data_path):
        """
        Fill PDF form with data from JSON file and return the path to filled PDF
        
        Args:
            json_data_path (str): Path to the JSON file containing form data
        
        Returns:
            str: Path to the filled PDF file
        """
        try:
            # Create a temporary file for the filled PDF
            temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
            output_pdf_path = temp_pdf.name
            
            # Read the PDF
            reader = PdfReader(self.template_pdf_path)
            writer = PdfWriter()
            
            # Copy all pages from the source PDF to the writer
            for page in reader.pages:
                writer.add_page(page)
                
            # Copy the form data from the reader to the writer
            if "/AcroForm" in reader.trailer["/Root"]:
                writer._root_object.update({
                    NameObject("/AcroForm"): reader.trailer["/Root"]["/AcroForm"]
                })

            # Load JSON data
            with open(json_data_path, 'r') as f:
                form_data = json.load(f)

            # Update form fields with data from JSON
            # Apply to all pages
            for page_num in range(len(writer.pages)):
                writer.update_page_form_field_values(
                    writer.pages[page_num],
                    form_data
                )

            # Write the filled PDF to output file
            with open(output_pdf_path, "wb") as output_file:
                writer.write(output_file)
                
            return output_pdf_path
            
        except Exception as e:
            print(f"Error filling PDF: {str(e)}")
            return None

    def cleanup_temp_file(self, filepath):
        """Delete temporary file after it's been served"""
        try:
            if filepath and os.path.exists(filepath):
                os.unlink(filepath)
        except Exception as e:
            print(f"Error cleaning up temporary file: {str(e)}")
