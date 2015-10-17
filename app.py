from flask import Flask, render_template, request, url_for, send_file
from tempfile import NamedTemporaryFile
from ricescheduler import make_url, sorted_classes, schedule, output_plain, output_docx, output_latex, output_html

app = Flask(__name__, static_url_path = "")

@app.route('/')
def form():
    years = [str(y) for y in range(2009,2017)][::-1]
    return render_template('form_submit.html', years=years)

@app.route('/output/', methods=['POST', 'GET'])
def output():

    semester = request.form['semester']
    year = request.form['year']
    weekdays = request.form.getlist('days')
    url = make_url(semester, year)
    possible_classes, no_classes = sorted_classes(weekdays, url)
    verbose = True
    course = schedule(possible_classes, no_classes, verbose) 


    if request.form['output'] == 'plain':
        return '<br/>'.join(course)
    elif request.form['output'] == 'docx':
        tf = NamedTemporaryFile(suffix='.docx')
        output_docx(course, semester, year, tf.name)
        filename = semester + year + 'Syllabus.docx'
        return send_file(tf.name, attachment_filename=filename, as_attachment=True)
    elif request.form['output'] == 'latex':
        tf = NamedTemporaryFile(suffix='.tex')
        output_latex(course, semester, year, tf.name)
        filename = semester + year + 'Syllabus.tex'
        return send_file(tf.name, attachment_filename=filename, as_attachment=True)
    elif request.form['output'] == 'html':
        tf = NamedTemporaryFile(suffix='.html')
        filename = semester + year + 'Syllabus.html'
        output_html(course, semester, year, tf.name)
        return send_file(tf.name, attachment_filename=filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
