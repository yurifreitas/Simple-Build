from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import logging

# Init app
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
from models import Pacote


@app.route('/')
def index():
    list = db.session.execute("select rowid, * from pacote")
    rows = list.fetchall()
    return render_template("list.html", rows=rows)


@app.route('/tax', methods=['POST'])
def tax():
    if request.method == "POST" and request.get_json():
        pac = request.get_json()
        pac_tax = calc_tax(pac['price'], pac['weight'], pac['height'], pac['length'], pac['width'])
        return jsonify({"tax": pac_tax})
    else:
        logging.warning("Requisição invalida")
        return "ERROR", 404


@app.route('/track', methods=['POST'])
def list_product_track():
    if request.method == "POST" and request.get_json():
        dict_body = request.get_json()  # convert body to dictionary
        print(dict_body)  # have a look at what is coming in
        packet = Pacote(name=dict_body['name'],
                        height=dict_body['height'],
                        length=dict_body['length'],
                        width=dict_body['width'],
                        weight=dict_body['weight'],
                        price=dict_body['price'])

        db.session.add(packet)
        db.session.commit()
        id = db.session.execute("select MAX(rowid) from pacote")
        id = int(id.fetchone()[0])
    else:
        logging.warning("Requisição invalida")
        return "ERROR", 404

    return jsonify({"ID": id})


@app.route('/track/<int:id_pacote>')
def list_product(id_pacote):
    pacote_id = db.session.execute("select rowid,* from pacote where rowid =" + str(id_pacote))
    rows = pacote_id.fetchall()
    return render_template("list.html", rows=rows)


@app.route('/reset/', methods=['POST'])
def reset():
    db.session.query(Pacote).delete()
    db.session.commit()

    return ""

@app.route('/remove/<int:id>', methods=['POST'])
def remove(id):
    db.session.query(Pacote).filter(rowid = id).delete()
    db.session.commit()

    return ""
# CALCULA O PESO REAL DO PRODUTO
def calc_weight(height, length, width):
    height = convert_float(height)
    length = convert_float(length)
    width = convert_float(width)
    try:
        volume = height * length * width
    except:
        logging.critical("ERRO AO CALCULAR O VOLUME height:%s length:%s width:%s", str(height), str(length), str(width))
    try:
        peso = volume * 300.0
    except:
        logging.critical("ERRO AO CALCULAR O PESO volume:%s", str(volume))
    return peso


# CALCULA AS TAXAS SOBRE O PRODUTO
def calc_tax(price, weight, height, length, width):
    price = convert_float(price)
    weight = convert_float(weight)
    calcw = calc_weight(height, length, width)
    if calcw <= 100:
        try:
            tax = price * 5.0 / 100.0
        except:
            logging.critical("ERRO AO CALCULAR A TAX MENOR QUE 100 price:%s", str(price))
        return '{:.2f}'.format(tax)
    elif calcw > 100:
        try:
            tax = calcw * weight

        except:
            logging.critical("ERRO AO CALCULAR A TAX MAIOR QUE 100 weight:%s weight_cal:%s", str(weight), str(calcw))
        return '{:.2f}'.format(tax)
    else:
        logging.critical("ERRROR CALC TAX weight_cal:%s", str(calcw))
        return 0.0


# REMOVE A VIRGULA E SUBSTITUI PARA PONTO PARA CONVERTER
def convert_float(str_json):
    try:
        str_json = float(str_json.replace(",", "."))
    except:
        logging.critical("Erro ao converter: " + str_json)
    return str_json



if __name__ == '__main__':
    app.run(debug='True')
