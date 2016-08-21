from flask import Flask, render_template, jsonify, request
from flask_bootstrap import Bootstrap
from config import port, host, debug
from dice import DiceController
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
Bootstrap(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///history.sqlite'
db = SQLAlchemy(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def index():
    return render_template('index.html', page='index')


@app.route('/myraspi/')
def myraspi():
    return render_template('index.html', page='myraspi')


@app.route('/dice/', methods=['GET', 'POST'])
def dice():
    d = DiceController(db)
    if request.method == 'POST':
        if request.form['submit'] == 'D4':
            d.roll(4, request.form.get('select'))
        elif request.form['submit'] == 'D6':
            d.roll(6, request.form.get('select'))
        elif request.form['submit'] == 'D8':
            d.roll(8, request.form.get('select'))
        elif request.form['submit'] == 'D10':
            d.roll(10, request.form.get('select'))
        elif request.form['submit'] == 'D12':
            d.roll(12, request.form.get('select'))
        elif request.form['submit'] == 'D20':
            d.roll(20, request.form.get('select'))
        elif request.form['submit'] == 'D100':
            d.roll(100, request.form.get('select'))

    player = d.last_ten_players()
    dices = d.last_ten_dices()
    result = d.last_ten_results()

    data = zip(player, dices, result)

    names = ['Basti', 'Juli', 'Phil', 'Lisa', 'Flo', 'Pieper']

    chances = []
    throws = []
    avgs = []
    for name in names:
        cc, throw, avg = d.crit_chance(name)
        chances.append(cc)
        avgs.append(avg)
        throws.append(throw)
    chances = zip(names, chances, throws, avgs)

    name = request.form.get('select')
    if name:
        names.remove(name)
        names.append(name)
        names.reverse()

    return render_template('index.html',
                           page='dice',
                           data=data,
                           names=names,
                           chances=chances)


@app.route('/dice2/', methods=['GET', 'POST'])
def dice2():
    d = DiceController(db)
    if request.method == 'POST':
        if request.form['submit'] == 'D4':
            d.roll(4, request.form.get('select'))
        elif request.form['submit'] == 'D6':
            d.roll(6, request.form.get('select'))
        elif request.form['submit'] == 'D8':
            d.roll(8, request.form.get('select'))
        elif request.form['submit'] == 'D10':
            d.roll(10, request.form.get('select'))
        elif request.form['submit'] == 'D12':
            d.roll(12, request.form.get('select'))
        elif request.form['submit'] == 'D20':
            d.roll(20, request.form.get('select'))
        elif request.form['submit'] == 'D100':
            d.roll(100, request.form.get('select'))

    names = ['Basti', 'Juli', 'Phil', 'Lisa', 'Flo', 'Pieper']
    names_std = ['Basti', 'Juli', 'Phil', 'Lisa', 'Flo', 'Pieper']
    tpl = []

    for name in names_std:
        idx = range(1, 11)
        tpl.append(zip(idx, d.last_ten_dices(name), d.last_ten_results(name)))

    name = request.form.get('select')
    if name:
        names.remove(name)
        names.append(name)
        names.reverse()

    return render_template('index.html',
                           page='dice2',
                           names=names,
                           names_std=names_std,
                           tpl=tpl)


@app.route('/_dice_results', methods=['GET'])
def dice_results():
    d = DiceController(db)

    player = d.last_ten_players()
    dices = d.last_ten_dices()
    result = d.last_ten_results()

    return jsonify(player=player, dice=dices, result=result)


@app.route('/_dice_results2', methods=['GET'])
def dice_results2():
    d = DiceController(db)
    names = ['Basti', 'Juli', 'Phil', 'Lisa', 'Flo', 'Pieper']
    tpl = []

    for name in names:
        tpl.append(zip(d.last_ten_dices(name), d.last_ten_results(name)))

    return jsonify(tpl=tpl, names=names)


@app.route('/_crit_chances', methods=['GET'])
def crit_chances():
    d = DiceController(db)
    names = ['Basti', 'Juli', 'Phil', 'Lisa', 'Flo', 'Pieper']

    chances = []
    throws = []
    avgs = []
    for name in names:
        cc, throw, avg = d.crit_chance(name)
        chances.append(cc)
        avgs.append(avg)
        throws.append(throw)

    return jsonify(chances=chances, names=names, throws=throws, avgs=avgs)

if __name__ == '__main__':
    app.run(port=port, debug=debug, host=host)
