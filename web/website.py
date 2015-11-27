from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from config import port, host
app = Flask(__name__)
app.config.from_object('config')
Bootstrap(app)


@app.route('/')
def index():
    return render_template('index.html', page='index')


@app.route('/myraspi/')
def myraspi():
    return render_template('index.html', page='myraspi')

if __name__ == '__main__':
    app.run(port=port, debug=True, host=host)
