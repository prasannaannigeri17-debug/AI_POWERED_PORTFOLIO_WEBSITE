import docx
import PyPDF2
def read(file_path):
    file_extension = file_path.split('.')[-1].lower()
    if file_extension == 'pdf':
        return read_pdf(file_path)
    elif file_extension == 'docx':
        return read_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a PDF or DOCX file.")

def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def read_docx(file_path):
    doc = docx.Document(file_path)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

