import json
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject

def fill_pdf(input_pdf_path, output_pdf_path, json_data_path):
    """
    Fill PDF form with data from JSON file
    
    Args:
        input_pdf_path (str): Path to the input PDF form
        output_pdf_path (str): Path where to save the filled PDF
        json_data_path (str): Path to the JSON file containing form data
    """
    try:
        # Read the PDF
        reader = PdfReader(input_pdf_path)
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
        writer.update_page_form_field_values(
            writer.pages[0],  # assuming all fields are on the first page
            form_data
        )

        # Write the filled PDF to output file
        with open(output_pdf_path, "wb") as output_file:
            writer.write(output_file)
            
        print(f"Successfully created filled PDF: {output_pdf_path}")
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {str(e)}")
    except Exception as e:
        print(f"Error filling PDF: {str(e)}")

def main():
    # Paths
    input_pdf = "resources/permit_application.pdf"
    output_pdf = "filled_permit_application.pdf"
    json_data = "permit_template.json"
    
    # Fill the PDF
    fill_pdf(input_pdf, output_pdf, json_data)

if __name__ == "__main__":
    main()
