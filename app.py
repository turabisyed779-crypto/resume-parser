from flask import Flask, request, jsonify
import re
import PyPDF2
import docx2txt

app = Flask(__name__)

# Function to extract text from PDF or DOCX
def extract_text(file):
    if file.filename.endswith('.pdf'):
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'
        return text
    elif file.filename.endswith('.docx'):
        return docx2txt.process(file)
    else:
        return ''

# Function to extract Name, Email, Phone, LinkedIn
def parse_resume(text):
    result = {}

    # Email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    result['email'] = email_match.group(0) if email_match else ''

    # Phone (simple pattern, adjust if needed)
    phone_match = re.search(r'\+?\d[\d\s\-\(\)]{7,}\d', text)
    result['phone'] = phone_match.group(0) if phone_match else ''

    # LinkedIn
    linkedin_match = re.search(r'linkedin\.com/[^\s]+', text)
    result['linkedin'] = linkedin_match.group(0) if linkedin_match else ''

    # Name (very basic: first line or first capitalized words)
    lines = text.split('\n')
    result['name'] = lines[0].strip() if lines else ''

    return result

@app.route('/parse_resume', methods=['POST'])
def parse_resume_endpoint():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    text = extract_text(file)
    data = parse_resume(text)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
