from flask import Flask, render_template, url_for, request
from flask_bootstrap import Bootstrap5
from code_chars import MORSE_CODE_CHARS
from codes import APP_KEY, letters, numbers, symbols
import subprocess


app = Flask(__name__)
app.config['SECRET_KEY'] = APP_KEY
Bootstrap5(app)


def convert_to_morse_code(plain_text):
    morse_code = ''
    for char in plain_text:
       if char == ' ':
            morse_code += ' / '
       else:
            morse_code += MORSE_CODE_CHARS[char.upper()] + ' '
    return morse_code


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/morse_code', methods=['GET', 'POST'])
def morse_code():
    if request.method == 'POST':
        try:
            plain_text = request.form['plain_text']
            morse_code_output = convert_to_morse_code(plain_text)
            return render_template('morse_code.html', plain_text=plain_text, morse_code_output=morse_code_output)
        except subprocess.CalledProcessError as e:
            return f"Error running morse_code function: {e}"

        # Return the form if the request method is GET
    return render_template('morse_code.html')



@app.route('/app2', methods=['GET', 'POST'])
def app2():
    return render_template('app2.html')


@app.route('/app3', methods=['GET', 'POST'])
def app3():
    return render_template('app3.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
    # app.run(debug=True)