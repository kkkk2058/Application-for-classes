from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('firstPage.html')

@app.route('/status')
def status():
    return render_template('sstatus.html')

@app.route('/buket')
def buket():
    return render_template('sbuket.html')


@app.route('/login')
def login():
    return render_template('slogin.html')

if __name__ == '__main__':
    app.run(debug=True)
