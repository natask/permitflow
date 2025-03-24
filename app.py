from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from dotenv import load_dotenv
from pdf_handler import PDFHandler
from maestro_processor import process_permit_data
from zipcode_price import zipcode_price
import json
import os
from datetime import datetime

load_dotenv()

app = Flask(__name__)
pdf_handler = PDFHandler()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view-pdf')
def view_pdf():
    return render_template('pdf_viewer.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Get user input directly from request
        user_input_json = request.get_json()
        app.logger.info(f"Received input: {user_input_json}")
        
        # Read permit template
        template_path = os.path.join(os.path.dirname(__file__), 'resources', 'permit_template.json')
        app.logger.info(f"Reading template from: {template_path}")
        
        with open(template_path, 'r') as f:
            template_json = f.read()
        app.logger.info("Template loaded successfully")
        
        # Process through Maestro
        app.logger.info("Starting Maestro processing...")
        try:
            price = zipcode_price(user_input_json['zipcode'])
            result = process_permit_data(template_json, json.dumps(user_input_json), price)
            app.logger.info(f"Maestro result: {result}")
        except Exception as e:
            app.logger.error(f"Maestro processing failed: {str(e)}")
            raise
        
        # Save result to resources directory with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(os.path.dirname(__file__), 'resources', f'fill_pdf_{timestamp}.json')
        app.logger.info(f"Saving timestamped result to: {output_path}")
        
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
            
        # Also save as fill_pdf.json for the PDF endpoint
        standard_path = os.path.join(os.path.dirname(__file__), 'resources', 'fill_pdf.json')
        app.logger.info(f"Saving standard result to: {standard_path}")
        
        with open(standard_path, 'w') as f:
            json.dump(result, f, indent=2)
        
        app.logger.info("Processing complete, redirecting to PDF viewer")
        # Redirect to PDF endpoint
        return redirect(url_for('serve_pdf'))
        
    except Exception as e:
        app.logger.error(f"Error in submit endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/pdf')
def serve_pdf():
    try:
        # Use the generated fill_pdf.json
        json_path = os.path.join(os.path.dirname(__file__), 'resources', 'fill_pdf.json')
        app.logger.info(f"Generating PDF using JSON from: {json_path}")
        
        filled_pdf_path = pdf_handler.fill_pdf(json_path)
        
        if filled_pdf_path:
            app.logger.info(f"PDF generated successfully at: {filled_pdf_path}")
            try:
                # Send the file inline (to display in browser) instead of as attachment
                response = send_file(
                    filled_pdf_path,
                    mimetype='application/pdf',
                    as_attachment=False  # This makes it display in the browser
                )
                
                # Register cleanup callback
                @response.call_on_close
                def cleanup():
                    pdf_handler.cleanup_temp_file(filled_pdf_path)
                    app.logger.info("Temporary PDF file cleaned up")
                    
                return response
            except Exception as e:
                app.logger.error(f"Error serving PDF: {str(e)}")
                return f"Error serving PDF: {str(e)}", 500
        else:
            app.logger.error("PDF generation failed")
            return "Error generating PDF", 500
    except Exception as e:
        app.logger.error(f"Error in PDF endpoint: {str(e)}")
        return f"Error in PDF endpoint: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)