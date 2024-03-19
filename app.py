from flask import Flask, render_template, request
from main import perform_analysis, read_file_content

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        paragraph = request.form.get('paragraph')
        uploaded_file = request.files.get('file')
        
        if paragraph:
            result = perform_analysis(paragraph)
            return render_template('result.html', result=result)
        elif uploaded_file:
            file_content = read_file_content(uploaded_file)
            if file_content:
                result = perform_analysis(file_content)
                return render_template('result.html', result=result)
            else:
                return "Error: Unsupported file format."
        else:
            return "Error: No input provided."
    return "Error: Invalid request method."

if __name__ == '__main__':
    app.run(debug=True)
