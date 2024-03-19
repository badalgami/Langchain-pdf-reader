from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.llms import OpenAI
from langchain.chains import VectorDBQA
from langchain.document_loaders import TextLoader
import PyPDF2
import docx

vector_store = Chroma()
embeddings = OpenAIEmbeddings()
llm_model = OpenAI()
text_splitter = RecursiveCharacterTextSplitter()
doc_loader = TextLoader()

vector_dbqa = VectorDBQA(vector_store, embeddings, llm_model, text_splitter, doc_loader)

def perform_analysis(text):
    question = request.form.get('question')
    result = vector_dbqa.ask(question, text)
    return result

def read_file_content(uploaded_file):
    file_extension = uploaded_file.filename.split('.')[-1]
    if file_extension.lower() in ['pdf', 'txt']:
        # Read content based on file type
        if file_extension.lower() == 'pdf':
            text = read_pdf(uploaded_file)
        elif file_extension.lower() == 'txt':
            text = read_txt(uploaded_file)
        return text
    elif file_extension.lower() == 'docx':
        text = read_docx(uploaded_file)
        return text
    else:
        return None

def read_pdf(uploaded_file):
    # Initialize PDF reader
    pdf_reader = PyPDF2.PdfFileReader(uploaded_file)
    text = ''
    # Read every page of the PDF file
    for page_num in range(pdf_reader.numPages):
        text += pdf_reader.getPage(page_num).extractText()
    return text

def read_txt(uploaded_file):
    # Read content from the uploaded text file
    text = uploaded_file.read().decode('utf-8')
    return text

def read_docx(uploaded_file):
    # Initialize docx reader
    doc = docx.Document(uploaded_file)
    text = ''
    # Read each paragraph from the docx file
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text
