from flask import Flask, request, render_template
import PyPDF2
import docx

app = Flask(__name__)

def extract_text_from_pdf(pdf_file):
    text = ''
    reader = PyPDF2.PdfReader(pdf_file)  # Use FileStorage object directly
    for page in reader.pages:
        text += page.extract_text() + '\n'
    return text

def extract_text_from_docx(docx_file):
    text = ''
    doc = docx.Document(docx_file)  # Use FileStorage object directly
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

def calculate_score(resume_text, job_description):
    resume_words = set(resume_text.lower().split())
    job_words = set(job_description.lower().split())
    matching_words = resume_words.intersection(job_words)
    score = (len(matching_words) / len(job_words)) * 100 if job_words else 0
    return score

@app.route('/', methods=['GET', 'POST'])
def index():
    score = 0  # Initialize score to 0 by default
    job_description = ''
    uploaded_file = None

    if request.method == 'POST':
        job_description = request.form['job_description']
        uploaded_file = request.files['file']

        if uploaded_file and uploaded_file.filename:  # Check if a file is uploaded
            if uploaded_file.filename.endswith('.pdf'):
                resume_text = extract_text_from_pdf(uploaded_file)
            elif uploaded_file.filename.endswith('.docx'):
                resume_text = extract_text_from_docx(uploaded_file)
            else:
                return 'Invalid file format. Please upload a PDF or DOCX file.'

            # Calculate the score only if resume text is extracted successfully
            if resume_text:
                score = calculate_score(resume_text, job_description)

    return render_template('index.html', score=score, job_description=job_description, uploaded_file=uploaded_file)

if __name__ == '__main__':
    app.run(debug=True)
