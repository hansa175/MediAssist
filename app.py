import speech_recognition as sr
from flask import Flask, request, jsonify, send_file, render_template
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

# Function to generate PDF Prescription
def generate_pdf(name, age, contact, speech_text):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Writing the prescription details
    c.setFont("Helvetica", 12)
    c.drawString(100, 750, "Prescription")
    c.drawString(100, 730, f"Name: {name}")
    c.drawString(100, 710, f"Age: {age}")
    c.drawString(100, 690, f"Contact: {contact}")
    c.drawString(100, 670, f"Speech Transcript: {speech_text}")

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer

@app.route('/process_speech', methods=['POST'])
def process_speech_route():
    # Get the data from the frontend
    data = request.get_json()
    name = data['name']
    age = data['age']
    contact = data['contact']
    speech_text = data['speech']  # Recognized speech text

    # Generate the prescription PDF
    pdf_buffer = generate_pdf(name, age, contact, speech_text)

    # Send the PDF as a response
    return send_file(pdf_buffer, as_attachment=True, download_name="prescription.pdf", mimetype='application/pdf')

@app.route('/')
def home():
    return render_template('index.html')  # Ensure this template exists

if __name__ == '__main__':
    app.run(debug=True)


